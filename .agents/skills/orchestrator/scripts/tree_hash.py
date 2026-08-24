#!/usr/bin/env python3
"""Print the canonical active tree hash or record a campaign baseline."""

from __future__ import annotations

import argparse
from pathlib import Path

from workflow_common import repo_path, repository_inventory, repository_tree_hash, utc_now, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--baseline-output", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    tree_hash = repository_tree_hash(repo)
    if args.baseline_output:
        try:
            output = repo_path(repo, str(args.baseline_output))
        except ValueError as exc:
            parser.error(str(exc))
        relative = output.relative_to(repo).as_posix()
        if not relative.startswith("AI_SPACE/sessions/"):
            parser.error("Campaign baseline must be under AI_SPACE/sessions/")
        if output.exists():
            parser.error(f"Campaign baseline already exists: {relative}")
        write_json(
            output,
            {
                "schema": "campaign-baseline.v1",
                "created_at": utc_now(),
                "tree_hash": tree_hash,
                "inventory": repository_inventory(repo),
            },
        )
        print(f"baseline={relative}")
    print(tree_hash)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
