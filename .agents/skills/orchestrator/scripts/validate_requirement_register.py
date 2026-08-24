#!/usr/bin/env python3
"""Validate the hash-bound atomic requirement register against AI_SPACE/SPEC.md."""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import file_sha256, load_json, repo_path


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def range_hash(lines: list[str], start: int, end: int) -> str:
    payload = "".join(lines[start - 1 : end]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def waiver_valid(waiver: dict | None) -> bool:
    if not waiver:
        return False
    expires = waiver.get("expires_at")
    if not expires:
        return True
    try:
        parsed = datetime.fromisoformat(str(expires).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return False
    if parsed.tzinfo is None:
        return False
    return parsed >= datetime.now(timezone.utc)


def validate_register(register_path: Path, repo: Path, terminal: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        data = load_json(register_path)
        schema = load_json(repo / ".agents/skills/orchestrator/assets/requirement-register.schema.json")
    except (OSError, ValueError) as exc:
        return [str(exc)]
    errors.extend(validate_schema(data, schema))
    if errors:
        return errors

    try:
        spec_path = repo_path(repo, data["spec_path"])
    except ValueError as exc:
        return [str(exc)]
    if not spec_path.is_file():
        return [f"spec does not exist: {data['spec_path']}"]
    if file_sha256(spec_path) != data["spec_sha256"]:
        errors.append("spec_sha256 does not match AI_SPACE/SPEC.md")

    spec_text = spec_path.read_text(encoding="utf-8")
    lines = spec_text.splitlines(keepends=True)
    if spec_text and not lines:
        lines = [spec_text]
    if data["line_count"] != len(lines):
        errors.append(f"line_count must be {len(lines)}")

    requirements = data["requirements"]
    requirement_ids = [item["id"] for item in requirements]
    for duplicate in sorted({item for item in requirement_ids if requirement_ids.count(item) > 1}):
        errors.append(f"duplicate requirement id: {duplicate}")
    requirement_map = {item["id"]: item for item in requirements}

    expected_line = 1
    covered_requirements: set[str] = set()
    for item in sorted(data["coverage"], key=lambda value: value["start_line"]):
        start = item["start_line"]
        end = item["end_line"]
        if start != expected_line:
            errors.append(f"coverage gap or overlap before line {start}; expected line {expected_line}")
        if end < start:
            errors.append(f"coverage range ends before it starts: {start}-{end}")
        if end > len(lines):
            errors.append(f"coverage range exceeds spec line count: {start}-{end}")
        if item["classification"] == "REQUIREMENT" and not item["requirement_ids"]:
            errors.append(f"requirement coverage range {start}-{end} has no requirement_ids")
        if item["classification"] == "NON_NORMATIVE" and item["requirement_ids"]:
            errors.append(f"non-normative coverage range {start}-{end} may not name requirement_ids")
        for requirement_id in item["requirement_ids"]:
            if requirement_id not in requirement_map:
                errors.append(f"coverage references unknown requirement: {requirement_id}")
            covered_requirements.add(requirement_id)
        expected_line = end + 1
    if expected_line != len(lines) + 1:
        errors.append(f"coverage stops at line {expected_line - 1}; spec ends at line {len(lines)}")

    coverage_lines_by_requirement: dict[str, set[int]] = {item: set() for item in requirement_ids}
    for item in data["coverage"]:
        for requirement_id in item["requirement_ids"]:
            if requirement_id in coverage_lines_by_requirement:
                coverage_lines_by_requirement[requirement_id].update(
                    range(item["start_line"], item["end_line"] + 1)
                )

    for requirement in requirements:
        requirement_id = requirement["id"]
        start = requirement["spec_start_line"]
        end = requirement["spec_end_line"]
        if requirement_id not in covered_requirements:
            errors.append(f"requirement is not referenced by coverage: {requirement_id}")
        if start > end or start < 1 or end > len(lines):
            errors.append(f"{requirement_id}: invalid spec line range {start}-{end}")
        else:
            expected_lines = set(range(start, end + 1))
            if coverage_lines_by_requirement.get(requirement_id, set()) != expected_lines:
                errors.append(
                    f"{requirement_id}: coverage lines must exactly match its declared spec range {start}-{end}"
                )
            if range_hash(lines, start, end) != requirement["text_sha256"]:
                errors.append(f"{requirement_id}: text_sha256 does not match its spec line range")
        if terminal:
            has_evidence = bool(requirement["implementation_evidence"]) and bool(requirement["validation_evidence"])
            if not has_evidence and not waiver_valid(requirement.get("waiver")):
                errors.append(f"{requirement_id}: missing implementation/validation evidence and no valid waiver")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--terminal", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    try:
        register_path = repo_path(repo, str(args.register))
    except ValueError as exc:
        return fail([str(exc)])
    errors = validate_register(register_path, repo, args.terminal)
    if errors:
        return fail(errors)
    data = load_json(register_path)
    print("PASS")
    print(f"requirements={len(data['requirements'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
