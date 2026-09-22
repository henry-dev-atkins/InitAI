#!/usr/bin/env python3
"""Reject active code/config references that load repository archive roots."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from workflow_common import is_excluded

SCANNED_SUFFIXES = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java",
    ".cs", ".c", ".cc", ".cpp", ".h", ".hpp", ".toml", ".yaml", ".yml",
    ".json", ".ini", ".cfg", ".sh", ".ps1", ".cmd",
}
CONTROL_ROOTS = {".agents", ".codex", "AI_SPACE"}
REFERENCE = re.compile(r"(?:AI_SPACE/)?archive[\\/]", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    findings: list[str] = []
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        relative = path.relative_to(repo).as_posix()
        if is_excluded(relative):
            continue
        if relative.split("/", 1)[0] in CONTROL_ROOTS:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if REFERENCE.search(line):
                findings.append(f"{relative}:{number}: active code/config references archive path")
    if findings:
        print("FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PASS")
    print("archive_isolation=clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
