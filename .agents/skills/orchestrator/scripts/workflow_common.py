#!/usr/bin/env python3
"""Shared, dependency-free helpers for orchestration validators and runners."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CONTROL_OR_PLACEHOLDER = re.compile(r"[\x00-\x1f{}<>]")
GLOB_CHARS = re.compile(r"[*?\[]")

DEFAULT_TREE_EXCLUDES = (
    ".git",
    "AI_SPACE/sessions",
    "AI_SPACE/handovers",
    "AI_SPACE/archive",
    "AI_SPACE/current_state.md",
    "AI_SPACE/TODO.md",
    "AI_SPACE/AI_LEARNINGS_LOG.md",
    "archive",
    "temp",
    ".ruff_cache",
    ".pytest_cache",
    ".mypy_cache",
    ".triton_tmp",
    "__pycache__",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()




def path_sha256(path: Path) -> str:
    """Hash one file, symlink or directory tree deterministically."""
    if path.is_symlink():
        return hashlib.sha256(os.readlink(path).encode("utf-8")).hexdigest()
    if path.is_file():
        return file_sha256(path)
    if not path.is_dir():
        raise FileNotFoundError(path)
    digest = hashlib.sha256()
    for child in sorted(path.rglob("*"), key=lambda item: item.as_posix().casefold()):
        relative = child.relative_to(path).as_posix()
        if child.is_symlink():
            kind = "symlink"
            payload = os.readlink(child).encode("utf-8")
        elif child.is_file():
            kind = "file"
            payload = child.read_bytes()
        else:
            continue
        digest.update(kind.encode("ascii"))
        digest.update(b"\0")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(payload).digest())
        digest.update(b"\n")
    return digest.hexdigest()

def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def normalise_repo_relative(value: str, *, allow_glob: bool = False) -> str:
    raw = value.replace("\\", "/").strip()
    if not raw or CONTROL_OR_PLACEHOLDER.search(raw):
        raise ValueError(f"malformed repository path: {value}")
    if not allow_glob and GLOB_CHARS.search(raw):
        raise ValueError(f"write/read scopes must use exact file or directory roots, not globs: {value}")
    if re.match(r"^[A-Za-z]:", raw) or raw.startswith("/"):
        raise ValueError(f"absolute path is not allowed: {value}")
    if raw == ".":
        return "."
    components = raw.split("/")
    if any(part in {"", ".", ".."} for part in components):
        raise ValueError(f"path must already be canonical and may not contain empty, '.' or '..' components: {value}")
    normalised = posixpath.normpath(raw)
    if normalised in {"", "."}:
        return "."
    if normalised == ".." or normalised.startswith("../"):
        raise ValueError(f"path escapes repository: {value}")
    return normalised[2:] if normalised.startswith("./") else normalised


def repo_path(repo: Path, value: str, *, allow_glob: bool = False) -> Path:
    relative = normalise_repo_relative(value, allow_glob=allow_glob)
    resolved = (repo.resolve() / relative).resolve(strict=False)
    try:
        resolved.relative_to(repo.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository through a symlink: {value}") from exc
    return resolved


def scope_key(value: str) -> str:
    normalised = normalise_repo_relative(value)
    return normalised.casefold() if os.name == "nt" else normalised


def scopes_overlap(left: str, right: str) -> bool:
    left_key = scope_key(left).rstrip("/")
    right_key = scope_key(right).rstrip("/")
    return (
        left_key == right_key
        or left_key.startswith(right_key + "/")
        or right_key.startswith(left_key + "/")
    )


def any_scope_overlap(left: Iterable[str], right: Iterable[str]) -> list[tuple[str, str]]:
    overlaps: list[tuple[str, str]] = []
    for left_scope in left:
        for right_scope in right:
            if scopes_overlap(str(left_scope), str(right_scope)):
                overlaps.append((str(left_scope), str(right_scope)))
    return overlaps


def is_excluded(relative: str, excludes: Iterable[str] = DEFAULT_TREE_EXCLUDES) -> bool:
    rel = relative.replace("\\", "/").strip("/")
    parts = rel.split("/") if rel else []
    for excluded in excludes:
        key = excluded.replace("\\", "/").strip("/")
        if rel == key or rel.startswith(key + "/"):
            return True
        if "/" not in key and key in parts:
            return True
    return False


def iter_active_entries(repo: Path, excludes: Iterable[str] = DEFAULT_TREE_EXCLUDES):
    root = repo.resolve()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        relative = path.relative_to(root).as_posix()
        if is_excluded(relative, excludes):
            continue
        if path.is_symlink():
            target = os.readlink(path)
            yield relative, "symlink", target.encode("utf-8")
        elif path.is_file():
            yield relative, "file", path.read_bytes()


def repository_tree_hash(repo: Path, excludes: Iterable[str] = DEFAULT_TREE_EXCLUDES) -> str:
    digest = hashlib.sha256()
    for relative, kind, payload in iter_active_entries(repo, excludes):
        digest.update(kind.encode("ascii"))
        digest.update(b"\0")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(payload).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def inventory_tree_hash(inventory: dict[str, dict[str, str]]) -> str:
    """Recompute the canonical tree hash from a recorded repository inventory."""
    digest = hashlib.sha256()
    for relative in sorted(inventory, key=str.casefold):
        entry = inventory[relative]
        digest.update(entry["kind"].encode("ascii"))
        digest.update(b"\0")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(entry["sha256"]))
        digest.update(b"\n")
    return digest.hexdigest()


def repository_inventory(repo: Path, excludes: Iterable[str] = DEFAULT_TREE_EXCLUDES) -> dict[str, dict[str, str]]:
    inventory: dict[str, dict[str, str]] = {}
    for relative, kind, payload in iter_active_entries(repo, excludes):
        inventory[relative] = {"kind": kind, "sha256": hashlib.sha256(payload).hexdigest()}
    return inventory


def diff_inventories(before: dict[str, dict[str, str]], after: dict[str, dict[str, str]]) -> dict[str, list[str]]:
    before_paths = set(before)
    after_paths = set(after)
    return {
        "added": sorted(after_paths - before_paths),
        "deleted": sorted(before_paths - after_paths),
        "modified": sorted(
            path for path in before_paths & after_paths if before[path] != after[path]
        ),
    }


def path_within_scopes(path: str, scopes: Iterable[str]) -> bool:
    normalised = scope_key(path)
    for scope in scopes:
        scope_normalised = scope_key(str(scope)).rstrip("/")
        if normalised == scope_normalised or normalised.startswith(scope_normalised + "/"):
            return True
    return False


def parse_markdown_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return header or [], rows


def split_ids(value: str) -> list[str]:
    if not value or value.strip().lower() in {"none", "null", "-"}:
        return []
    return [item for item in re.split(r"[\s,]+", value.strip()) if item]


def parse_bullet_section(text: str, heading: str) -> list[str]:
    match = re.search(
        rf"^{re.escape(heading)}:\s*$\n(?P<body>(?:\s*-\s+.*(?:\n|$))+)",
        text,
        re.MULTILINE,
    )
    if not match:
        return []
    values: list[str] = []
    for line in match.group("body").splitlines():
        item = re.sub(r"^\s*-\s+", "", line).strip().strip("`")
        if item and item.lower() != "none":
            values.append(item)
    return values
