#!/usr/bin/env python3
"""Validate a runner-produced evidence ledger against its reviewed manifest."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import file_sha256, load_json, path_sha256, repo_path


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def manifest_schema_path(repo: Path, manifest: dict) -> Path:
    names = {
        "plan-command-manifest.v1": "plan-command-manifest.schema.json",
        "global-validation-manifest.v1": "global-validation-manifest.schema.json",
    }
    name = names.get(manifest.get("schema"))
    if name is None:
        raise ValueError(f"unsupported manifest schema: {manifest.get('schema')}")
    return repo / ".agents/skills/orchestrator/assets" / name


def validate_ledger(ledger_path: Path, repo: Path, explicit_manifest: Path | None = None) -> list[str]:
    errors: list[str] = []
    try:
        data = load_json(ledger_path)
        ledger_schema = load_json(repo / ".agents/skills/orchestrator/assets/evidence-ledger.schema.json")
    except (OSError, ValueError) as exc:
        return [str(exc)]
    errors.extend(validate_schema(data, ledger_schema))
    if errors:
        return errors
    runner_path = Path(__file__).resolve().with_name("run_command_manifest.py")
    if file_sha256(runner_path) != data["runner"]["sha256"]:
        errors.append("runner.sha256 does not match run_command_manifest.py")

    try:
        declared_manifest_path = repo_path(repo, data["manifest_path"])
        manifest_path = explicit_manifest or declared_manifest_path
        if explicit_manifest is not None and explicit_manifest.resolve() != declared_manifest_path.resolve():
            errors.append("explicit manifest path differs from ledger manifest_path")
        manifest = load_json(manifest_path)
        manifest_schema = load_json(manifest_schema_path(repo, manifest))
    except (OSError, ValueError) as exc:
        return [str(exc)]

    manifest_errors = validate_schema(manifest, manifest_schema)
    errors.extend(manifest_errors)
    if manifest_errors:
        return errors
    if file_sha256(manifest_path) != data["manifest_sha256"]:
        errors.append("manifest_sha256 does not match the reviewed manifest")

    manifest_commands = manifest.get("commands", [])
    ledger_commands = data.get("commands", [])
    if len(manifest_commands) != len(ledger_commands):
        errors.append("ledger command count does not match manifest command count")

    failed_ids: list[str] = []
    previous_tree_after: str | None = None
    seen_failure = False
    for index, manifest_command in enumerate(manifest_commands):
        if index >= len(ledger_commands):
            break
        record = ledger_commands[index]
        for key in ["id", "argv", "cwd", "expected_status", "timeout_seconds", "requirement_ids", "finding_ids"]:
            if record.get(key) != manifest_command.get(key):
                errors.append(f"{record.get('id', index)}: {key} does not match manifest")
        status = record.get("status")
        exit_code = record.get("exit_code")
        timed_out = record.get("timed_out")
        expected = manifest_command.get("expected_status")
        started_at = record.get("started_at")
        finished_at = record.get("finished_at")
        if index == 0 and record.get("tree_hash_before") != data.get("repository_tree_hash_before"):
            errors.append(f"{record.get('id')}: first command tree does not match repository_tree_hash_before")
        if previous_tree_after is not None and record.get("tree_hash_before") != previous_tree_after:
            errors.append(f"{record.get('id')}: command tree chain is discontinuous")
        previous_tree_after = record.get("tree_hash_after")
        if status in {"PASS", "FAIL"}:
            if not started_at or not finished_at:
                errors.append(f"{record.get('id')}: executed command requires start and finish timestamps")
            else:
                try:
                    if datetime.fromisoformat(finished_at.replace("Z", "+00:00")) < datetime.fromisoformat(started_at.replace("Z", "+00:00")):
                        errors.append(f"{record.get('id')}: finished_at precedes started_at")
                except ValueError:
                    errors.append(f"{record.get('id')}: timestamps are not ISO-8601")
        elif started_at is not None or finished_at is not None:
            errors.append(f"{record.get('id')}: NOT_RUN timestamps must be null")
        if status in {"PASS", "FAIL"} and exit_code is None:
            errors.append(f"{record.get('id')}: executed command requires an exit code")
        if timed_out and (status != "FAIL" or exit_code != 124):
            errors.append(f"{record.get('id')}: timeout must be a failed gate with exit code 124")
        if timed_out and status == "PASS":
            errors.append(f"{record.get('id')}: timed out command cannot pass")
        if status == "PASS":
            if expected == "pass" and exit_code != 0:
                errors.append(f"{record.get('id')}: expected pass but exit code was non-zero")
            elif expected == "fail" and exit_code == 0:
                errors.append(f"{record.get('id')}: expected failure but exit code was zero")
        if status == "FAIL":
            failed_ids.append(str(record.get("id")))
            seen_failure = True
        if status == "NOT_RUN":
            if exit_code is not None:
                errors.append(f"{record.get('id')}: NOT_RUN requires null exit_code")
            if not seen_failure:
                errors.append(f"{record.get('id')}: NOT_RUN is allowed only after a failed gate")

        for path_key, hash_key in [
            ("stdout_path", "stdout_sha256"),
            ("stderr_path", "stderr_sha256"),
        ]:
            try:
                output_path = repo_path(repo, str(record.get(path_key, "")))
            except ValueError as exc:
                errors.append(f"{record.get('id')}: {exc}")
                continue
            if not output_path.is_file():
                errors.append(f"{record.get('id')}: missing {path_key}: {record.get(path_key)}")
            elif file_sha256(output_path) != record.get(hash_key):
                errors.append(f"{record.get('id')}: {hash_key} mismatch")

        declared = list(manifest_command.get("artefact_paths", []) or [])
        recorded = record.get("artefacts", []) or []
        recorded_paths = [item.get("path") for item in recorded]
        if status == "NOT_RUN":
            if recorded:
                errors.append(f"{record.get('id')}: NOT_RUN command may not record artefacts")
        elif status == "PASS" and recorded_paths != declared:
            errors.append(f"{record.get('id')}: PASS artefacts do not exactly match manifest artefact_paths")
        elif status == "FAIL":
            undeclared = [item for item in recorded_paths if item not in declared]
            if undeclared or len(recorded_paths) != len(set(recorded_paths)):
                errors.append(f"{record.get('id')}: FAIL artefacts must be a unique subset of manifest artefact_paths")
            exit_matched = (expected == "pass" and exit_code == 0) or (expected == "fail" and exit_code != 0)
            if exit_matched and recorded_paths == declared:
                errors.append(f"{record.get('id')}: FAIL is inconsistent with the exit result and complete artefacts")
        for artefact in recorded:
            try:
                artefact_path = repo_path(repo, artefact["path"])
            except ValueError as exc:
                errors.append(f"{record.get('id')}: {exc}")
                continue
            if not artefact_path.exists():
                errors.append(f"{record.get('id')}: missing artefact: {artefact['path']}")
            elif path_sha256(artefact_path) != artefact["sha256"]:
                errors.append(f"{record.get('id')}: artefact hash mismatch: {artefact['path']}")

    if ledger_commands and ledger_commands[-1].get("tree_hash_after") != data.get("repository_tree_hash_after"):
        errors.append("last command tree does not match repository_tree_hash_after")

    first_failed = data.get("first_failed_gate")
    expected_first = failed_ids[0] if failed_ids else None
    if first_failed != expected_first:
        errors.append(f"first_failed_gate must be {expected_first!r}")
    expected_status = "FAIL" if failed_ids else "PASS"
    if data.get("status") != expected_status:
        errors.append(f"root status must be {expected_status}")
    if failed_ids:
        first_index = next((i for i, item in enumerate(ledger_commands) if item.get("status") == "FAIL"), -1)
        for item in ledger_commands[first_index + 1 :]:
            if item.get("status") != "NOT_RUN":
                errors.append("commands after the first failed gate must be NOT_RUN")
                break

    workstream_id = str(data.get("workstream_id", ""))
    plan_id = str(data.get("plan_id", ""))
    if workstream_id != "GLOBAL" and not re.fullmatch(r"WS[0-9]{3,}", workstream_id):
        errors.append(f"invalid workstream_id: {workstream_id}")
    if not (re.fullmatch(r"P[0-9]{3,}", plan_id) or re.fullmatch(r"GVM[0-9]{3,}", plan_id)):
        errors.append(f"invalid plan_id: {plan_id}")
    manifest_kind = manifest.get("schema")
    if manifest_kind == "global-validation-manifest.v1":
        if workstream_id != "GLOBAL" or plan_id != manifest.get("manifest_id"):
            errors.append("global validation ledger identifiers must match the GVM manifest")
    if manifest_kind == "plan-command-manifest.v1":
        if workstream_id != manifest.get("workstream_id") or plan_id != manifest.get("plan_id"):
            errors.append("plan evidence ledger identifiers must match the reviewed plan manifest")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    try:
        ledger_path = repo_path(repo, str(args.ledger))
        explicit_manifest = repo_path(repo, str(args.manifest)) if args.manifest else None
    except ValueError as exc:
        return fail([str(exc)])
    errors = validate_ledger(ledger_path, repo, explicit_manifest)
    if errors:
        return fail(errors)
    data = load_json(ledger_path)
    print("PASS")
    print("commands=" + ",".join(item["id"] for item in data["commands"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
