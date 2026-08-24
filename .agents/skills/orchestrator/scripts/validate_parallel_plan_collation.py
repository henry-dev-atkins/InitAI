#!/usr/bin/env python3
"""Validate authorised plan collation and shared-checkout parallel safety."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from schema_validation import validate as validate_schema
from validate_contract_register import validate_register as validate_contracts
from validate_finding_register_current import validate_register as validate_findings
from workflow_common import (
    any_scope_overlap,
    load_json,
    parse_markdown_table,
    repo_path,
    split_ids,
)

ELIGIBLE_STATES = {"PLANNING", "AWAITING_PLAN_COLLATION", "REPLANNING"}


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def load_json_or_fenced(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if not match:
        raise ValueError("no JSON object or fenced JSON block found")
    return json.loads(match.group(1))


def normalise_scopes(values: list, label: str, errors: list[str], repo: Path) -> list[str]:
    output: list[str] = []
    for value in values:
        try:
            resolved = repo_path(repo, str(value))
            normalised = resolved.relative_to(repo).as_posix()
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if normalised == ".":
            errors.append(f"{label}: repository root is too broad")
        output.append(normalised)
    for duplicate in sorted({item for item in output if output.count(item) > 1}):
        errors.append(f"{label}: duplicate scope: {duplicate}")
    return output


def within_scope_overlaps(values: list[str]) -> list[tuple[str, str]]:
    return [
        (left, right)
        for index, left in enumerate(values)
        for right in values[index + 1 :]
        if any_scope_overlap([left], [right])
    ]


def authority_path(repo: Path, value: Path, label: str, errors: list[str]) -> Path | None:
    try:
        path = repo_path(repo, str(value))
    except ValueError as exc:
        errors.append(f"{label}: {exc}")
        return None
    if not path.is_file():
        errors.append(f"{label}: file does not exist: {value}")
        return None
    return path


def validate_ids(values: list, pattern: str, label: str, plan_id: str, errors: list[str]) -> None:
    for value in values:
        if not isinstance(value, str) or not re.fullmatch(pattern, value):
            errors.append(f"{plan_id}: invalid {label}: {value}")


def row_values(row: dict[str, str], column: str) -> list[str]:
    return split_ids(row.get(column, ""))


def compare_authority(plan_id: str, label: str, actual: list[str], expected: list[str], errors: list[str]) -> None:
    if set(actual) != set(expected):
        errors.append(f"{plan_id}: {label} differs from workstream authority: actual={sorted(actual)} expected={sorted(expected)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--workstream-register", type=Path, required=True)
    parser.add_argument("--finding-register", type=Path, required=True)
    parser.add_argument("--requirement-register", type=Path, required=True)
    parser.add_argument("--contract-register", type=Path, required=True)
    parser.add_argument("--locks", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    errors: list[str] = []
    portfolio_path = authority_path(repo, args.portfolio, "portfolio", errors)
    workstream_path = authority_path(repo, args.workstream_register, "workstream register", errors)
    finding_path = authority_path(repo, args.finding_register, "finding register", errors)
    requirement_path = authority_path(repo, args.requirement_register, "requirement register", errors)
    contract_path = authority_path(repo, args.contract_register, "contract register", errors)
    locks_path = authority_path(repo, args.locks, "locks", errors)
    if errors:
        return fail(errors)

    try:
        data = load_json_or_fenced(portfolio_path)
        workstream_headers, workstream_rows = parse_markdown_table(workstream_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail([str(exc)])

    required_workstream_headers = {
        "Workstream", "Findings", "Requirement IDs", "Depends On", "Write Scope",
        "Stable Read Scope", "Contracts Changed", "Contracts Consumed",
        "Mutable Resources", "Plan", "State",
    }
    missing_headers = sorted(required_workstream_headers - set(workstream_headers))
    if missing_headers:
        errors.append(f"workstream register missing columns: {missing_headers}")
    if not isinstance(data, dict):
        return fail(["portfolio root must be an object"])
    plans = data.get("plans")
    if not isinstance(plans, list) or not plans:
        return fail(["portfolio must contain a non-empty plans array"])

    workstream_ids_in_register = [row.get("Workstream", "") for row in workstream_rows]
    for duplicate in sorted({item for item in workstream_ids_in_register if item and workstream_ids_in_register.count(item) > 1}):
        errors.append(f"duplicate workstream register ID: {duplicate}")
    workstreams = {row.get("Workstream", ""): row for row in workstream_rows}

    errors.extend(f"finding register: {item}" for item in validate_findings(finding_path))
    errors.extend(f"contract register: {item}" for item in validate_contracts(contract_path))
    try:
        finding_data = load_json(finding_path)
        requirement_data = load_json(requirement_path)
        requirement_schema = load_json(repo / ".agents/skills/orchestrator/assets/requirement-register.schema.json")
        contract_data = load_json(contract_path)
    except (OSError, ValueError) as exc:
        return fail([*errors, str(exc)])
    requirement_errors = validate_schema(requirement_data, requirement_schema)
    errors.extend(f"requirement register: {item}" for item in requirement_errors)
    if not isinstance(finding_data, dict):
        return fail([*errors, "finding register root must be an object"])
    if not isinstance(requirement_data, dict):
        return fail([*errors, "requirement register root must be an object"])
    if not isinstance(contract_data, dict):
        return fail([*errors, "contract register root must be an object"])
    finding_items = finding_data.get("findings", [])
    requirement_items = requirement_data.get("requirements", [])
    contract_items = contract_data.get("contracts", [])
    finding_ids = {item["id"] for item in finding_items if isinstance(item, dict) and "id" in item}
    requirement_ids = {item["id"] for item in requirement_items if isinstance(item, dict) and "id" in item}
    contract_ids = {item["id"] for item in contract_items if isinstance(item, dict) and "id" in item}
    for finding in finding_items:
        if not isinstance(finding, dict):
            continue
        for requirement_id in finding.get("requirement_ids", []):
            if requirement_id not in requirement_ids:
                errors.append(f"finding register: {finding.get('id', 'unknown')} references unknown requirement: {requirement_id}")

    plan_ids: list[str] = []
    workstream_ids: list[str] = []
    normalised_plans: list[dict] = []
    for index, plan in enumerate(plans):
        if not isinstance(plan, dict):
            errors.append(f"plans[{index}] is not an object")
            continue
        plan_id = plan.get("plan_id")
        workstream_id = plan.get("workstream_id")
        if not isinstance(plan_id, str) or not re.fullmatch(r"P[0-9]{3,}", plan_id):
            errors.append(f"invalid plan_id: {plan_id}")
        else:
            plan_ids.append(plan_id)
        if not isinstance(workstream_id, str) or not re.fullmatch(r"WS[0-9]{3,}", workstream_id):
            errors.append(f"{plan_id}: invalid workstream_id: {workstream_id}")
        else:
            workstream_ids.append(workstream_id)

        required_arrays = [
            "findings", "requirement_ids", "write_scope", "stable_read_scope",
            "contracts_changed", "contracts_consumed", "mutable_resources", "dependencies",
        ]
        for key in required_arrays:
            if not isinstance(plan.get(key), list):
                errors.append(f"{plan_id}: {key} must be an array")
                plan[key] = []
        if not plan.get("findings"):
            errors.append(f"{plan_id}: findings must be a non-empty array")
        if not plan.get("requirement_ids"):
            errors.append(f"{plan_id}: requirement_ids must be a non-empty array")

        plan_copy = dict(plan)
        plan_copy["write_scope"] = normalise_scopes(plan.get("write_scope", []), f"{plan_id} write_scope", errors, repo)
        plan_copy["stable_read_scope"] = normalise_scopes(plan.get("stable_read_scope", []), f"{plan_id} stable_read_scope", errors, repo)
        normalised_plans.append(plan_copy)
        validate_ids(plan["findings"], r"F[0-9]{3,}", "finding ID", str(plan_id), errors)
        validate_ids(plan["requirement_ids"], r"REQ[0-9]{3,}", "requirement ID", str(plan_id), errors)
        validate_ids(plan["contracts_changed"], r"CON[0-9]{3,}", "changed contract ID", str(plan_id), errors)
        validate_ids(plan["contracts_consumed"], r"CON[0-9]{3,}", "consumed contract ID", str(plan_id), errors)
        validate_ids(plan["dependencies"], r"WS[0-9]{3,}", "dependency ID", str(plan_id), errors)
        if workstream_id in plan["dependencies"]:
            errors.append(f"{plan_id}: workstream may not depend on itself")
        for left, right in within_scope_overlaps(plan_copy["write_scope"]):
            errors.append(f"{plan_id}: overlapping write scopes: {left} <-> {right}")
        for left, right in within_scope_overlaps(plan_copy["stable_read_scope"]):
            errors.append(f"{plan_id}: overlapping stable-read scopes: {left} <-> {right}")
        for left, right in any_scope_overlap(plan_copy["write_scope"], plan_copy["stable_read_scope"]):
            errors.append(f"{plan_id}: own write/stable-read conflict: {left} <-> {right}")

        row = workstreams.get(str(workstream_id))
        if row is None:
            errors.append(f"{plan_id}: workstream not found in register: {workstream_id}")
            continue
        if row.get("State") not in ELIGIBLE_STATES:
            errors.append(f"{plan_id}: workstream state is not eligible for collation: {row.get('State')}")
        if row.get("Plan") != plan_id:
            errors.append(f"{plan_id}: plan ID differs from workstream authority: {row.get('Plan')}")
        compare_authority(plan_id, "findings", [str(item) for item in plan["findings"]], row_values(row, "Findings"), errors)
        compare_authority(plan_id, "requirement IDs", [str(item) for item in plan["requirement_ids"]], row_values(row, "Requirement IDs"), errors)
        compare_authority(plan_id, "write scope", plan_copy["write_scope"], normalise_scopes(row_values(row, "Write Scope"), f"{plan_id} authorised write scope", errors, repo), errors)
        compare_authority(plan_id, "stable read scope", plan_copy["stable_read_scope"], normalise_scopes(row_values(row, "Stable Read Scope"), f"{plan_id} authorised stable read scope", errors, repo), errors)
        compare_authority(plan_id, "contracts changed", [str(item) for item in plan["contracts_changed"]], row_values(row, "Contracts Changed"), errors)
        compare_authority(plan_id, "contracts consumed", [str(item) for item in plan["contracts_consumed"]], row_values(row, "Contracts Consumed"), errors)
        compare_authority(plan_id, "mutable resources", [str(item) for item in plan["mutable_resources"]], row_values(row, "Mutable Resources"), errors)
        compare_authority(plan_id, "dependencies", [str(item) for item in plan["dependencies"]], row_values(row, "Depends On"), errors)

        for dependency in plan["dependencies"]:
            dependency_row = workstreams.get(str(dependency))
            if dependency_row is None:
                errors.append(f"{plan_id}: dependency not found: {dependency}")
            elif dependency_row.get("State") != "ACCEPTED":
                errors.append(f"{plan_id}: dependency is not ACCEPTED: {dependency}={dependency_row.get('State')}")
        for finding in plan["findings"]:
            if finding not in finding_ids:
                errors.append(f"{plan_id}: unknown finding ID: {finding}")
        for requirement_id in plan["requirement_ids"]:
            if requirement_id not in requirement_ids:
                errors.append(f"{plan_id}: unknown requirement ID: {requirement_id}")
        for contract in [*plan["contracts_changed"], *plan["contracts_consumed"]]:
            if contract not in contract_ids:
                errors.append(f"{plan_id}: unknown contract ID: {contract}")

    for duplicate in sorted({item for item in plan_ids if plan_ids.count(item) > 1}):
        errors.append(f"duplicate plan_id: {duplicate}")
    for duplicate in sorted({item for item in workstream_ids if workstream_ids.count(item) > 1}):
        errors.append(f"duplicate workstream_id: {duplicate}")

    for i, left in enumerate(normalised_plans):
        for right in normalised_plans[i + 1 :]:
            left_id = left.get("plan_id", f"plans[{i}]")
            right_id = right.get("plan_id", "unknown")
            for a, b in any_scope_overlap(left["write_scope"], right["write_scope"]):
                errors.append(f"write scope overlap: {left_id} {a} <-> {right_id} {b}")
            for a, b in any_scope_overlap(left["write_scope"], right["stable_read_scope"]):
                errors.append(f"write/stable-read conflict: {left_id} {a} -> {right_id} {b}")
            for a, b in any_scope_overlap(right["write_scope"], left["stable_read_scope"]):
                errors.append(f"write/stable-read conflict: {right_id} {a} -> {left_id} {b}")
            left_changed = set(left["contracts_changed"])
            left_consumed = set(left["contracts_consumed"])
            right_changed = set(right["contracts_changed"])
            right_consumed = set(right["contracts_consumed"])
            for contract in sorted(
                (left_changed & right_consumed)
                | (right_changed & left_consumed)
                | (left_changed & right_changed)
            ):
                errors.append(f"contract conflict: {left_id} <-> {right_id}: {contract}")
            for resource in sorted(set(left["mutable_resources"]) & set(right["mutable_resources"])):
                errors.append(f"mutable resource conflict: {left_id} <-> {right_id}: {resource}")

    lock_headers, lock_rows = parse_markdown_table(locks_path)
    required_lock_headers = {
        "Workstream", "Write Scope", "Stable Read Scope", "Contract IDs",
        "Mutable Resources", "Status",
    }
    missing_lock_headers = sorted(required_lock_headers - set(lock_headers))
    if missing_lock_headers:
        errors.append(f"locks register missing columns: {missing_lock_headers}")
    for plan in normalised_plans:
        plan_id = plan.get("plan_id", "unknown")
        workstream_id = plan.get("workstream_id")
        for row in lock_rows:
            if row.get("Workstream") == workstream_id or row.get("Status", "").lower() not in {"reserved", "active"}:
                continue
            locked_write = normalise_scopes(row_values(row, "Write Scope"), "lock write scope", errors, repo)
            locked_stable = normalise_scopes(row_values(row, "Stable Read Scope"), "lock stable read scope", errors, repo)
            if any_scope_overlap(plan["write_scope"], locked_write + locked_stable):
                errors.append(f"{plan_id}: write scope conflicts with active lock held by {row.get('Workstream')}")
            if any_scope_overlap(plan["stable_read_scope"], locked_write):
                errors.append(f"{plan_id}: stable read conflicts with active writer {row.get('Workstream')}")
            locked_contracts = set(row_values(row, "Contract IDs"))
            for contract in sorted(
                (set(plan["contracts_changed"]) | set(plan["contracts_consumed"])) & locked_contracts
            ):
                errors.append(f"{plan_id}: contract locked by {row.get('Workstream')}: {contract}")
            locked_resources = set(row_values(row, "Mutable Resources"))
            for resource in sorted(set(plan["mutable_resources"]) & locked_resources):
                errors.append(f"{plan_id}: mutable resource locked by {row.get('Workstream')}: {resource}")

    if errors:
        return fail(errors)
    print("PASS")
    print("plans=" + ",".join(plan_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
