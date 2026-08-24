#!/usr/bin/env python3
"""Mechanical preflight for one authorised workstream plan and its manifest."""

from __future__ import annotations

import argparse
import ast
import re
import shlex
import sys
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import (
    any_scope_overlap,
    file_sha256,
    load_json,
    normalise_repo_relative,
    parse_bullet_section,
    repo_path,
)

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
    "CAPABILITY.RESEARCH", "CAPABILITY.PRODUCT", "EVIDENCE.VALIDATION", "FIX.ALIGNMENT",
    "DEPENDENCY.LOCAL", "TEMPORARY.DIAGNOSTIC", "ENVIRONMENT.ADAPTATION",
    "WORKAROUND.QUARANTINED", "FLUFF.DISPOSABLE", "DOCS.MEMORY", "AGENT.WORKFLOW",
    "CLEANUP.HYGIENE", "SPEC.EDIT",
}


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def has_placeholder(value: str) -> bool:
    return bool(re.search(r"(\{[^{}\n]+\}|<[^<>\n]+>|\$\{\{[^}]+\}\})", value))


def extract_field(text: str, label: str) -> str | None:
    match = re.search(rf"^-\s*{re.escape(label)}:\s*`?([^`\n]+)`?\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def parse_validation_table(text: str) -> list[dict[str, str]]:
    body = section_body(text, "Validation and Resolution Evidence")
    lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        return []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def split_ids(value: str) -> list[str]:
    if not value or value.lower() in {"none", "-"}:
        return []
    return [item.strip("` ") for item in re.split(r"[\s,]+", value) if item.strip("` ")]


def command_words(command: dict) -> list[str]:
    return [str(part) for part in command.get("argv", [])]


def validate_inline_python(command: dict, errors: list[str]) -> None:
    words = command_words(command)
    for index, word in enumerate(words[:-1]):
        if word == "-c" and index > 0 and "python" in words[index - 1].lower():
            try:
                ast.parse(words[index + 1])
            except SyntaxError as exc:
                errors.append(f"{command.get('id')}: inline Python does not compile: {exc.msg}")


def validate_temp_root(value: str | None, errors: list[str], command_id: str) -> None:
    if value is None:
        return
    try:
        normalised = normalise_repo_relative(value)
    except ValueError as exc:
        errors.append(f"{command_id}: {exc}")
        return
    if not normalised.startswith("temp/"):
        errors.append(f"{command_id}: temp root must be under repo-local temp/: {value}")


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
    else:
        validate_temp_root(basetemp, errors, str(command.get("id")))


def normalised_set(values: list[str], label: str, errors: list[str], repo: Path) -> set[str]:
    result: set[str] = set()
    for value in values:
        try:
            normalised = repo_path(repo, value).relative_to(repo).as_posix()
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if normalised == ".":
            errors.append(f"{label}: repository root is too broad")
        if normalised in result:
            errors.append(f"{label}: duplicate scope: {normalised}")
        result.add(normalised)
    return result


def compare_exact(
    label: str,
    actual: list[str],
    expected: list[str],
    errors: list[str],
    *,
    repo: Path,
    paths: bool = False,
) -> None:
    if paths:
        actual_set = normalised_set(actual, label, errors, repo)
        expected_set = normalised_set(expected, f"expected {label}", errors, repo)
    else:
        actual_set = set(actual)
        expected_set = set(expected)
    if actual_set != expected_set:
        errors.append(f"{label} does not match authority: actual={sorted(actual_set)} expected={sorted(expected_set)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--parent-session", type=Path)
    parser.add_argument("--workstream", required=True)
    parser.add_argument("--plan-id", required=True)
    parser.add_argument("--expected-finding", action="append", default=[])
    parser.add_argument("--expected-requirement", action="append", default=[])
    parser.add_argument("--allowed-write-scope", action="append", default=[])
    parser.add_argument("--stable-read-scope", action="append", default=[])
    parser.add_argument("--off-limits-scope", action="append", default=[])
    parser.add_argument("--contract-changed", action="append", default=[])
    parser.add_argument("--contract-consumed", action="append", default=[])
    parser.add_argument("--mutable-resource", action="append", default=[])
    parser.add_argument("--dependency", action="append", default=[])
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    errors: list[str] = []
    try:
        plan_path = repo_path(repo, str(args.plan))
        manifest_path = repo_path(repo, str(args.manifest))
    except ValueError as exc:
        return fail([str(exc)])
    if not plan_path.is_file():
        return fail([f"plan does not exist: {args.plan}"])
    if not manifest_path.is_file():
        return fail([f"manifest does not exist: {args.manifest}"])
    if args.parent_session:
        try:
            session_path = repo_path(repo, str(args.parent_session))
            if not session_path.is_dir():
                errors.append(f"parent session does not exist: {args.parent_session}")
        except ValueError as exc:
            errors.append(str(exc))

    text = plan_path.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, re.MULTILINE):
            errors.append(f"missing required section: {section}")
    if "template" not in plan_path.name.lower() and has_placeholder(text):
        errors.append("unresolved placeholder outside template")

    identity_expectations = {
        "Workstream ID": args.workstream,
        "Plan ID": args.plan_id,
    }
    for label, expected in identity_expectations.items():
        if extract_field(text, label) != expected:
            errors.append(f"{label} does not match expected {expected}")
    findings = split_ids(extract_field(text, "Source findings") or "")
    requirements = split_ids(extract_field(text, "Requirement IDs") or "")
    predecessor = (extract_field(text, "Predecessor plan") or "none").strip()
    failed_assumption = (extract_field(text, "Failed assumption from predecessor") or "none").strip()
    causal_delta = (extract_field(text, "Material causal delta") or "none").strip()
    if predecessor.lower() not in {"none", "null", "-"}:
        if not re.fullmatch(r"P[0-9]{3,}", predecessor):
            errors.append(f"invalid predecessor plan ID: {predecessor}")
        if failed_assumption.lower() in {"none", "null", "-"}:
            errors.append("successor plan requires Failed assumption from predecessor")
        if causal_delta.lower() in {"none", "null", "-"}:
            errors.append("successor plan requires Material causal delta")
    compare_exact("source findings", findings, args.expected_finding, errors, repo=repo)
    compare_exact("requirement IDs", requirements, args.expected_requirement, errors, repo=repo)

    workflow_class = extract_field(text, "Workflow class")
    if workflow_class not in {"SMALL", "STANDARD", "CAMPAIGN"}:
        errors.append(f"invalid Workflow class: {workflow_class}")

    type_match = re.search(r"Primary Work Type:\s*`?([A-Z.]+)`?", text)
    if not type_match:
        errors.append("missing Primary Work Type")
    elif type_match.group(1) not in VALID_WORK_TYPES:
        errors.append(f"invalid Primary Work Type: {type_match.group(1)}")

    write_scope = parse_bullet_section(text, "Write scope")
    stable_reads = parse_bullet_section(text, "Stable read assumptions")
    off_limits = parse_bullet_section(text, "Off-limits")
    contracts_changed = parse_bullet_section(text, "Contracts changed")
    contracts_consumed = parse_bullet_section(text, "Contracts consumed")
    mutable_resources = parse_bullet_section(text, "Mutable resources")
    dependencies = parse_bullet_section(text, "Dependencies")
    compare_exact("write scope", write_scope, args.allowed_write_scope, errors, repo=repo, paths=True)
    compare_exact("stable read scope", stable_reads, args.stable_read_scope, errors, repo=repo, paths=True)
    compare_exact("off-limits scope", off_limits, args.off_limits_scope, errors, repo=repo, paths=True)
    compare_exact("contracts changed", contracts_changed, args.contract_changed, errors, repo=repo)
    compare_exact("contracts consumed", contracts_consumed, args.contract_consumed, errors, repo=repo)
    compare_exact("mutable resources", mutable_resources, args.mutable_resource, errors, repo=repo)
    compare_exact("dependencies", dependencies, args.dependency, errors, repo=repo)
    canonical_write_scope = normalised_set(write_scope, "write scope", errors, repo)
    canonical_stable_reads = normalised_set(stable_reads, "stable read scope", errors, repo)
    canonical_off_limits = normalised_set(off_limits, "off-limits scope", errors, repo)
    ordered_write_scope = sorted(canonical_write_scope)
    for index, left in enumerate(ordered_write_scope):
        for right in ordered_write_scope[index + 1 :]:
            if any_scope_overlap([left], [right]):
                errors.append(f"overlapping write scopes: {left} <-> {right}")
    for left, right in any_scope_overlap(canonical_write_scope, canonical_stable_reads):
        errors.append(f"write scope overlaps a stable read assumption: {left} <-> {right}")
    for left, right in any_scope_overlap(canonical_write_scope, canonical_off_limits):
        errors.append(f"write scope overlaps off-limits scope: {left} <-> {right}")
    for finding in findings:
        if not re.fullmatch(r"F[0-9]{3,}", finding):
            errors.append(f"invalid finding ID: {finding}")
    for requirement in requirements:
        if not re.fullmatch(r"REQ[0-9]{3,}", requirement):
            errors.append(f"invalid requirement ID: {requirement}")
    for dependency in dependencies:
        if not re.fullmatch(r"WS[0-9]{3,}", dependency):
            errors.append(f"invalid dependency ID: {dependency}")
    for contract in contracts_changed + contracts_consumed:
        if not re.fullmatch(r"CON[0-9]{3,}", contract):
            errors.append(f"invalid contract ID: {contract}")

    manifest_section = section_body(text, "Command Manifest")
    manifest_ref = extract_field(manifest_section, "Path")
    manifest_hash = extract_field(manifest_section, "SHA-256")
    expected_manifest_ref = manifest_path.relative_to(repo).as_posix()
    if manifest_ref != expected_manifest_ref:
        errors.append(f"Command Manifest Path must be {expected_manifest_ref}")
    actual_manifest_hash = file_sha256(manifest_path)
    if manifest_hash != actual_manifest_hash:
        errors.append("Command Manifest SHA-256 does not match the manifest file")

    try:
        manifest = load_json(manifest_path)
        schema = load_json(repo / ".agents/skills/orchestrator/assets/plan-command-manifest.schema.json")
        manifest_errors = validate_schema(manifest, schema)
        errors.extend(manifest_errors)
        if manifest_errors and not isinstance(manifest.get("commands"), list):
            manifest["commands"] = []
        if manifest.get("workstream_id") != args.workstream:
            errors.append("command manifest workstream_id does not match plan authority")
        if manifest.get("plan_id") != args.plan_id:
            errors.append("command manifest plan_id does not match plan authority")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        manifest = {"commands": []}

    command_ids: list[str] = []
    all_command_requirements: set[str] = set()
    all_command_findings: set[str] = set()
    for command in manifest.get("commands", []):
        command_id = str(command.get("id"))
        command_ids.append(command_id)
        all_command_requirements.update(command.get("requirement_ids", []))
        all_command_findings.update(command.get("finding_ids", []))
        try:
            cwd_path = repo_path(repo, command.get("cwd", "."))
            if not cwd_path.is_dir():
                errors.append(f"{command_id}: cwd is not an existing directory: {command.get('cwd')}")
        except ValueError as exc:
            errors.append(f"{command_id}: {exc}")
        validate_temp_root(command.get("temp_root"), errors, command_id)
        validate_pytest_basetemp(command, errors)
        validate_inline_python(command, errors)
        for artefact in command.get("artefact_paths", []) or []:
            try:
                repo_path(repo, artefact)
            except ValueError as exc:
                errors.append(f"{command_id}: artefact path: {exc}")
        for required in command.get("requires_existing_paths", []) or []:
            try:
                required_path = repo_path(repo, required)
            except ValueError as exc:
                errors.append(f"{command_id}: {exc}")
                continue
            if not required_path.exists():
                errors.append(f"{command_id}: required path does not exist: {required}")
        for argument in command.get("argv", []):
            if has_placeholder(str(argument)):
                errors.append(f"{command_id}: argv contains unresolved placeholder")
    for duplicate in sorted({item for item in command_ids if command_ids.count(item) > 1}):
        errors.append(f"duplicate command id: {duplicate}")
    if set(requirements) - all_command_requirements:
        errors.append(f"requirements lack command evidence: {sorted(set(requirements) - all_command_requirements)}")
    if all_command_requirements - set(requirements):
        errors.append(f"commands reference unauthorised requirements: {sorted(all_command_requirements - set(requirements))}")
    if set(findings) - all_command_findings:
        errors.append(f"findings lack command evidence: {sorted(set(findings) - all_command_findings)}")
    if all_command_findings - set(findings):
        errors.append(f"commands reference unauthorised findings: {sorted(all_command_findings - set(findings))}")

    rows = parse_validation_table(text)
    if not rows:
        errors.append("Validation and Resolution Evidence must contain the structured command table")
    table_ids: list[str] = []
    for row in rows:
        command_id = row.get("Command ID", "").strip("` ")
        table_ids.append(command_id)
        if command_id not in command_ids:
            errors.append(f"validation table references unknown command: {command_id}")
        manifest_command = next((item for item in manifest.get("commands", []) if item.get("id") == command_id), None)
        if manifest_command:
            if set(split_ids(row.get("Requirement IDs", ""))) != set(manifest_command.get("requirement_ids", [])):
                errors.append(f"{command_id}: validation-table requirement IDs do not match manifest")
            if set(split_ids(row.get("Finding IDs", ""))) != set(manifest_command.get("finding_ids", [])):
                errors.append(f"{command_id}: validation-table finding IDs do not match manifest")
            if not row.get("Proof", "").strip():
                errors.append(f"{command_id}: validation table requires a proof statement")
    if table_ids != command_ids:
        errors.append("validation table command order/set must exactly match the manifest")

    if errors:
        return fail(errors)
    print("PASS")
    print(f"validated_plan={plan_path}")
    print("validated_command_ids=" + ",".join(command_ids))
    return 0


if __name__ == "__main__":
    sys.exit(main())
