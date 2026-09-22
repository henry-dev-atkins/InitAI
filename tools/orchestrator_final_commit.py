#!/usr/bin/env python3
"""Validate the terminal review before creating the final local commit."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


COMMIT_PREFIXES = (
    "CLEANUP:",
    "FEAT:",
    "CONFIG:",
    "DOCS:",
    "FIX:",
    "TEST:",
    "AI:",
    "SPEC_EDIT:",
)


class FinalCommitError(RuntimeError):
    """Report a failed terminal review or Git operation."""


def repository_root() -> Path:
    """Return the repository root containing this tool directory."""
    return Path(__file__).resolve().parents[1]


def run_process(arguments: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    """Run one repository command and capture its output for clear failures."""
    return subprocess.run(
        arguments,
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def validate_commit_message(message: str) -> None:
    """Require one approved repository commit prefix and one-line text."""
    if not message.strip():
        raise FinalCommitError("commit message must not be empty")
    if "\n" in message or "\r" in message:
        raise FinalCommitError("commit message must be one line")
    if not message.startswith(COMMIT_PREFIXES):
        prefixes = ", ".join(COMMIT_PREFIXES)
        raise FinalCommitError(f"commit message must start with one of: {prefixes}")


def validate_terminal_review(review: str, root: Path) -> None:
    """Run the repository terminal validator against the current active tree."""
    validator = root / ".agents/skills/orchestrator/scripts/validate_terminal_coverage.py"
    if not validator.is_file():
        raise FinalCommitError(f"terminal review validator is missing: {validator}")

    result = run_process(
        [
            sys.executable,
            "-B",
            str(validator),
            review,
            "--repo-root",
            str(root),
        ],
        root,
    )
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        raise FinalCommitError(f"terminal review validation failed:\n{details}")


def ensure_git_repository(root: Path) -> None:
    """Require that the tool is operating on the repository it resolved."""
    result = run_process(["git", "rev-parse", "--show-toplevel"], root)
    if result.returncode != 0:
        raise FinalCommitError("current directory is not a Git repository")
    reported_root = Path(result.stdout.strip()).resolve()
    if reported_root != root.resolve():
        raise FinalCommitError(f"Git repository root does not match tool root: {reported_root}")


def stage_changes(root: Path) -> None:
    """Stage the current repository tree after terminal validation has passed."""
    result = run_process(["git", "add", "--all", "--", "."], root)
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        raise FinalCommitError(f"git add failed:\n{details}")

    result = run_process(["git", "diff", "--cached", "--quiet"], root)
    if result.returncode == 0:
        raise FinalCommitError("there are no changes to commit")
    if result.returncode != 1:
        details = (result.stdout + result.stderr).strip()
        raise FinalCommitError(f"could not inspect staged changes:\n{details}")


def create_commit(message: str, root: Path) -> None:
    """Create one local commit from the staged, terminal-validated tree."""
    result = run_process(["git", "commit", "--message", message], root)
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        raise FinalCommitError(f"git commit failed:\n{details}")
    output = (result.stdout + result.stderr).strip()
    if output:
        print(output)


def main() -> int:
    """Validate arguments, run terminal review and create one local commit."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal-review", required=True)
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    try:
        root = repository_root()
        validate_commit_message(args.message)
        ensure_git_repository(root)
        validate_terminal_review(args.terminal_review, root)
        stage_changes(root)
        create_commit(args.message, root)
    except FinalCommitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
