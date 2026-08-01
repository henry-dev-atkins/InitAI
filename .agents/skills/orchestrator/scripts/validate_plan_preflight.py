#!/usr/bin/env python3
"""Validate a workflow plan before full plan review."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Identity and Traceability",
    "Work Classification",
    "Mission",
    "Scope and Contracts",
    "Protected Invariants / Must Not",
    "Command Manifest",
    "Implementation Steps",
    "Validation and Resolution Evidence",
    "Risks and Assumptions",
    "Result Packet Contract",
    "Executive Summary",
    "Am I going in Circles?",
    "Is there a more elegant way of doing this?",
]

VALID_WORK_TYPES = {
    "CAPABILITY.RESEARCH",
    "CAPABILITY.PRODUCT",
    "EVIDENCE.VALIDATION",
    "FIX.ALIGNMENT",
    "DEPENDENCY.LOCAL",
    "TEMPORARY.DIAGNOSTIC",
    "ENVIRONMENT.ADAPTATION",
    "WORKAROUND.QUARANTINED",
    "FLUFF.DISPOSABLE",
    "DOCS.MEMORY",
    "AGENT.WORKFLOW",
    "CLEANUP.HYGIENE",
    "SPEC.EDIT",
}


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def extract_json_block(text: str, heading: str) -> object:
    start = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not start:
        raise ValueError(f"missing section: {heading}")
    after = text[start.end() :]
    match = re.search(r"```json\s*(.*?)\s*```", after, re.DOTALL)
    if not match:
        raise ValueError(f"missing fenced json block in {heading}")
    return json.loads(match.group(1))


def repo_path(repo: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        resolved = path.resolve()
    else:
        resolved = (repo / path).resolve()
    repo_resolved = repo.resolve()
    try:
        resolved.relative_to(repo_resolved)
    except ValueError as exc:
        raise ValueError(f"path escapes repository: {value}") from exc
    return resolved


def has_placeholder(value: str) -> bool:
    return bool(re.search(r"(\{[^{}\n]+\}|<[^<>\n]+>|\$\{\{[^}]+\}\})", value))


def malformed_path(value: str) -> bool:
    return bool(re.search(r"[\x00-\x1f]", value)) or has_placeholder(value)


def validate_temp_root(value: str | None, errors: list[str]) -> None:
    if value is None:
        return
    if malformed_path(value):
        errors.append(f"malformed temp root: {value}")
    normalized = value.replace("\\", "/").lstrip("./")
    if not normalized.startswith("temp/"):
        errors.append(f"temp root must be repo-local temp/: {value}")


def command_words(command: dict) -> list[str]:
    if "argv" in command:
        return [str(part) for part in command["argv"]]
    if "shell" in command:
        return re.split(r"\s+", str(command["shell"]).strip())
    return []


def validate_inline_python(command: dict, errors: list[str]) -> None:
    words = command_words(command)
    for index, word in enumerate(words[:-1]):
        if word == "-c" and index > 0 and "python" in words[index - 1].lower():
            try:
                ast.parse(words[index + 1])
            except SyntaxError as exc:
                errors.append(f"{command.get('id')}: inline Python does not compile: {exc.msg}")


def validate_pytest_basetemp(command: dict, errors: list[str]) -> None:
    words = command_words(command)
    if not any("pytest" in word.lower() for word in words):
        return
    basetemp = None
    for index, word in enumerate(words):
        if word == "--basetemp" and index + 1 < len(words):
            basetemp = words[index + 1]
        elif word.startswith("--basetemp="):
            basetemp = word.split("=", 1)[1]
    if not basetemp:
        errors.append(f"{command.get('id')}: pytest command must declare --basetemp under temp/")
        return
    validate_temp_root(basetemp, errors)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--workstream")
    parser.add_argument("--plan-id")
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    plan_path = repo_path(repo, str(args.plan))
    if not plan_path.exists():
        return fail([f"plan does not exist: {args.plan}"])

    text = plan_path.read_text(encoding="utf-8")
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"missing required section: {section}")

    if args.workstream and f"Workstream ID: {args.workstream}" not in text:
        errors.append(f"workstream ID does not match expected {args.workstream}")
    if args.plan_id and f"Plan ID: {args.plan_id}" not in text:
        errors.append(f"plan ID does not match expected {args.plan_id}")

    type_match = re.search(r"Primary Work Type:\s*`?([A-Z.]+)`?", text)
    if not type_match:
        errors.append("missing Primary Work Type")
    elif type_match.group(1) not in VALID_WORK_TYPES:
        errors.append(f"invalid Primary Work Type: {type_match.group(1)}")

    non_template = "template" not in plan_path.name.lower()
    if non_template and has_placeholder(text):
        errors.append("unresolved placeholder outside template")

    try:
        manifest = extract_json_block(text, "Command Manifest")
    except (ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        manifest = None

    command_ids: list[str] = []
    if isinstance(manifest, dict):
        if manifest.get("schema") != "plan-command-manifest.v1":
            errors.append("command manifest schema must be plan-command-manifest.v1")
        commands = manifest.get("commands")
        if not isinstance(commands, list) or not commands:
            errors.append("command manifest must contain at least one command")
            commands = []
        for command in commands:
            if not isinstance(command, dict):
                errors.append("command entry must be an object")
                continue
            command_id = command.get("id")
            if not isinstance(command_id, str) or not re.match(r"^CMD[0-9]{3}$", command_id):
                errors.append(f"invalid command id: {command_id}")
            else:
                command_ids.append(command_id)
            if ("argv" in command) == ("shell" in command):
                errors.append(f"{command_id}: command must declare exactly one of argv or shell")
            for key in ["cwd", "purpose", "phase", "expected_status", "evidence_target"]:
                if not command.get(key):
                    errors.append(f"{command_id}: missing {key}")
            if command.get("phase") not in {"pre-edit", "implementation-validation", "final-validation", "diagnostic"}:
                errors.append(f"{command_id}: invalid phase")
            if command.get("expected_status") not in {"pass", "fail"}:
                errors.append(f"{command_id}: invalid expected_status")
            for key in ["cwd", "temp_root"]:
                value = command.get(key)
                if isinstance(value, str) and malformed_path(value):
                    errors.append(f"{command_id}: malformed {key}: {value}")
            try:
                repo_path(repo, str(command.get("cwd", ".")))
            except ValueError as exc:
                errors.append(f"{command_id}: {exc}")
            validate_temp_root(command.get("temp_root"), errors)
            validate_pytest_basetemp(command, errors)
            validate_inline_python(command, errors)
            for required in command.get("requires_existing_paths", []) or []:
                try:
                    required_path = repo_path(repo, required)
                except ValueError as exc:
                    errors.append(f"{command_id}: {exc}")
                    continue
                if not required_path.exists():
                    errors.append(f"{command_id}: required path does not exist: {required}")

    duplicates = sorted({item for item in command_ids if command_ids.count(item) > 1})
    for duplicate in duplicates:
        errors.append(f"duplicate command id: {duplicate}")
    for command_id in command_ids:
        if command_id not in text.split("## Validation and Resolution Evidence", 1)[-1]:
            errors.append(f"command id not referenced by validation evidence: {command_id}")

    if errors:
        return fail(errors)

    print("PASS")
    print(f"validated_plan={plan_path}")
    print("validated_command_ids=" + ",".join(command_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
