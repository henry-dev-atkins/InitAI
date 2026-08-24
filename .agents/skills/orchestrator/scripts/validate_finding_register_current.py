#!/usr/bin/env python3
"""Validate the canonical JSON finding register."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import load_json


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def waiver_expired(value: str | None) -> bool:
    if not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return parsed < datetime.now(timezone.utc)


def validate_register(register: Path, schema_path: Path | None = None) -> list[str]:
    chosen_schema = schema_path or Path(__file__).resolve().parents[1] / "assets/finding-register-current.schema.json"
    try:
        data = load_json(register)
        schema = load_json(chosen_schema)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    errors = validate_schema(data, schema)
    findings = data.get("findings", []) if isinstance(data, dict) else []
    ids: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        finding_id = finding.get("id", "unknown")
        ids.append(str(finding_id))
        status = finding.get("status")
        resolved_by = finding.get("resolved_by")
        closed_at = finding.get("closed_at")
        if status == "RESOLVED" and (not resolved_by or not closed_at):
            errors.append(f"{finding_id}: RESOLVED requires resolved_by and closed_at")
        if status != "RESOLVED" and (resolved_by is not None or closed_at is not None):
            errors.append(f"{finding_id}: non-resolved finding may not have closure fields")
        waiver = finding.get("waiver")
        if waiver and not isinstance(waiver, dict):
            errors.append(f"{finding_id}: waiver must be an object or null")
        elif waiver:
            if status not in {"DEFERRED_BY_HUMAN", "RESOLVED"}:
                errors.append(f"{finding_id}: waiver is allowed only for deferred or resolved findings")
            if waiver_expired(waiver.get("expires_at")):
                errors.append(f"{finding_id}: waiver expiry is invalid or in the past")
    for duplicate in sorted({item for item in ids if ids.count(item) > 1}):
        errors.append(f"duplicate finding id: {duplicate}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    parser.add_argument("--schema", type=Path)
    args = parser.parse_args()

    errors = validate_register(args.register, args.schema)
    if errors:
        return fail(errors)
    data = load_json(args.register)
    print("PASS")
    print("findings=" + ",".join(item["id"] for item in data.get("findings", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
