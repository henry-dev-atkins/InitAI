#!/usr/bin/env python3
"""Create, compare, accept and restore one shared-checkout workstream snapshot."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path

from workflow_common import (
    any_scope_overlap,
    diff_inventories,
    path_within_scopes,
    repo_path,
    repository_inventory,
    repository_tree_hash,
    utc_now,
    write_json,
    load_json,
)


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def copy_entry(source: Path, destination: Path) -> str:
    if source.is_symlink():
        raise ValueError(f"write scope root may not be a symlink: {source}")
    if source.is_file():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return "file"
    if source.is_dir():
        symlinks = [path for path in source.rglob("*") if path.is_symlink()]
        if symlinks:
            raise ValueError(f"write scope may not contain symlinks: {symlinks[0]}")
        shutil.copytree(source, destination, symlinks=False)
        return "directory"
    return "missing"


def load_snapshot(snapshot_dir: Path) -> dict:
    return load_json(snapshot_dir / "snapshot_manifest.json")


def inventory_within_scopes(inventory: dict[str, dict[str, str]], scopes: list[str]) -> dict[str, dict[str, str]]:
    return {path: value for path, value in inventory.items() if path_within_scopes(path, scopes)}


def current_diff(repo: Path, snapshot: dict) -> dict:
    after = repository_inventory(repo)
    diff = diff_inventories(snapshot["repository_inventory_before"], after)
    changed = sorted(diff["added"] + diff["deleted"] + diff["modified"])
    own = [path for path in changed if path_within_scopes(path, snapshot["write_scopes"])]
    concurrent = [
        path
        for path in changed
        if not path_within_scopes(path, snapshot["write_scopes"])
        and path_within_scopes(path, snapshot["concurrent_write_scopes"])
    ]
    violations = [path for path in changed if path not in own and path not in concurrent]
    stable_invalidations = [
        path for path in changed if path_within_scopes(path, snapshot["stable_read_scopes"])
    ]
    return {
        "schema": "workstream-scope-diff.v1",
        "workstream_id": snapshot["workstream_id"],
        "plan_id": snapshot["plan_id"],
        "snapshot_created_at": snapshot["created_at"],
        "checked_at": utc_now(),
        "tree_hash_before": snapshot["tree_hash_before"],
        "tree_hash_after": repository_tree_hash(repo),
        "write_scopes": snapshot["write_scopes"],
        "concurrent_write_scopes": snapshot["concurrent_write_scopes"],
        "stable_read_scopes": snapshot["stable_read_scopes"],
        "added": diff["added"],
        "deleted": diff["deleted"],
        "modified": diff["modified"],
        "workstream_changes": own,
        "concurrent_changes": concurrent,
        "scope_violations": violations,
        "stable_read_invalidations": stable_invalidations,
        "status": "PASS" if not violations and not stable_invalidations else "FAIL",
    }


def create(args: argparse.Namespace, repo: Path) -> int:
    snapshot_dir = repo_path(repo, str(args.snapshot_dir))
    snapshot_relative = snapshot_dir.relative_to(repo).as_posix()
    if not snapshot_relative.startswith("AI_SPACE/sessions/"):
        return fail(["snapshot directory must be under AI_SPACE/sessions/"])
    if snapshot_dir.exists() and any(snapshot_dir.iterdir()):
        return fail([f"snapshot directory is not empty: {args.snapshot_dir}"])
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    def canonical(values: list[str]) -> list[str]:
        return [repo_path(repo, value).relative_to(repo).as_posix() for value in values]

    try:
        write_scopes = canonical(args.scope)
        stable_reads = canonical(args.stable_read)
        concurrent = canonical(args.concurrent_scope)
    except ValueError as exc:
        return fail([str(exc)])
    if not write_scopes:
        return fail(["at least one --scope is required"])
    if "." in write_scopes + stable_reads + concurrent:
        return fail(["repository root is too broad for workstream scope control"])
    for values, label in [
        (write_scopes, "write scope"),
        (stable_reads, "stable read scope"),
        (concurrent, "concurrent write scope"),
    ]:
        duplicates = sorted({item for item in values if values.count(item) > 1})
        if duplicates:
            return fail([f"duplicate {label}: {item}" for item in duplicates])
        nested = [
            (left, right)
            for index, left in enumerate(values)
            for right in values[index + 1 :]
            if any_scope_overlap([left], [right])
        ]
        if nested:
            return fail([f"overlapping {label}: {left} <-> {right}" for left, right in nested])
    conflicts = any_scope_overlap(write_scopes, stable_reads)
    if conflicts:
        return fail([f"write/stable-read overlap: {left} <-> {right}" for left, right in conflicts])
    conflicts = any_scope_overlap(write_scopes, concurrent)
    if conflicts:
        return fail([f"write/concurrent-scope overlap: {left} <-> {right}" for left, right in conflicts])
    missing_stable_reads = [value for value in stable_reads if not repo_path(repo, value).exists()]
    if missing_stable_reads:
        return fail([f"stable read scope does not exist: {value}" for value in missing_stable_reads])

    entries: list[dict] = []
    data_root = snapshot_dir / "data"
    for index, value in enumerate(write_scopes):
        source = repo_path(repo, value)
        destination = data_root / f"scope_{index:03d}"
        try:
            kind = copy_entry(source, destination)
        except ValueError as exc:
            return fail([str(exc)])
        entries.append(
            {
                "scope": value,
                "kind": kind,
                "snapshot_path": destination.relative_to(snapshot_dir).as_posix() if kind != "missing" else None,
            }
        )

    manifest = {
        "schema": "workstream-snapshot.v1",
        "workstream_id": args.workstream,
        "plan_id": args.plan_id,
        "created_at": utc_now(),
        "tree_hash_before": repository_tree_hash(repo),
        "write_scopes": write_scopes,
        "stable_read_scopes": stable_reads,
        "concurrent_write_scopes": concurrent,
        "scope_entries": entries,
        "repository_inventory_before": repository_inventory(repo),
    }
    write_json(snapshot_dir / "snapshot_manifest.json", manifest)
    print("PASS")
    print(f"snapshot={snapshot_dir.relative_to(repo).as_posix()}")
    return 0


def diff(args: argparse.Namespace, repo: Path) -> int:
    snapshot_dir = repo_path(repo, str(args.snapshot_dir))
    try:
        snapshot = load_snapshot(snapshot_dir)
    except (OSError, ValueError) as exc:
        return fail([str(exc)])
    report = current_diff(repo, snapshot)
    output = repo_path(repo, str(args.output)) if args.output else snapshot_dir / "scope_diff.json"
    write_json(output, report)
    print(report["status"])
    print(f"diff={output.relative_to(repo).as_posix()}")
    return 0 if report["status"] == "PASS" else 1


def archive_destination(root: Path, relative: str) -> Path:
    destination = root / relative
    if not destination.exists():
        return destination
    suffix = utc_now().replace(":", "").replace("-", "")
    return destination.with_name(destination.name + "__" + suffix)


def restore(args: argparse.Namespace, repo: Path) -> int:
    snapshot_dir = repo_path(repo, str(args.snapshot_dir))
    archive_root = repo_path(repo, str(args.archive_root))
    archive_relative = archive_root.relative_to(repo).as_posix()
    if not archive_relative.startswith("AI_SPACE/archive/rejected/"):
        return fail(["rejected implementation archive must be under AI_SPACE/archive/rejected/"])
    try:
        snapshot = load_snapshot(snapshot_dir)
    except (OSError, ValueError) as exc:
        return fail([str(exc)])

    archive_root.mkdir(parents=True, exist_ok=True)
    archived: list[str] = []
    restored: list[str] = []
    for entry in snapshot["scope_entries"]:
        relative = entry["scope"]
        current = repo_path(repo, relative)
        if current.exists() or current.is_symlink():
            destination = archive_destination(archive_root, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(current), str(destination))
            archived.append(destination.relative_to(repo).as_posix())
        if entry["kind"] != "missing":
            source = snapshot_dir / entry["snapshot_path"]
            current.parent.mkdir(parents=True, exist_ok=True)
            if entry["kind"] == "file":
                shutil.copy2(source, current)
            elif entry["kind"] == "directory":
                shutil.copytree(source, current, symlinks=True)
            restored.append(relative)

    after_inventory = repository_inventory(repo)
    expected_scope_inventory = inventory_within_scopes(
        snapshot["repository_inventory_before"], snapshot["write_scopes"]
    )
    actual_scope_inventory = inventory_within_scopes(after_inventory, snapshot["write_scopes"])
    restoration_errors: list[str] = []
    if expected_scope_inventory != actual_scope_inventory:
        restoration_errors.append("restored write scopes do not match the baseline inventory")

    report = {
        "schema": "workstream-restore.v1",
        "workstream_id": snapshot["workstream_id"],
        "plan_id": snapshot["plan_id"],
        "restored_at": utc_now(),
        "archived_rejected_paths": archived,
        "restored_scopes": restored,
        "tree_hash_after_restore": repository_tree_hash(repo),
        "restoration_errors": restoration_errors,
        "status": "PASS" if not restoration_errors else "FAIL",
    }
    output = repo_path(repo, str(args.output)) if args.output else snapshot_dir / "restore_report.json"
    write_json(output, report)
    print(report["status"])
    print(f"restore_report={output.relative_to(repo).as_posix()}")
    return 0 if report["status"] == "PASS" else 1


def accept(args: argparse.Namespace, repo: Path) -> int:
    snapshot_dir = repo_path(repo, str(args.snapshot_dir))
    try:
        snapshot = load_snapshot(snapshot_dir)
    except (OSError, ValueError) as exc:
        return fail([str(exc)])
    report = current_diff(repo, snapshot)
    scope_diff_path = repo_path(repo, str(args.scope_diff_path))
    if not scope_diff_path.is_file():
        return fail([f"scope diff does not exist: {args.scope_diff_path}"])
    try:
        recorded_diff = load_json(scope_diff_path)
    except (OSError, ValueError) as exc:
        return fail([str(exc)])
    for key in ("workstream_id", "plan_id", "tree_hash_before", "tree_hash_after", "workstream_changes", "scope_violations", "stable_read_invalidations", "status"):
        if recorded_diff.get(key) != report.get(key):
            return fail([f"scope diff is stale or inconsistent at {key}"])
    if report["status"] != "PASS":
        return fail(
            [
                "scope diff is not acceptable",
                *[f"scope violation: {item}" for item in report["scope_violations"]],
                *[f"stable read invalidated: {item}" for item in report["stable_read_invalidations"]],
            ]
        )
    output = repo_path(repo, str(args.output))
    accepted_inventory = repository_inventory(repo)
    accepted = {
        "schema": "accepted-workstream-state.v1",
        "workstream_id": snapshot["workstream_id"],
        "plan_id": snapshot["plan_id"],
        "accepted_at": utc_now(),
        "baseline_tree_hash": snapshot["tree_hash_before"],
        "accepted_tree_hash": report["tree_hash_after"],
        "scope_diff_path": scope_diff_path.relative_to(repo).as_posix(),
        "scope_diff_sha256": hashlib.sha256(scope_diff_path.read_bytes()).hexdigest(),
        "workstream_changes": report["workstream_changes"],
        "accepted_path_inventory": {
            path: accepted_inventory.get(path) for path in report["workstream_changes"]
        },
        "status": "ACCEPTED",
    }
    write_json(output, accepted)
    print("PASS")
    print(f"accepted_state={output.relative_to(repo).as_posix()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    subparsers = parser.add_subparsers(dest="action", required=True)

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--snapshot-dir", type=Path, required=True)
    create_parser.add_argument("--workstream", required=True)
    create_parser.add_argument("--plan-id", required=True)
    create_parser.add_argument("--scope", action="append", default=[])
    create_parser.add_argument("--stable-read", action="append", default=[])
    create_parser.add_argument("--concurrent-scope", action="append", default=[])

    diff_parser = subparsers.add_parser("diff")
    diff_parser.add_argument("--snapshot-dir", type=Path, required=True)
    diff_parser.add_argument("--output", type=Path)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--snapshot-dir", type=Path, required=True)
    restore_parser.add_argument("--archive-root", type=Path, required=True)
    restore_parser.add_argument("--output", type=Path)

    accept_parser = subparsers.add_parser("accept")
    accept_parser.add_argument("--snapshot-dir", type=Path, required=True)
    accept_parser.add_argument("--scope-diff-path", type=Path, required=True)
    accept_parser.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    repo = args.repo_root.resolve()
    if args.action == "create":
        return create(args, repo)
    if args.action == "diff":
        return diff(args, repo)
    if args.action == "restore":
        return restore(args, repo)
    if args.action == "accept":
        return accept(args, repo)
    return fail([f"unknown action: {args.action}"])


if __name__ == "__main__":
    sys.exit(main())
