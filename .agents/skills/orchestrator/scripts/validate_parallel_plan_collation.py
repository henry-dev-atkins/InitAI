#!/usr/bin/env python3
"""Validate parallel plan portfolio collation input."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import PurePosixPath, Path


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


def normalise_scope(path: str) -> str:
    value = path.replace("\\", "/").strip().strip("/")
    if not value or re.search(r"[\x00-\x1f{}<>]", value):
        raise ValueError(f"malformed write scope: {path}")
    if PurePosixPath(value).is_absolute() or value.startswith("../"):
        raise ValueError(f"write scope escapes repository: {path}")
    return value


def overlaps(left: str, right: str) -> bool:
    left = normalise_scope(left)
    right = normalise_scope(right)
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--required-finding", action="append", default=[])
    args = parser.parse_args()

    try:
        data = load_json_or_fenced(args.portfolio)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail([str(exc)])

    errors: list[str] = []
    if not isinstance(data, dict):
        return fail(["portfolio root must be an object"])
    plans = data.get("plans")
    if not isinstance(plans, list) or not plans:
        return fail(["portfolio must contain a non-empty plans array"])

    plan_ids: list[str] = []
    workstream_ids: list[str] = []
    covered_findings: set[str] = set()

    for index, plan in enumerate(plans):
        if not isinstance(plan, dict):
            errors.append(f"plans[{index}] is not an object")
            continue
        plan_id = plan.get("plan_id")
        workstream_id = plan.get("workstream_id")
        if not isinstance(plan_id, str) or not re.match(r"^P[0-9]{3}$", plan_id):
            errors.append(f"invalid plan_id: {plan_id}")
        else:
            plan_ids.append(plan_id)
        if not isinstance(workstream_id, str) or not re.match(r"^WS[0-9]{3}$", workstream_id):
            errors.append(f"{plan_id}: invalid workstream_id: {workstream_id}")
        else:
            workstream_ids.append(workstream_id)
        findings = plan.get("findings", [])
        if not isinstance(findings, list) or not findings:
            errors.append(f"{plan_id}: findings must be a non-empty array")
        else:
            covered_findings.update(str(item) for item in findings)
        for key in ["write_scope", "contracts_changed", "contracts_consumed", "dependencies"]:
            if key not in plan or not isinstance(plan[key], list):
                errors.append(f"{plan_id}: {key} must be an array")

    for duplicate in sorted({item for item in plan_ids if plan_ids.count(item) > 1}):
        errors.append(f"duplicate plan_id: {duplicate}")
    for duplicate in sorted({item for item in workstream_ids if workstream_ids.count(item) > 1}):
        errors.append(f"duplicate workstream_id: {duplicate}")
    for finding in args.required_finding:
        if finding not in covered_findings:
            errors.append(f"required finding not covered: {finding}")

    for i, left in enumerate(plans):
        if not isinstance(left, dict):
            continue
        for right in plans[i + 1 :]:
            if not isinstance(right, dict):
                continue
            left_id = left.get("plan_id", f"plans[{i}]")
            right_id = right.get("plan_id", "unknown")
            for left_scope in left.get("write_scope", []) or []:
                for right_scope in right.get("write_scope", []) or []:
                    try:
                        if overlaps(str(left_scope), str(right_scope)):
                            errors.append(f"write scope overlap: {left_id} {left_scope} <-> {right_id} {right_scope}")
                    except ValueError as exc:
                        errors.append(str(exc))
            left_changed = set(left.get("contracts_changed", []) or [])
            left_consumed = set(left.get("contracts_consumed", []) or [])
            right_changed = set(right.get("contracts_changed", []) or [])
            right_consumed = set(right.get("contracts_consumed", []) or [])
            for contract in sorted((left_changed & right_consumed) | (right_changed & left_consumed)):
                errors.append(f"contract conflict: {left_id} <-> {right_id}: {contract}")
            left_ws = left.get("workstream_id")
            right_ws = right.get("workstream_id")
            if right_ws in (left.get("dependencies", []) or []):
                errors.append(f"dependency conflict in same batch: {left_id} depends on {right_ws}")
            if left_ws in (right.get("dependencies", []) or []):
                errors.append(f"dependency conflict in same batch: {right_id} depends on {left_ws}")

    if errors:
        return fail(errors)

    print("PASS")
    print("plans=" + ",".join(plan_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
