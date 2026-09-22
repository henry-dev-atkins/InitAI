"""Behaviour tests for the repository helper tools."""

from __future__ import annotations

from decimal import Decimal
import subprocess
import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from calculator import CalculatorError, evaluate_expression  # noqa: E402


class CalculatorTests(unittest.TestCase):
    """Verify safe Decimal arithmetic and its command-line contract."""

    def test_evaluates_basic_decimal_expression(self) -> None:
        """Nested arithmetic returns the expected Decimal result."""
        self.assertEqual(
            evaluate_expression("1.20 + (2.30 * 2)"),
            Decimal("5.80"),
        )

    def test_cli_reads_expression_from_stdin(self) -> None:
        """The CLI evaluates one expression supplied through standard input."""
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/calculator.py")],
            cwd=ROOT,
            input="1.20 + 2.30\n",
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "3.50\n")
        self.assertEqual(result.stderr, "")

    def test_rejects_names_and_function_calls(self) -> None:
        """The calculator accepts arithmetic syntax only."""
        with self.assertRaises(CalculatorError):
            evaluate_expression("__import__('os').system('whoami')")

    def test_rejects_division_by_zero(self) -> None:
        """Division by zero fails explicitly."""
        with self.assertRaises(CalculatorError):
            evaluate_expression("1 / 0")


class FinalCommitWrapperTests(unittest.TestCase):
    """Verify the terminal review guard fails closed."""

    def run_wrapper(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        """Run the Python commit wrapper from the repository root."""
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(ROOT / "tools/orchestrator_final_commit.py"),
                *arguments,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_rejects_commit_message_without_repository_prefix(self) -> None:
        """Commit policy is checked before terminal review validation."""
        result = self.run_wrapper(
            "--terminal-review",
            "missing-terminal-review.json",
            "--message",
            "unapproved message",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("commit message", result.stderr.lower())

    def test_rejects_missing_terminal_review(self) -> None:
        """A missing terminal review cannot authorise a commit."""
        result = self.run_wrapper(
            "--terminal-review",
            "missing-terminal-review.json",
            "--message",
            "FIX: test wrapper",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("terminal review", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
