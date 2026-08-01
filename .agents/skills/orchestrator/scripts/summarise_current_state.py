#!/usr/bin/env python3
"""Produce a compact current-state capsule from session artefacts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def read_optional(path: Path) -> tuple[str, bool]:
    if not path.exists():
        return "", False
    return path.read_text(encoding="utf-8", errors="replace"), True


def first_lines(text: str, limit: int = 12) -> list[str]:
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return lines[:limit]


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unavailable"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    session = args.session
    if not session.exists():
        print(f"FAIL\n- session does not exist: {session}")
        return 1

    sources = {
        "session_board": session / "session_board.md",
        "finding_register": session / "finding_register.md",
        "workstream_register": session / "workstream_register.md",
        "locks": session / "locks.md",
    }
    missing: list[str] = []
    contents: dict[str, str] = {}
    for name, path in sources.items():
        text, ok = read_optional(path)
        if not ok:
            missing.append(str(path))
        contents[name] = text

    lines = [
        "# Current State Capsule",
        "",
        "This is a workflow cache, not spec authority and not product capability.",
        "",
        "## Revision",
        "",
        f"- Current checkout: {git_value(['rev-parse', '--short', 'HEAD'])}",
        f"- Dirty state: {git_value(['status', '--short']) or 'clean'}",
        f"- Active session: `{session.as_posix()}`",
        "",
        "## Open Blockers",
        "",
    ]
    blocker_lines = [line for line in first_lines(contents["session_board"], 30) if "BLOCKED" in line or "blocker" in line.lower()]
    lines.extend(f"- {line}" for line in (blocker_lines or ["none found in available session board"]))
    lines.extend(["", "## Active Portfolio", ""])
    register_lines = first_lines(contents["workstream_register"], 20) or ["workstream register missing or empty"]
    lines.extend(f"- {line}" for line in register_lines)
    lines.extend(["", "## Finding Snapshot", ""])
    finding_lines = first_lines(contents["finding_register"], 20) or ["finding register missing or empty"]
    lines.extend(f"- {line}" for line in finding_lines)
    lines.extend(["", "## Locks", ""])
    lock_lines = first_lines(contents["locks"], 20) or ["locks file missing or empty"]
    lines.extend(f"- {line}" for line in lock_lines)
    lines.extend(["", "## Missing or Deferred Sources", ""])
    lines.extend(f"- `{item}`" for item in (missing or ["none"]))
    capsule = "\n".join(lines) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(capsule, encoding="utf-8")
    print(capsule, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
