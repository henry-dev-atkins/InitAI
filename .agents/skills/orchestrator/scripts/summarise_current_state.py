#!/usr/bin/env python3
"""Produce a compact current-state capsule from authoritative session artefacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from workflow_common import repository_tree_hash


def read_optional(path: Path) -> tuple[str, bool]:
    if not path.exists():
        return "", False
    return path.read_text(encoding="utf-8", errors="replace"), True


def first_lines(text: str, limit: int = 12) -> list[str]:
    return [line.rstrip() for line in text.splitlines() if line.strip()][:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--global-pointer", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo = args.repo_root.resolve()
    session = args.session.resolve()
    if not session.exists():
        print(f"FAIL\n- session does not exist: {session}")
        return 1

    sources = {
        "session_board": session / "session_board.md",
        "finding_register": session / "finding_register.md",
        "requirement_register": session / "requirement_register.json",
        "workstream_register": session / "workstream_register.md",
        "contract_register": session / "contract_register.json",
        "locks": session / "locks.md",
    }
    missing: list[str] = []
    contents: dict[str, str] = {}
    for name, path in sources.items():
        text, ok = read_optional(path)
        if not ok:
            missing.append(str(path))
        contents[name] = text

    tree_hash = repository_tree_hash(repo)
    output_path = args.output or session / "current_state_capsule.md"
    pointer_path = args.global_pointer or repo / "AI_SPACE/current_state.md"
    lines = [
        "# Current State Capsule",
        "",
        "This is a workflow cache, not spec authority and not product capability.",
        "",
        "## Revision",
        "",
        f"- Canonical active-tree hash: {tree_hash}",
        f"- Current checkout: `{repo}`",
        f"- Active session: `{session}`",
        f"- Session capsule path: `{output_path}`",
        f"- Global pointer path: `{pointer_path}`",
        "",
        "## Open Blockers",
        "",
    ]
    blocker_lines = [line for line in first_lines(contents["session_board"], 30) if "BLOCKED" in line or "blocker" in line.lower()]
    lines.extend(f"- {line}" for line in (blocker_lines or ["none found in available session board"]))
    for heading, key, limit in [
        ("Active Portfolio", "workstream_register", 20),
        ("Finding Snapshot", "finding_register", 20),
        ("Requirement Snapshot", "requirement_register", 12),
        ("Contract Snapshot", "contract_register", 12),
        ("Locks", "locks", 20),
    ]:
        lines.extend(["", f"## {heading}", ""])
        selected = first_lines(contents[key], limit) or [f"{key.replace('_', ' ')} missing or empty"]
        lines.extend(f"- {line}" for line in selected)
    lines.extend(["", "## Missing or Deferred Sources", ""])
    lines.extend(f"- `{item}`" for item in (missing or ["none"]))
    capsule = "\n".join(lines) + "\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(capsule, encoding="utf-8")
    pointer_path.parent.mkdir(parents=True, exist_ok=True)
    pointer_path.write_text(capsule, encoding="utf-8")
    print(capsule, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
