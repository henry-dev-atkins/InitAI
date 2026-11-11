import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[3]
RUNNER = ROOT / ".agents" / "workflow" / "run.py"
spec = importlib.util.spec_from_file_location("executor_runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


class ExecutorContractTests(unittest.TestCase):
    def test_supported_profiles_are_centralised(self):
        self.assertEqual(
            runner.EXECUTOR_PROFILES,
            {"coding_monkey", "standard", "expert", "adversarial", "long_context", "math_genius"},
        )

    def test_current_workflow_check_accepts_executor_policy(self):
        workflow_path = ROOT / ".agents" / "workflow" / "workflow.toml"
        workflow = runner.tomllib.loads(workflow_path.read_text(encoding="utf-8"))
        roles, skills = runner.roles_and_skills(ROOT)
        runner.validate_loop_graph(workflow, roles, skills)

    def test_adversarial_profile_requires_independence(self):
        workflow_path = ROOT / ".agents" / "workflow" / "workflow.toml"
        workflow = runner.tomllib.loads(workflow_path.read_text(encoding="utf-8"))
        workflow["executors"]["adversarial"]["independent"] = False
        roles, skills = runner.roles_and_skills(ROOT)
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(workflow, roles, skills)

    def test_unknown_node_profile_is_rejected(self):
        workflow_path = ROOT / ".agents" / "workflow" / "workflow.toml"
        workflow = runner.tomllib.loads(workflow_path.read_text(encoding="utf-8"))
        workflow["nodes"]["conformance"]["executor"] = "unknown"
        roles, skills = runner.roles_and_skills(ROOT)
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(workflow, roles, skills)


if __name__ == "__main__":
    unittest.main()
