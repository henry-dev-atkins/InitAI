from pathlib import Path
import unittest


ROOT = Path(__file__).parents[4]
PLAN = (ROOT / ".agents/skills/planning/plan/SKILL.md").read_text(encoding="utf-8")
REVIEW = (ROOT / ".agents/skills/planning/plan-review/SKILL.md").read_text(encoding="utf-8")


class PlanContractTests(unittest.TestCase):
    def test_plan_requires_quality_contract(self):
        for value in (
            "Findings", "Findings: none", "Plan Quality Review", "Plan Quality Summary",
            "Solutions.1.a", "Solutions.1.b", "Solutions.1.c", "Solutions.1.d",
            "Solutions.2.a", "Solutions.2.b", "Solutions.2.c", "Solutions.2.d",
            "$code-style", "$maintain-review", "$maintain-elegance", "$parsimonious",
            "$adversarial-review", "$plan-desk-check",
        ):
            self.assertIn(value, PLAN)

    def test_plan_review_requires_independent_checks(self):
        for value in ("Findings: none", "Plan Quality Summary", "independently",
                      "exception", "N", "Yes, <specific explanation and examples>"):
            self.assertIn(value, REVIEW)

    def test_elegance_contract_is_exact(self):
        self.assertIn("exactly `No` or `Yes, <specific explanation and examples>`", PLAN)
        self.assertIn("exactly `No` or `Yes, <specific explanation and examples>`", REVIEW)


if __name__ == "__main__":
    unittest.main()
