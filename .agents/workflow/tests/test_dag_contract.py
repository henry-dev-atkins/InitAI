import importlib.util
import sys
import unittest


RUNNER = __import__("pathlib").Path(__file__).parents[3] / ".agents" / "workflow" / "run.py"
spec = importlib.util.spec_from_file_location("workflow_runner", RUNNER)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)


def node(dependencies=None, source=None):
    inputs = {}
    if source:
        inputs["input"] = {"schema": "schemas/value.json", "source": source}
    return {
        "kind": "agent_task", "agent": "worker", "depends_on": dependencies or [],
        "inputs": inputs, "outputs": {"output": {"schema": "schemas/value.json"}},
        "read_scope": ["."], "write_scope": [], "resources": [],
    }


class DagContractTests(unittest.TestCase):
    def test_valid_graph_and_bound_ports(self):
        graph = {"nodes": {"source": node(), "consumer": node(["source"], "source.output")}}
        runner.validate_loop_graph(graph, {"worker"}, set())

    def test_cycles_are_rejected(self):
        graph = {"nodes": {"a": node(["b"]), "b": node(["a"])} }
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(graph, {"worker"}, set())

    def test_unbound_source_is_rejected(self):
        graph = {"nodes": {"consumer": node(["source"], "source.output")}}
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(graph, {"worker"}, set())

    def test_input_source_requires_declared_dependency(self):
        graph = {"nodes": {"source": node(), "consumer": node([], "source.output")}}
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(graph, {"worker"}, set())

    def test_named_bindings_are_validated(self):
        graph = {"nodes": {"source": node()}}
        with self.assertRaises(runner.WorkflowError):
            runner.validate_loop_graph(graph, {"other"}, set())


if __name__ == "__main__":
    unittest.main()
