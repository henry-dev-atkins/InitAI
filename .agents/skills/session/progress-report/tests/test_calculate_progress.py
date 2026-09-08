import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from calculate_progress import build_metrics


class ProgressMetricsTests(unittest.TestCase):
    def test_cli_emits_versioned_metrics(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd() / "temp") as temporary:
            session = Path(temporary) / "session__20260907_120000"
            session.mkdir()
            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(Path(__file__).parents[1] / "scripts" / "calculate_progress.py"),
                    "--session",
                    str(session),
                    "--report-time",
                    "2026-09-07T13:00:00+00:00",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(json.loads(result.stdout)["schema"], "progress-metrics.v1")

    def test_counts_rates_and_known_convergence(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd() / "temp") as temporary:
            session = Path(temporary) / "session__20260907_120000"
            session.mkdir()
            (session / "finding_register.json").write_text(
                '{"schema":"finding-register-current.v1","findings":['
                '{"id":"F001","status":"RESOLVED"},'
                '{"id":"F002","status":"ASSIGNED"},'
                '{"id":"F003","status":"OPEN"}]}', encoding="utf-8"
            )
            (session / "workstream_register.md").write_text(
                "| Workstream | Outcome | State |\n|---|---|---|\n"
                "| WS001 | done | ACCEPTED |\n| WS002 | work | IMPLEMENTING |\n", encoding="utf-8"
            )
            metrics = build_metrics(session, datetime(2026, 9, 7, 13, 0, tzinfo=timezone.utc))
            self.assertEqual(metrics["findings"]["known_total"], 3)
            self.assertEqual(metrics["findings"]["solved"], 1)
            self.assertEqual(metrics["workstreams"]["completed"], 1)
            self.assertEqual(metrics["convergence"]["known_closure_percent"], 33.3)
            self.assertEqual(metrics["convergence"]["perfectly_converged"], False)
            self.assertEqual(metrics["latent_finding_scenario"]["projected_next_review_findings"], 3)

    def test_explicit_chat_events_are_retained_as_context_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd() / "temp") as temporary:
            session = Path(temporary) / "session__20260907_120000"
            session.mkdir()
            metrics = build_metrics(
                session,
                datetime(2026, 9, 7, 13, 0, tzinfo=timezone.utc),
                ["prompt=2026-09-07T12:05:00+00:00"],
            )
            self.assertEqual(metrics["evidence"]["chat_events"][0]["label"], "prompt")
            self.assertEqual(metrics["evidence"]["chat_events"][0]["timestamp"], "2026-09-07T12:05:00+00:00")
            self.assertEqual(metrics["evidence"]["file_times"], None)

    def test_missing_records_mark_metrics_without_inventing_counts(self) -> None:
        with tempfile.TemporaryDirectory(dir=Path.cwd() / "temp") as temporary:
            session = Path(temporary) / "session__20260907_120000"
            session.mkdir()
            metrics = build_metrics(session, datetime(2026, 9, 7, 13, 0, tzinfo=timezone.utc))
            self.assertEqual(metrics["findings"]["known_total"], 0)
            self.assertIsNone(metrics["convergence"]["known_closure_percent"])
            self.assertIsNone(metrics["rates_per_elapsed_hour"]["solved_findings"])
            self.assertEqual(metrics["latent_finding_scenario"]["confidence"], "unavailable")


if __name__ == "__main__":
    unittest.main()
