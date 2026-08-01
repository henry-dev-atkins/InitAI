#!/usr/bin/env python3
"""Validate a structured current finding register."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VALID_STATES = {"OPEN", "ASSIGNED", "RESOLVED", "DEFERRED_BY_HUMAN", "BLOCKED"}
VALID_SEVERITIES = {"critical", "high", "medium", "low"}


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    args = parser.parse_args()

    try:
        data = json.loads(args.register.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail([str(exc)])

    errors: list[str] = []
    if not isinstance(data, dict):
        return fail(["register root must be an object"])
    if data.get("schema") != "finding-register-current.v1":
        errors.append("schema must be finding-register-current.v1")
    findings = data.get("findings")
    if not isinstance(findings, list):
        return fail(["findings must be an array"])

    ids: list[str] = []
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not re.match(r"^F[0-9]{3}$", finding_id):
            errors.append(f"invalid finding id: {finding_id}")
        else:
            ids.append(finding_id)
        for key in ["owner", "spec_authority", "problem", "repo_evidence", "resolution_evidence"]:
            if not isinstance(finding.get(key), str) or not finding.get(key).strip():
                errors.append(f"{finding_id}: missing {key}")
        status = finding.get("status")
        severity = finding.get("severity")
        if status not in VALID_STATES:
            errors.append(f"{finding_id}: invalid status: {status}")
        if severity not in VALID_SEVERITIES:
            errors.append(f"{finding_id}: invalid severity: {severity}")
        has_closure = bool(finding.get("resolved_by") or finding.get("closed_at"))
        if status == "RESOLVED" and not finding.get("resolved_by"):
            errors.append(f"{finding_id}: RESOLVED requires resolved_by")
        if status != "RESOLVED" and has_closure:
            errors.append(f"{finding_id}: non-resolved finding has closure fields")

    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"duplicate finding id: {duplicate}")

    if errors:
        return fail(errors)

    print("PASS")
    print("findings=" + ",".join(ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
