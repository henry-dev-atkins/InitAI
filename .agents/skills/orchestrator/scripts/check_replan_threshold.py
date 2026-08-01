#!/usr/bin/env python3
"""Fail when repeated replanning exceeds the workflow threshold without diagnosis."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def fail(message: str) -> int:
    print("FAIL")
    print(f"- {message}")
    return 1


def parse_markdown_table(path: Path, workstream: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    lines = [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines()]
    header: list[str] | None = None
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and cells[0] == "Workstream":
            header = cells
            continue
        if header and cells and cells[0] == workstream:
            return dict(zip(header, cells))
    return None


def has_marker(session: Path, workstream: str) -> bool:
    pattern = re.compile(r"(DIAGNOSIS|BACK[-_ ]TO[-_ ]BASICS|BACK_TO_BASICS)", re.IGNORECASE)
    for path in session.rglob("*"):
        if path.is_file() and (workstream in path.as_posix() or path.name in {"workstream_register.md", "session_board.md"}):
            try:
                if pattern.search(path.read_text(encoding="utf-8", errors="replace")):
                    return True
            except OSError:
                continue
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--workstream", required=True)
    parser.add_argument("--plan-threshold", type=int, default=3)
    parser.add_argument("--implementation-threshold", type=int, default=2)
    args = parser.parse_args()

    if not args.session.exists():
        return fail(f"session does not exist: {args.session}")
    row = parse_markdown_table(args.session / "workstream_register.md", args.workstream)
    if row is None:
        return fail(f"workstream not found in register: {args.workstream}")

    try:
        rejected_plans = int(row.get("Rejected Plans", "0"))
        rejected_implementations = int(row.get("Rejected Implementations", "0"))
    except ValueError:
        return fail("rejection counters must be integers")

    threshold_state = row.get("Threshold State", "")
    exceeded = rejected_plans >= args.plan_threshold or rejected_implementations >= args.implementation_threshold
    marker_present = "BACK_TO_BASICS" in threshold_state or "DIAGNOSIS" in threshold_state or has_marker(args.session, args.workstream)
    if exceeded and not marker_present:
        return fail(
            f"{args.workstream} exceeded threshold: rejected_plans={rejected_plans}, "
            f"rejected_implementations={rejected_implementations}"
        )

    print("PASS")
    print(f"workstream={args.workstream}")
    print(f"rejected_plans={rejected_plans}")
    print(f"rejected_implementations={rejected_implementations}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
