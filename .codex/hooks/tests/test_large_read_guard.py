from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


HOOK_PATH = Path(__file__).resolve().parents[1] / "large_read_guard.py"
spec = importlib.util.spec_from_file_location("large_read_guard", HOOK_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load hook at {HOOK_PATH}")
HOOK = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = HOOK
spec.loader.exec_module(HOOK)


class LargeReadGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(
            dir=Path(__file__).resolve().parents[3] / "temp", prefix="hook-test-"
        )
        self.root = Path(self.temp.name)
        self.write("src/small.txt", "one\ntwo\n")
        self.write("src/large.txt", "x\n" * 11)
        self.write("src/wide.txt", "z" * 101)
        self.settings = HOOK.Settings(10, 100)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def find(self, command: str) -> list[object]:
        return HOOK.find_large_reads(command, self.root, self.root, self.settings)

    def test_direct_and_bounded_reads(self) -> None:
        self.assertTrue(self.find("cat src/large.txt"))
        self.assertEqual(self.find("head -n 4 src/large.txt"), [])
        self.assertEqual(self.find("tail -4 src/large.txt"), [])
        self.assertEqual(self.find("Get-Content src/large.txt -TotalCount 4"), [])

    def test_bytes_and_aggregate_limits(self) -> None:
        self.assertTrue(self.find("less src/wide.txt"))
        for index in range(6):
            self.write(f"bundle/f{index}.txt", "a\nb\n")
        findings = self.find("cat bundle/*.txt")
        self.assertTrue(findings[0].aggregate)
        self.assertEqual(findings[0].operand_count, 6)

    def test_streams_and_unbounded_filters_are_denied(self) -> None:
        for command in (
            "tail -f src/small.txt",
            "Get-Content src/small.txt -Wait",
            "cat src/large.txt | sort",
            "cat src/large.txt | rg needle",
        ):
            with self.subTest(command=command):
                self.assertTrue(self.find(command))
        self.assertEqual(self.find("cat src/large.txt | head -n 4"), [])
        self.assertEqual(self.find("cat src/large.txt | wc -l"), [])

    def test_redirection_and_wrappers(self) -> None:
        self.assertEqual(self.find("cat src/large.txt > temp/copy.txt"), [])
        self.assertTrue(self.find("cat src/large.txt > /dev/stdout"))
        self.assertTrue(self.find("bash -lc 'cat src/large.txt'"))
        self.assertTrue(self.find("pwsh -Command \"Get-Content src/large.txt\""))

    def test_authority_paths_are_exempt(self) -> None:
        for path in (
            "AGENTS.md",
            "nested/AGENTS.md",
            "AI_SPACE/SPEC.md",
            "AI_SPACE/TODO.md",
            "AI_SPACE/AI_LEARNINGS_LOG.md",
            "AI_SPACE/sessions/one/plan.md",
            ".agents/skills/example/SKILL.md",
            ".agents/workflow/run.py",
            ".codex/agents/example.toml",
        ):
            self.write(path, "x\n" * 20)
            self.assertEqual(self.find(f"cat {path}"), [])

    def test_ambiguous_inputs_fail_closed(self) -> None:
        for command in (
            "cat missing.txt",
            "cat $FILE",
            "cat",
            "cat -",
            "cat C:/outside/file.txt",
        ):
            with self.subTest(command=command):
                with self.assertRaises(HOOK.UnsafeRead):
                    self.find(command)

    def test_path_forms_and_literal_wildcards(self) -> None:
        self.assertTrue(self.find("Get-Content -Path:src/large.txt"))
        self.assertEqual(HOOK.resolve("src/large.txt", True, self.root), [self.root / "src/large.txt"])

    def test_denial_has_supported_shape_without_content(self) -> None:
        output = HOOK.hook_output(self.find("cat src/large.txt"))
        specific = output["hookSpecificOutput"]
        self.assertEqual(specific["hookEventName"], "PreToolUse")
        self.assertEqual(specific["permissionDecision"], "deny")
        self.assertNotIn("xxxxxxxx", specific["permissionDecisionReason"])

    def run_main(self, event: object) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(HOOK.sys, "stdin", io.StringIO(json.dumps(event))), redirect_stdout(stdout), redirect_stderr(stderr):
            result = HOOK.main(["--line-threshold", "10", "--byte-threshold", "100"])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_main_requires_canonical_hook_payload(self) -> None:
        event = {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_use_id": "test-1",
            "cwd": str(self.root),
            "tool_input": {"command": "cat src/large.txt"},
        }
        result, output, error = self.run_main(event)
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(error, "")
        result, output, error = self.run_main({"tool_input": {"cmd": "cat src/large.txt"}})
        self.assertEqual(result, 2)
        self.assertEqual(output, "")
        self.assertIn("required", error)

    def test_main_fails_closed_on_bad_json(self) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(HOOK.sys, "stdin", io.StringIO("{")), redirect_stdout(stdout), redirect_stderr(stderr):
            result = HOOK.main(["--line-threshold", "10", "--byte-threshold", "100"])
        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("Expecting", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
