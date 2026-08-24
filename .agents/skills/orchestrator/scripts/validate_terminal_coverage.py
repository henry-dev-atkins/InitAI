#!/usr/bin/env python3
"""Validate exhaustive requirement coverage and one frozen terminal tree."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_validation import validate as validate_schema
from validate_evidence_ledger import validate_ledger
from validate_finding_register_current import validate_register as validate_findings
from validate_requirement_register import validate_register as validate_requirements
from workflow_common import (
    diff_inventories,
    file_sha256,
    inventory_tree_hash,
    load_json,
    parse_markdown_table,
    repo_path,
    repository_inventory,
    repository_tree_hash,
)

EXPECTED_LENSES = {
    "requirement_coverage",
    "behavioural_correctness",
    "files_config_outputs",
    "extra_prohibited_logic",
    "validation_edge_cases",
    "holistic_integration_minimality",
}
TERMINAL_WORKSTREAM_STATES = {"ACCEPTED", "CANCELLED", "SUPERSEDED"}


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    try:
        record_path = repo_path(repo, str(args.record))
        record = load_json(record_path)
        schema = load_json(repo / ".agents/skills/orchestrator/assets/terminal-review.schema.json")
    except (OSError, ValueError) as exc:
        return fail([str(exc)])

    errors = validate_schema(record, schema)
    if errors:
        return fail(errors)

    current_hash = repository_tree_hash(repo)
    if record["tree_hash"] != current_hash:
        errors.append("terminal tree_hash does not match the current active repository tree")

    try:
        campaign_baseline_path = repo_path(repo, record["campaign_baseline_path"])
        requirement_path = repo_path(repo, record["requirement_register_path"])
        finding_path = repo_path(repo, record["finding_register_path"])
        workstream_path = repo_path(repo, record["workstream_register_path"])
        global_ledger_path = repo_path(repo, record["global_validation_ledger_path"])
    except ValueError as exc:
        return fail([str(exc)])

    authority_errors: list[str] = []
    authority_errors.extend(validate_requirements(requirement_path, repo, terminal=True))
    authority_errors.extend(f"finding register: {item}" for item in validate_findings(finding_path))
    authority_errors.extend(f"global validation: {item}" for item in validate_ledger(global_ledger_path, repo))
    errors.extend(authority_errors)
    if authority_errors:
        return fail(errors)

    requirements = load_json(requirement_path).get("requirements", []) if requirement_path.exists() else []
    requirement_ids = {item["id"] for item in requirements}

    findings = load_json(finding_path).get("findings", []) if finding_path.exists() else []
    for finding in findings:
        status = finding.get("status")
        if status == "RESOLVED":
            continue
        if status == "DEFERRED_BY_HUMAN" and finding.get("waiver"):
            continue
        errors.append(f"{finding.get('id', 'unknown')}: terminal finding status is {status}")

    workstream_rows: list[dict[str, str]] = []
    if not workstream_path.is_file():
        errors.append(f"missing workstream register: {record['workstream_register_path']}")
    else:
        headers, workstream_rows = parse_markdown_table(workstream_path)
        required_headers = {"Workstream", "Plan", "Accepted State", "State"}
        missing_headers = sorted(required_headers - set(headers))
        if missing_headers:
            errors.append(f"workstream register missing terminal columns: {missing_headers}")
        for row in workstream_rows:
            state = row.get("State", "")
            if state not in TERMINAL_WORKSTREAM_STATES:
                errors.append(f"{row.get('Workstream', 'unknown')}: terminal workstream state is {state}")

    reviewers = record["reviewers"]
    if len(reviewers) != 6:
        errors.append("terminal review requires exactly six reviewers")
    review_ids = [item["review_id"] for item in reviewers]
    if len(review_ids) != len(set(review_ids)):
        errors.append("terminal reviewer IDs must be unique")
    lenses = {item["lens"] for item in reviewers}
    if lenses != EXPECTED_LENSES:
        errors.append("terminal reviewers must use the six required distinct lenses")

    assigned: set[str] = set()
    for reviewer in reviewers:
        if reviewer["tree_hash"] != record["tree_hash"]:
            errors.append(f"{reviewer['review_id']}: reviewed a different tree hash")
        unknown = set(reviewer["assigned_requirement_ids"]) - requirement_ids
        if unknown:
            errors.append(f"{reviewer['review_id']}: unknown requirement IDs: {sorted(unknown)}")
        assigned.update(reviewer["assigned_requirement_ids"])
        if reviewer["verdict"] == "PASS" and reviewer["findings"]:
            errors.append(f"{reviewer['review_id']}: PASS reviewer may not have findings")
        if reviewer["verdict"] == "FINDINGS" and not reviewer["findings"]:
            errors.append(f"{reviewer['review_id']}: FINDINGS requires findings")
    if assigned != requirement_ids:
        errors.append(
            "terminal reviewer assignment does not cover all requirements; "
            f"missing={sorted(requirement_ids - assigned)}"
        )

    global_ledger = load_json(global_ledger_path) if global_ledger_path.exists() else {}
    if global_ledger.get("status") != "PASS":
        errors.append("global validation ledger must have PASS status")
    if global_ledger.get("repository_tree_hash_before") != record["tree_hash"]:
        errors.append("global validation did not start on the terminal tree hash")
    if global_ledger.get("repository_tree_hash_after") != record["tree_hash"]:
        errors.append("global validation changed the terminal tree")

    current_inventory = repository_inventory(repo)
    accepted_schema = load_json(
        repo / ".agents/skills/orchestrator/assets/accepted-workstream-state.schema.json"
    )
    campaign_schema = load_json(
        repo / ".agents/skills/orchestrator/assets/campaign-baseline.schema.json"
    )
    accepted_states: dict[str, dict] = {}
    accepted_order: list[tuple[datetime, str, dict]] = []

    if not campaign_baseline_path.is_file():
        errors.append(f"missing campaign baseline: {record['campaign_baseline_path']}")
        campaign_baseline = {}
    else:
        try:
            campaign_baseline = load_json(campaign_baseline_path)
        except (OSError, ValueError) as exc:
            errors.append(f"invalid campaign baseline: {exc}")
            campaign_baseline = {}
    campaign_errors = validate_schema(campaign_baseline, campaign_schema)
    errors.extend(f"campaign baseline: {item}" for item in campaign_errors)
    baseline_inventory = (
        campaign_baseline.get("inventory", {})
        if isinstance(campaign_baseline, dict) and not campaign_errors
        else {}
    )
    if baseline_inventory and inventory_tree_hash(baseline_inventory) != campaign_baseline.get("tree_hash"):
        errors.append("campaign baseline tree_hash does not match its recorded inventory")

    for row in workstream_rows:
        if row.get("State") != "ACCEPTED":
            continue
        workstream_id = row.get("Workstream", "unknown")
        accepted_reference = row.get("Accepted State", "")
        if not accepted_reference or accepted_reference.lower() in {"none", "null", "-"}:
            errors.append(f"{workstream_id}: ACCEPTED workstream has no Accepted State path")
            continue
        try:
            accepted_path = repo_path(repo, accepted_reference)
        except ValueError as exc:
            errors.append(f"{workstream_id}: {exc}")
            continue
        if not accepted_path.is_file():
            errors.append(f"{workstream_id}: missing accepted state: {accepted_reference}")
            continue
        accepted_key = accepted_path.relative_to(repo).as_posix()
        try:
            accepted_state = load_json(accepted_path)
        except (OSError, ValueError) as exc:
            errors.append(f"{workstream_id}: invalid accepted state: {exc}")
            continue
        accepted_errors = validate_schema(accepted_state, accepted_schema)
        errors.extend(f"{workstream_id}: accepted state: {item}" for item in accepted_errors)
        if accepted_errors:
            continue
        if accepted_state.get("workstream_id") != workstream_id:
            errors.append(f"{workstream_id}: accepted-state workstream ID mismatch")
        if accepted_state.get("plan_id") != row.get("Plan"):
            errors.append(f"{workstream_id}: accepted-state plan ID mismatch")
        if row.get("Scope Diff") not in {"", "none", "null", "-", accepted_state.get("scope_diff_path")}:
            errors.append(f"{workstream_id}: scope-diff register path mismatch")
        if row.get("Accepted Tree Hash") not in {"", "none", "null", "-", accepted_state.get("accepted_tree_hash")}:
            errors.append(f"{workstream_id}: accepted-tree register hash mismatch")
        changed_paths = accepted_state.get("workstream_changes", [])
        accepted_inventory = accepted_state.get("accepted_path_inventory", {})
        if set(changed_paths) != set(accepted_inventory):
            errors.append(f"{workstream_id}: accepted_path_inventory must cover exactly workstream_changes")
        try:
            scope_diff_path = repo_path(repo, accepted_state.get("scope_diff_path", ""))
        except ValueError as exc:
            errors.append(f"{workstream_id}: {exc}")
            continue
        if not scope_diff_path.is_file():
            errors.append(f"{workstream_id}: accepted-state scope diff is missing")
        elif file_sha256(scope_diff_path) != accepted_state.get("scope_diff_sha256"):
            errors.append(f"{workstream_id}: accepted-state scope diff hash mismatch")
        if accepted_key in accepted_states:
            errors.append(f"duplicate accepted-state path in workstream register: {accepted_key}")
        accepted_states[accepted_key] = accepted_state
        accepted_at_raw = str(accepted_state.get("accepted_at", ""))
        try:
            accepted_at = datetime.fromisoformat(accepted_at_raw.replace("Z", "+00:00"))
            if accepted_at.tzinfo is None:
                raise ValueError("timezone is required")
            accepted_at = accepted_at.astimezone(timezone.utc)
        except ValueError:
            errors.append(f"{workstream_id}: accepted_at must be an ISO-8601 timestamp with timezone")
            accepted_at = datetime.min.replace(tzinfo=timezone.utc)
        accepted_order.append((accepted_at, accepted_key, accepted_state))

    campaign_diff = diff_inventories(baseline_inventory, current_inventory) if baseline_inventory else {"added": [], "deleted": [], "modified": []}
    final_changed_paths = set(campaign_diff["added"] + campaign_diff["deleted"] + campaign_diff["modified"])
    accepted_changed_paths = {
        path
        for _, _, accepted_state in accepted_order
        for path in accepted_state.get("workstream_changes", [])
    }
    for path in sorted(final_changed_paths - accepted_changed_paths):
        errors.append(f"unowned campaign mutation: {path}")

    latest_expected: dict[str, tuple[str, object, str]] = {}
    for accepted_at, accepted_key, accepted_state in sorted(accepted_order):
        for path, expected in accepted_state.get("accepted_path_inventory", {}).items():
            latest_expected[path] = (accepted_at, expected, accepted_key)
    for path, (_, expected, accepted_key) in latest_expected.items():
        if current_inventory.get(path) != expected:
            errors.append(f"accepted path changed after its latest accepted state: {path} ({accepted_key})")

    for requirement in requirements:
        requirement_id = requirement["id"]
        if requirement.get("waiver"):
            continue
        for evidence in requirement.get("implementation_evidence", []):
            try:
                accepted_path = repo_path(repo, evidence["accepted_state_path"])
            except ValueError as exc:
                errors.append(f"{requirement_id}: {exc}")
                continue
            accepted_key = accepted_path.relative_to(repo).as_posix()
            accepted_state = accepted_states.get(accepted_key)
            if accepted_state is None:
                errors.append(
                    f"{requirement_id}: implementation evidence is not an ACCEPTED workstream state: {accepted_key}"
                )
                continue
            if accepted_state.get("workstream_id") != evidence.get("workstream_id"):
                errors.append(f"{requirement_id}: accepted-state workstream does not match evidence")
            if accepted_state.get("plan_id") != evidence.get("plan_id"):
                errors.append(f"{requirement_id}: accepted-state plan does not match evidence")
        for evidence in requirement.get("validation_evidence", []):
            try:
                ledger_path = repo_path(repo, evidence["ledger_path"])
            except ValueError as exc:
                errors.append(f"{requirement_id}: {exc}")
                continue
            ledger_errors = validate_ledger(ledger_path, repo)
            errors.extend(f"{requirement_id}: {item}" for item in ledger_errors)
            if ledger_path.exists():
                command_status = {
                    item["id"]: item["status"] for item in load_json(ledger_path).get("commands", [])
                }
                for command_id in evidence["command_ids"]:
                    if command_status.get(command_id) != "PASS":
                        errors.append(f"{requirement_id}: validation command is not PASS: {command_id}")

    all_pass = all(item["verdict"] == "PASS" for item in reviewers)
    expected_status = "PASS" if all_pass and not errors else "FINDINGS"
    if record["status"] != expected_status:
        errors.append(f"terminal status must be {expected_status}")
    if record["status"] != "PASS":
        errors.append("terminal completion requires status PASS")

    if errors:
        return fail(errors)
    print("PASS")
    print(f"tree_hash={record['tree_hash']}")
    print(f"requirements={len(requirement_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
