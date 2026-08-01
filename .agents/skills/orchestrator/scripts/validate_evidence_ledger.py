#!/usr/bin/env python3
"""Validate a structured implementation evidence ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def bad_text(value: str) -> bool:
    return bool(re.search(r"[\x00-\x1f{}<>]", value))


def repo_path(repo: Path, value: str) -> Path:
    if bad_text(value):
        raise ValueError(f"malformed path: {value}")
    path = Path(value)
    resolved = path.resolve() if path.is_absolute() else (repo / path).resolve()
    try:
        resolved.relative_to(repo.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {value}") from exc
    return resolved


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail([str(exc)])

    errors: list[str] = []
    if not isinstance(data, dict):
        return fail(["ledger root must be an object"])
    if data.get("schema") != "evidence-ledger.v1":
        errors.append("schema must be evidence-ledger.v1")
    for key, pattern in {"workstream_id": r"^WS[0-9]{3}$", "plan_id": r"^P[0-9]{3}$"}.items():
        value = data.get(key)
        if not isinstance(value, str) or not re.match(pattern, value):
            errors.append(f"invalid {key}: {value}")

    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("commands must be a non-empty array")
        commands = []

    failed_ids: list[str] = []
    seen_ids: list[str] = []
    for command in commands:
        if not isinstance(command, dict):
            errors.append("command entry must be an object")
            continue
        command_id = command.get("id")
        if not isinstance(command_id, str) or not re.match(r"^CMD[0-9]{3}$", command_id):
            errors.append(f"invalid command id: {command_id}")
        else:
            seen_ids.append(command_id)
        argv = command.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
            errors.append(f"{command_id}: argv must be a non-empty string array")
        elif any(bad_text(item) for item in argv):
            errors.append(f"{command_id}: argv contains control characters or unresolved placeholders")
        cwd = command.get("cwd")
        if not isinstance(cwd, str) or not cwd:
            errors.append(f"{command_id}: cwd is required")
        else:
            try:
                repo_path(repo, cwd)
            except ValueError as exc:
                errors.append(f"{command_id}: {exc}")
        exit_code = command.get("exit_code")
        status = command.get("status")
        if not isinstance(exit_code, int):
            errors.append(f"{command_id}: exit_code must be an integer")
        if status not in {"PASS", "FAIL", "NOT_RUN"}:
            errors.append(f"{command_id}: invalid status")
        if status == "PASS" and exit_code != 0:
            errors.append(f"{command_id}: PASS requires exit_code 0")
        if status == "FAIL" and exit_code == 0:
            errors.append(f"{command_id}: FAIL requires non-zero exit_code")
        if status == "FAIL" and isinstance(command_id, str):
            failed_ids.append(command_id)
        for artefact in command.get("artefacts", []) or []:
            if not isinstance(artefact, dict) or not isinstance(artefact.get("path"), str):
                errors.append(f"{command_id}: artefact must contain path")
                continue
            try:
                artefact_path = repo_path(repo, artefact["path"])
            except ValueError as exc:
                errors.append(f"{command_id}: {exc}")
                continue
            recorded_hash = artefact.get("sha256")
            if recorded_hash is not None and not re.match(r"^[a-fA-F0-9]{64}$", str(recorded_hash)):
                errors.append(f"{command_id}: malformed sha256 for {artefact['path']}")
            if artefact_path.exists() and recorded_hash:
                actual = sha256(artefact_path)
                if actual.lower() != str(recorded_hash).lower():
                    errors.append(f"{command_id}: sha256 mismatch for {artefact['path']}")

    for duplicate in sorted({item for item in seen_ids if seen_ids.count(item) > 1}):
        errors.append(f"duplicate command id: {duplicate}")

    first_failed = data.get("first_failed_gate")
    if failed_ids and first_failed not in failed_ids:
        errors.append("first_failed_gate must name the first failing command when any command fails")
    if not failed_ids and first_failed not in {None, ""}:
        errors.append("first_failed_gate must be null or empty when no command failed")

    if errors:
        return fail(errors)

    print("PASS")
    print("commands=" + ",".join(seen_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
