#!/usr/bin/env python3
"""Calculate reproducible progress metrics from one AI_SPACE session."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


WORKSTREAM_GROUPS = {
    "completed": {"ACCEPTED"},
    "in_progress": {"PLANNING", "REPLANNING", "IMPLEMENTING", "AWAITING_IMPLEMENTATION_REVIEW"},
    "waiting": {
        "AWAITING_PLAN", "AWAITING_PLAN_COLLATION", "AWAITING_PLAN_PREFLIGHT",
        "AWAITING_PLAN_REVIEW", "READY", "REJECTED", "BLOCKED",
    },
    "terminal_excluded": {"CANCELLED", "SUPERSEDED"},
}


FINDING_GROUPS = {
    "solved": {"RESOLVED"},
    "in_progress": {"ASSIGNED"},
    "waiting": {"OPEN", "BLOCKED", "DEFERRED_BY_HUMAN"},
}


def parse_time(value: str) -> datetime:
    """Parse an ISO-8601 timestamp and require a timezone."""

    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp requires a timezone: {value}")
    return parsed


def session_start(session: Path, report_time: datetime) -> datetime:
    """Read the session start from the repository session name."""

    match = re.search(r"session__(\d{8}_\d{6})$", session.name)
    if not match:
        raise ValueError(f"session name must end with session__YYYYMMDD_HHMMSS: {session}")
    return datetime.strptime(match.group(1), "%Y%m%d_%H%M%S").replace(tzinfo=report_time.tzinfo)


def load_json(path: Path) -> Any:
    """Load one JSON file."""

    return json.loads(path.read_text(encoding="utf-8"))


def parse_chat_events(events: list[str]) -> list[dict[str, str]]:
    """Validate and normalise explicit chat-event inputs."""

    parsed: list[dict[str, str]] = []
    for event in events:
        label, separator, value = event.partition("=")
        if not separator or not label.strip():
            raise ValueError(f"chat event must use LABEL=ISO-8601: {event}")
        parsed.append({"label": label.strip(), "timestamp": parse_time(value.strip()).isoformat()})
    return parsed


def file_time_window(session: Path, report_time: datetime) -> dict[str, str] | None:
    """Return the weak file-time window for the current session."""

    files = [path for path in session.glob("**/*") if path.is_file()]
    if not files:
        return None
    times = [datetime.fromtimestamp(path.stat().st_mtime, tz=report_time.tzinfo) for path in files]
    return {
        "quality": "weak",
        "start": min(times).isoformat(),
        "end": max(times).isoformat(),
    }


def read_findings(session: Path) -> list[dict[str, str]]:
    """Read finding status from the current workflow state only."""
    state_path = session / "state.json"
    if not state_path.is_file():
        return []
    state = load_json(state_path)
    workstream_by_finding = {
        finding_id: workstream
        for workstream in state.get("workstreams", {}).values()
        for finding_id in workstream.get("findings", [])
    }
    records: list[dict[str, str]] = []
    for finding in state.get("findings", []):
        workstream = workstream_by_finding.get(finding["id"])
        if workstream is None or workstream.get("stage") == "pending":
            status = "OPEN"
        elif workstream.get("blocked") is not None:
            status = "BLOCKED"
        elif workstream.get("stage") == "accepted":
            status = "RESOLVED"
        else:
            status = "ASSIGNED"
        records.append({"id": finding["id"], "status": status})
    return records


def read_workstreams(session: Path) -> list[dict[str, str]]:
    """Read workstream status from the current workflow state only."""
    state_path = session / "state.json"
    if not state_path.is_file():
        return []
    state = load_json(state_path)
    return [
        {
            "id": item["id"],
            "outcome": item["outcome"],
            "status": "BLOCKED" if item.get("blocked") else (
                "ACCEPTED" if item.get("stage") == "accepted"
                else item.get("stage", "").upper()
            ),
        }
        for item in state.get("workstreams", {}).values()
    ]


def conformance_status(session: Path) -> str:
    """Read fresh conformance status from the current workflow state only."""
    state_path = session / "state.json"
    if not state_path.is_file():
        return "NOT_RECORDED"
    state = load_json(state_path)
    return "PASS" if state.get("stage") == "done" else "NOT_RECORDED"


def build_metrics(session: Path, report_time: datetime, chat_events: list[str] | None = None) -> dict[str, Any]:
    """Build all report metrics from current session evidence."""

    if not session.is_dir():
        raise ValueError(f"session does not exist: {session}")
    start = session_start(session, report_time)
    elapsed_seconds = max(0.0, (report_time - start).total_seconds())
    elapsed_hours = elapsed_seconds / 3600.0
    findings = read_findings(session)
    workstreams = read_workstreams(session)
    finding_counts = {name: sum(item["status"] in statuses for item in findings) for name, statuses in FINDING_GROUPS.items()}
    workstream_counts = {name: sum(item["status"] in statuses for item in workstreams) for name, statuses in WORKSTREAM_GROUPS.items()}
    known_total = len(findings)
    solved = finding_counts["solved"]
    unresolved = known_total - solved
    completed = workstream_counts["completed"]
    finding_rate = solved / elapsed_hours if elapsed_hours > 0 and findings else None
    workstream_rate = completed / elapsed_hours if elapsed_hours > 0 and workstreams else None
    conformance = conformance_status(session)
    parsed_chat_events = parse_chat_events(chat_events or [])
    return {
        "schema": "progress-metrics.v1",
        "session": session.as_posix(),
        "session_start": start.isoformat(),
        "report_time": report_time.isoformat(),
        "elapsed_seconds": elapsed_seconds,
        "evidence": {
            "primary": "session_folder_timestamp_and_session_artefacts",
            "file_times": file_time_window(session, report_time),
            "chat_events": parsed_chat_events,
        },
        "workstreams": workstream_counts,
        "findings": {**finding_counts, "yet_to_find": "unknown", "known_total": known_total},
        "convergence": {
            "known_closure_percent": round(solved / known_total * 100.0, 1) if known_total else None,
            "fresh_conformance": conformance,
            "perfectly_converged": conformance == "PASS",
        },
        "rates_per_elapsed_hour": {
            "completed_workstreams": round(workstream_rate, 3) if workstream_rate is not None else None,
            "solved_findings": round(finding_rate, 3) if finding_rate is not None else None,
        },
        "eta_hours": {
            "known_findings": round(unresolved / finding_rate, 2) if finding_rate else None,
            "known_workstreams": round((len(workstreams) - completed) / workstream_rate, 2) if workstream_rate else None,
        },
        "latent_finding_scenario": {
            "projected_next_review_findings": known_total if findings else None,
            "confidence": "low" if findings else "unavailable",
            "excluded_from_convergence": True,
        },
        "workstream_records": workstreams,
        "finding_records": findings,
        "prior_report_count": len(list(session.parent.glob("session__*/progress_reports/report_*.md"))),
    }


def main() -> int:
    """Parse arguments and print one JSON metric record."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--report-time", required=True)
    parser.add_argument("--chat-event", action="append", default=[])
    args = parser.parse_args()
    try:
        report_time = parse_time(args.report_time)
        metrics = build_metrics(args.session.resolve(), report_time, args.chat_event)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
