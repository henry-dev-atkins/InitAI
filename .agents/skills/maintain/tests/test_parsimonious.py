import pathlib
import unittest


ROOT = pathlib.Path(__file__).parents[4]
SKILL = ROOT / ".agents" / "skills" / "maintain" / "parsimonious" / "SKILL.md"
INDEX = ROOT / ".agents" / "skills" / "README.md"


class ParsimoniousContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")

    def test_identity_and_discovery(self):
        self.assertIn("name: parsimonious", self.skill)
        self.assertIn("$parsimonious", self.index)

    def test_scope_and_report_only_boundaries(self):
        for phrase in (
            "exactly the scope supplied by the caller",
            "directly connected dependencies",
            "Review tests only when tests are inside the supplied scope",
            "Review plans before implementation",
            "compare the diff with that plan",
            "Do not edit files",
            "create workflow phases",
        ):
            self.assertIn(phrase, self.skill)

    def test_cost_model_and_verdicts(self):
        for phrase in (
            "concept count", "cognitive load", "future change cost",
            "failure surface", "maintenance burden", "operational risk",
            "permission surface", "startup cost", "dependency lock-in",
            "migration burden", "user friction", "proof burden",
            "requirement scope", "PARSIMONIOUS", "NEEDS_TIGHTENING",
            "WASTEFUL",
        ):
            self.assertIn(phrase, self.skill)

    def test_output_contract_and_traceability(self):
        for field in (
            "rank:", "severity:", "confidence:", "cost_type:",
            "element:", "requirement_or_invariant:", "evidence:",
            "cost:", "smallest_preserving_simplification:",
            "Core Capability Impact",
        ):
            self.assertIn(field, self.skill)
        for confidence in ("CONFIRMED", "PROBABLE", "NEEDS_INVESTIGATION"):
            self.assertIn(confidence, self.skill)
        self.assertIn("requirement concern", self.skill)


if __name__ == "__main__":
    unittest.main()
