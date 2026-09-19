#!/usr/bin/env python3
"""Execute a reviewed argv-only command manifest and write the evidence ledger."""

from __future__ import annotations

import argparse
import platform
import subprocess
import sys
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import (
    file_sha256,
    load_json,
    path_sha256,
    repo_path,
    repository_tree_hash,
    utc_now,
    write_json,
)


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def relative_to_repo(repo: Path, path: Path) -> str:
    return path.resolve().relative_to(repo.resolve()).as_posix()


def schema_path_for(repo: Path, manifest: dict) -> Path:
    schema = manifest.get("schema")
    names = {
        "plan-command-manifest.v1": "plan-command-manifest.schema.json",
        "global-validation-manifest.v1": "global-validation-manifest.schema.json",
    }
    if schema not in names:
        raise ValueError(f"unsupported manifest schema: {schema}")
    return repo / ".agents/skills/orchestrator/assets" / names[schema]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--workstream", required=True)
    parser.add_argument("--plan-id", required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    try:
        manifest_path = repo_path(repo, str(args.manifest))
        ledger_path = repo_path(repo, str(args.ledger))
        manifest = load_json(manifest_path)
        schema = load_json(schema_path_for(repo, manifest))
    except (OSError, ValueError) as exc:
        return fail([str(exc)])

    schema_errors = validate_schema(manifest, schema)
    if schema_errors:
        return fail(schema_errors)
    if manifest["schema"] == "plan-command-manifest.v1":
        if manifest["workstream_id"] != args.workstream or manifest["plan_id"] != args.plan_id:
            return fail(["runner WS/plan identifiers do not match the reviewed plan manifest"])
    elif manifest["manifest_id"] != args.plan_id or args.workstream != "GLOBAL":
        return fail(["runner identifiers do not match the reviewed global validation manifest"])

    manifest_hash = file_sha256(manifest_path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    log_dir = ledger_path.parent / "command_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    tree_before_all = repository_tree_hash(repo)
    command_records: list[dict] = []
    first_failed: str | None = None

    for command in manifest["commands"]:
        command_id = command["id"]
        stdout_path = log_dir / f"{command_id}.stdout.txt"
        stderr_path = log_dir / f"{command_id}.stderr.txt"
        command_tree_before = repository_tree_hash(repo)

        if first_failed is not None:
            stdout_path.write_bytes(b"")
            stderr_path.write_bytes(b"")
            command_records.append(
                {
                    "id": command_id,
                    "argv": command["argv"],
                    "cwd": command["cwd"],
                    "expected_status": command["expected_status"],
                    "timeout_seconds": command["timeout_seconds"],
                    "timed_out": False,
                    "requirement_ids": command["requirement_ids"],
                    "finding_ids": command["finding_ids"],
                    "started_at": None,
                    "finished_at": None,
                    "exit_code": None,
                    "status": "NOT_RUN",
                    "tree_hash_before": command_tree_before,
                    "tree_hash_after": command_tree_before,
                    "stdout_path": relative_to_repo(repo, stdout_path),
                    "stdout_sha256": file_sha256(stdout_path),
                    "stderr_path": relative_to_repo(repo, stderr_path),
                    "stderr_sha256": file_sha256(stderr_path),
                    "summary": "Not run because an earlier gate failed.",
                    "artefacts": [],
                }
            )
            continue

        prerequisite_errors: list[str] = []
        try:
            cwd = repo_path(repo, command["cwd"])
        except ValueError as exc:
            prerequisite_errors.append(str(exc))
            cwd = repo
        for required in command.get("requires_existing_paths", []) or []:
            try:
                required_path = repo_path(repo, required)
            except ValueError as exc:
                prerequisite_errors.append(str(exc))
                continue
            if not required_path.exists():
                prerequisite_errors.append(f"required path does not exist: {required}")

        started_at = utc_now()
        timed_out = False
        if prerequisite_errors:
            exit_code = 125
            stdout = b""
            stderr = ("\n".join(prerequisite_errors) + "\n").encode("utf-8")
        else:
            try:
                completed = subprocess.run(
                    command["argv"],
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    timeout=command["timeout_seconds"],
                )
                exit_code = int(completed.returncode)
                stdout = completed.stdout
                stderr = completed.stderr
            except subprocess.TimeoutExpired:
                timed_out = True
                exit_code = 124
                stdout = b""
                stderr = (
                    f"Command timed out after {command['timeout_seconds']} seconds.\n"
                ).encode("utf-8")
            except OSError as exc:
                exit_code = 126
                stdout = b""
                stderr = (str(exc) + "\n").encode("utf-8")
        finished_at = utc_now()
        stdout_path.write_bytes(stdout)
        stderr_path.write_bytes(stderr)

        expected_pass = command["expected_status"] == "pass"
        gate_passed = (
            not timed_out
            and ((exit_code == 0) if expected_pass else (exit_code != 0))
        )
        status = "PASS" if gate_passed else "FAIL"
        if status == "FAIL" and first_failed is None:
            first_failed = command_id

        artefacts: list[dict[str, str]] = []
        artefact_errors: list[str] = []
        for value in command.get("artefact_paths", []) or []:
            try:
                artefact_path = repo_path(repo, value)
            except ValueError as exc:
                artefact_errors.append(str(exc))
                continue
            if not artefact_path.exists():
                artefact_errors.append(f"required artefact does not exist: {value}")
                continue
            artefacts.append({"path": value, "sha256": path_sha256(artefact_path)})
        if artefact_errors and status == "PASS":
            status = "FAIL"
            if first_failed is None:
                first_failed = command_id
            with stderr_path.open("ab") as handle:
                handle.write(("\n".join(artefact_errors) + "\n").encode("utf-8"))

        command_records.append(
            {
                "id": command_id,
                "argv": command["argv"],
                "cwd": command["cwd"],
                "expected_status": command["expected_status"],
                "timeout_seconds": command["timeout_seconds"],
                "timed_out": timed_out,
                "requirement_ids": command["requirement_ids"],
                "finding_ids": command["finding_ids"],
                "started_at": started_at,
                "finished_at": finished_at,
                "exit_code": exit_code,
                "status": status,
                "tree_hash_before": command_tree_before,
                "tree_hash_after": repository_tree_hash(repo),
                "stdout_path": relative_to_repo(repo, stdout_path),
                "stdout_sha256": file_sha256(stdout_path),
                "stderr_path": relative_to_repo(repo, stderr_path),
                "stderr_sha256": file_sha256(stderr_path),
                "summary": f"exit_code={exit_code}; expected_status={command['expected_status']}",
                "artefacts": artefacts,
            }
        )

    ledger = {
        "schema": "evidence-ledger.v1",
        "workstream_id": args.workstream,
        "plan_id": args.plan_id,
        "manifest_path": relative_to_repo(repo, manifest_path),
        "manifest_sha256": manifest_hash,
        "status": "FAIL" if first_failed else "PASS",
        "first_failed_gate": first_failed,
        "repository_tree_hash_before": tree_before_all,
        "repository_tree_hash_after": repository_tree_hash(repo),
        "runner": {
            "name": "run_command_manifest.py",
            "version": "1",
            "sha256": file_sha256(Path(__file__).resolve()),
        },
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.splitlines()[0],
            "repo_root": str(repo),
        },
        "commands": command_records,
    }
    write_json(ledger_path, ledger)
    print(ledger["status"])
    print(f"ledger={relative_to_repo(repo, ledger_path)}")
    return 0 if ledger["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
