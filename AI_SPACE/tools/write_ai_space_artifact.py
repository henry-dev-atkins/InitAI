#!/usr/bin/env python3
"""Write one authorised AI_SPACE control-plane artefact without shell redirection."""

from __future__ import annotations

import argparse
import base64
import binascii
import os
import tempfile
from pathlib import Path, PurePosixPath


ALLOWED_EXACT = {
    "AI_SPACE/TODO.md",
    "AI_SPACE/AI_LEARNINGS_LOG.md",
    "AI_SPACE/current_state.md",
}
ALLOWED_PREFIXES = (
    "AI_SPACE/sessions/",
    "AI_SPACE/handovers/",
    "AI_SPACE/archive/",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalise_path(raw: str) -> str:
    value = raw.replace("\\", "/").strip()
    if not value or value.startswith("/") or ":" in value:
        raise ValueError("Path must be a repository-relative AI_SPACE path")
    pure = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError("Path traversal and ambiguous path components are forbidden")
    result = pure.as_posix()
    if result not in ALLOWED_EXACT and not any(result.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise ValueError("Path is outside the authorised AI_SPACE control-plane locations")
    return result


def decode_content(value: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("ContentBase64 is not valid base64") from exc


def reject_symlink_components(root: Path, relative: str) -> Path:
    target = root
    for component in PurePosixPath(relative).parts:
        target = target / component
        if target.is_symlink():
            raise ValueError(f"Symlink path components are forbidden: {relative}")
    return target


def atomic_replace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--mode", choices=("create", "overwrite", "append"), required=True)
    parser.add_argument("--content-base64", required=True)
    args = parser.parse_args()

    try:
        relative = normalise_path(args.path)
        payload = decode_content(args.content_base64)
    except ValueError as exc:
        parser.error(str(exc))

    root = repo_root().resolve()
    try:
        target = reject_symlink_components(root, relative)
        resolved_target = target.resolve(strict=False)
        resolved_target.relative_to((root / "AI_SPACE").resolve())
    except ValueError as exc:
        parser.error(str(exc))

    if args.mode == "create":
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("xb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError:
            parser.error(f"Target already exists: {relative}")
    elif args.mode == "overwrite":
        atomic_replace(target, payload)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("ab") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

    print(relative)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
