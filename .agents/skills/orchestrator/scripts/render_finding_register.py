#!/usr/bin/env python3
"""Render the canonical JSON finding register as the existing Markdown table view."""

from __future__ import annotations

import argparse
from pathlib import Path

from workflow_common import load_json


def safe(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = load_json(args.register)
    lines = [
        "# Finding Register",
        "",
        f"This file is a rendered view of `{args.register.as_posix()}`. Only the orchestrator changes the JSON authority or regenerates this view.",
        "",
        "| Finding ID | Status | Severity | Owner | Requirement IDs | Spec Authority | Problem | Repo Evidence | Affected Behaviour/Files | Resolution Evidence | Source Reports | Waiver |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for finding in data.get("findings", []):
        waiver = finding.get("waiver")
        waiver_text = waiver.get("waiver_id") if isinstance(waiver, dict) else "none"
        row = [
            finding.get("id"),
            finding.get("status"),
            finding.get("severity"),
            finding.get("owner"),
            ", ".join(finding.get("requirement_ids", [])) or "none",
            finding.get("spec_authority"),
            finding.get("problem"),
            finding.get("repo_evidence"),
            finding.get("affected_behaviour_files"),
            finding.get("resolution_evidence"),
            ", ".join(finding.get("source_reports", [])) or "none",
            waiver_text,
        ]
        lines.append("| " + " | ".join(safe(item) for item in row) + " |")
    lines.extend(
        [
            "",
            "Allowed status: `OPEN`, `ASSIGNED`, `RESOLVED`, `DEFERRED_BY_HUMAN`, `BLOCKED`.",
            "",
            "A finding becomes `RESOLVED` only after accepted implementation review provides the required evidence. `DEFERRED_BY_HUMAN` remains a terminal blocker unless each linked requirement has an explicit authorised waiver.",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS")
    print(f"output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
