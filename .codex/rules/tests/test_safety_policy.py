"""Static tests for the autonomous deletion policy."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]


class SafetyPolicyTests(unittest.TestCase):
    def test_instructions_do_not_authorise_autonomous_deletion(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        removal = (ROOT / ".agents/skills/maintain/thorough-removal/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Never permanently delete", agents)
        self.assertIn("Never permanently delete", removal)
        self.assertNotIn("temp/` may be removed", agents)
        self.assertNotIn("temp/` may be removed", removal)

    def test_incident_commands_are_forbidden(self) -> None:
        rules = (ROOT / ".codex/rules/safety.rules").read_text(encoding="utf-8")
        for command in ('pattern = ["rm"]', 'pattern = ["rd"]',
                        'pattern = ["rmdir"]', 'pattern = ["del"]',
                        'pattern = ["erase"]', 'pattern = ["Remove-Item"]'):
            with self.subTest(command=command):
                self.assertIn(command, rules)
        self.assertIn("rd /s /q", rules)


if __name__ == "__main__":
    unittest.main()
