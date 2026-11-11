import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[4]
SKILL = ROOT / ".agents" / "skills" / "maintain" / "find-dev-artifacts" / "SKILL.md"
INDEX = ROOT / ".agents" / "skills" / "README.md"


class FindDevArtifactsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")

    def test_identity_and_discovery(self):
        self.assertIn("name: find-dev-artifacts", self.skill)
        self.assertIn("$find-dev-artifacts", self.index)

    def test_scope_and_report_only_boundaries(self):
        for phrase in (
            "exactly the scope supplied by the caller",
            "wider\nrepository context",
            "one exact element per finding",
            "Ignore generated, archived, migration, fixture, and session paths",
            "Do not edit files",
            "create workflow phases",
        ):
            self.assertIn(phrase, self.skill)

    def test_cues_and_capability_traceability(self):
        for phrase in (
            "finding", "workstream", "session", "attempt", "review",
            "experiment", "migration", "final2", "v2", "capability_or_terminology:",
            "Do not prescribe a replacement name",
        ):
            self.assertIn(phrase, self.skill)

    def test_verdicts_and_output_contract(self):
        for phrase in (
            "CLEAN", "NEEDS_RENAMING", "PROCESS_LEAKAGE", "rank:",
            "severity:", "confidence:", "element:", "evidence:",
            "process_artifact:", "impact:", "Core Capability Impact",
            "CONFIRMED", "PROBABLE",
        ):
            self.assertIn(phrase, self.skill)


if __name__ == "__main__":
    unittest.main()
