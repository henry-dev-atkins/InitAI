"""Exercise the file protocol through fresh CLI processes and real repository work.

Run from the repository root with Python 3.11 or newer:
    python -m unittest discover -s .agents/workflow/tests -v
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / ".agents/workflow/run.py"


class WorkflowBehaviour(unittest.TestCase):
    """Use isolated repository fixtures to check observable dispatch and recovery."""

    def setUp(self) -> None:
        """Create a repo-local disposable checkout with the real binding files."""
        (ROOT / "temp").mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(prefix="workflow-test-", dir=ROOT / "temp")
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        shutil.copytree(ROOT / ".agents/skills", self.repo / ".agents/skills")
        shutil.copytree(ROOT / ".codex/agents", self.repo / ".codex/agents")
        shutil.copytree(ROOT / ".agents/workflow", self.repo / ".agents/workflow")
        self.write("AI_SPACE/SPEC.md", "# Authority\nAddition returns the sum of its two inputs.\n")
        self.write("src/add.py", "def add(a, b):\n    return a - b\n")
        self.report = self.write("AI_SPACE/sessions/test/evidence.md", "Reviewed the complete declared scope.\n")
        self.session = "AI_SPACE/sessions/test"
        self.packet_number = 0


    def write(self, relative: str, text: str) -> str:
        """Write fixture content and return its repository-relative path."""
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return relative


    def command(self, operation: str, *arguments: str) -> list[str]:
        """Build an invocation shared by sequential and concurrent CLI tests."""
        return [sys.executable, str(RUNNER), operation, "--repo", str(self.repo),
                "--session", self.session, *arguments]


    def cli(self, operation: str, *arguments: str, success: bool = True) -> dict[str, Any]:
        """Run a fresh process and require both JSON output and the expected exit status."""
        process = subprocess.run(self.command(operation, *arguments), cwd=self.repo,
                                 capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode == 0, success,
                         f"{operation}: exit {process.returncode}\n{process.stdout}\n{process.stderr}")
        try:
            result = json.loads(process.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"CLI did not return JSON: {error}\n{process.stdout}\n{process.stderr}")
        self.assertEqual(result["ok"], success, result)
        return result


    def task(self, operation: str, workstream: str | None = None) -> dict[str, Any]:
        """Find a ready operation without depending on generated task identifiers."""
        result = self.cli("next")
        tasks = [task for task in result["tasks"]
                 if task["operation"] == operation and task.get("workstream_id") == workstream]
        self.assertEqual(len(tasks), 1, result)
        return tasks[0]


    def claim(self, operation: str, agent: str, workstream: str | None = None) -> dict[str, Any]:
        """Reserve the named operation for one concrete agent instance."""
        task = self.task(operation, workstream)
        return self.cli("claim", "--task", task["task_id"], "--agent", agent)["claim"]


    def complete(self, claim: dict[str, Any], packet: dict[str, Any], *, success: bool = True) -> dict[str, Any]:
        """Submit a distinct JSON packet so retries cannot hide persisted state errors."""
        self.packet_number += 1
        path = self.write(f"{self.session}/result-{self.packet_number}.json", json.dumps(packet))
        return self.cli("complete", "--claim", claim["id"], "--agent", claim["agent"],
                        "--result", path, success=success)


    def perform(self, operation: str, packet: dict[str, Any], agent: str = "manager",
                workstream: str | None = None) -> None:
        """Claim and complete one valid handoff while leaving the packet visible."""
        self.complete(self.claim(operation, agent, workstream), packet)


    def findings(self, count: int) -> list[dict[str, str]]:
        """Create distinct, evidence-backed findings for separate test outcomes."""
        return [{"id": f"F{number}", "authority": "AI_SPACE/SPEC.md", "expected": "Correct addition",
                 "actual": f"Fault {number}", "evidence": self.report, "severity": "major"}
                for number in range(1, count + 1)]


    def workstreams(self, count: int) -> list[dict[str, Any]]:
        """Create one independent outcome per source finding."""
        return [{"id": f"W{number}", "findings": [f"F{number}"], "outcome": f"Correct outcome {number}",
                 "depends_on": [], "work_type": "FIX.ALIGNMENT", "workflow_class": "STANDARD"}
                for number in range(1, count + 1)]


    def batch(self, count: int = 1) -> None:
        """Open a session and take a reviewed finding set through explicit selection."""
        self.cli("init")
        self.perform("conformance", {"operation": "conformance", "verdict": "FINDINGS", "coverage": "full",
                                     "report": self.report, "findings": self.findings(count)})
        self.perform("collate", {"operation": "collate", "verdict": "COLLATED",
                                 "workstreams": self.workstreams(count)})
        self.perform("select", {"operation": "select", "verdict": "SELECTED",
                                "workstreams": [f"W{number}" for number in range(1, count + 1)]})


    def plan_packet(self, workstream: str = "W1", plan_id: str = "P1", *,
                    writes: list[str] | None = None, reads: list[str] | None = None,
                    resources: list[str] | None = None, preflight: str = "SKIPPED") -> dict[str, Any]:
        """Write a durable plan and declare its worker role and reservations."""
        path = self.write(f"{self.session}/{plan_id}.md",
                          f"# {plan_id}\nWorkstream {workstream}.\nCorrect addition and validate its result.\n")
        return {"operation": "planning", "verdict": "PLANNED", "plan_id": plan_id, "path": path,
                "write_scope": ["src/add.py"] if writes is None else writes,
                "read_scope": [] if reads is None else reads, "resources": resources or [],
                "implementation_agent": "repo-engineer", "preflight": preflight}


    def plan(self, workstream: str = "W1", plan_id: str = "P1", **policy: Any) -> dict[str, Any]:
        """Submit a plan through the planner instance, with explicit scopes when required."""
        packet = self.plan_packet(workstream, plan_id, **policy)
        self.perform("planning", packet, f"planner-{workstream}", workstream)
        return packet


    def review_packet(self, operation: str, plan_id: str, verdict: str) -> dict[str, str]:
        """Bind a review verdict to one exact plan and an existing evidence document."""
        return {"operation": operation, "verdict": verdict, "plan_id": plan_id, "evidence": self.report}


    def accept_plan(self, workstream: str = "W1", plan_id: str = "P1") -> None:
        """Accept the specified current plan using an independent instance."""
        self.perform("plan_review", self.review_packet("plan_review", plan_id, "ACCEPT"),
                     f"plan-reviewer-{workstream}", workstream)


    def implementation_packet(self, plan_id: str = "P1", changed: list[str] | None = None,
                              exit_code: int = 0) -> dict[str, Any]:
        """Build submitted validation facts for tests that do not claim a real code fix."""
        log = self.write(f"{self.session}/{plan_id}-validation.log", f"Recorded exit code: {exit_code}\n")
        return {"operation": "implementation", "verdict": "IMPLEMENTED", "plan_id": plan_id,
                "changed_files": ["src/add.py"] if changed is None else changed, "report": self.report,
                "validation": [{"argv": [sys.executable, "-c", "pass"], "exit_code": exit_code, "log": log}]}


    def test_complete_batch_edits_source_runs_validation_and_requires_fresh_conformance(self) -> None:
        """Prove a real edit crosses all gates and survives new processes before DONE."""
        self.batch()
        self.plan()
        self.accept_plan()
        claim = self.claim("implementation", "worker-W1", "W1")
        self.write("src/add.py", "def add(a, b):\n    return a + b\n")
        argv = [sys.executable, "-c",
                "import runpy; add = runpy.run_path('src/add.py')['add']; assert add(7, 4) == 11; print('PASS')"]
        validation = subprocess.run(argv, cwd=self.repo, capture_output=True, text=True, timeout=20)
        self.assertEqual(validation.returncode, 0, validation.stderr)
        log = self.write(f"{self.session}/real-validation.log", validation.stdout + validation.stderr)
        packet = self.implementation_packet()
        packet["validation"] = [{"argv": argv, "exit_code": validation.returncode, "log": log}]
        self.complete(claim, packet)
        self.perform("implementation_review",
                     self.review_packet("implementation_review", "P1", "ACCEPT_IMPLEMENTATION"),
                     "implementation-reviewer", "W1")
        self.cli("status")
        self.task("conformance")
        self.perform("conformance", {"operation": "conformance", "verdict": "PASS", "coverage": "full",
                                     "report": self.report, "findings": []}, "fresh-reviewer")
        self.assertEqual(self.cli("next")["status"], "DONE")
        self.cli("invalidate", "--reason", "The maintainer changed source outside the protocol")
        self.task("conformance")


    def test_malformed_results_cannot_consume_claim_or_finish_session(self) -> None:
        """Reject incomplete, contradictory and unknown output with the claim intact."""
        self.cli("init")
        claim = self.claim("conformance", "reviewer")
        valid = {"operation": "conformance", "verdict": "PASS", "coverage": "full",
                 "report": self.report, "findings": []}
        missing = dict(valid)
        del missing["findings"]
        for packet in [missing, dict(valid, verdict="DONE"), dict(valid, extra="unknown"),
                       dict(valid, coverage="partial"), dict(valid, findings=self.findings(1)),
                       dict(valid, report="AI_SPACE/missing.md"), dict(valid, operation="plan_review")]:
            with self.subTest(packet=packet):
                self.complete(claim, packet, success=False)
                self.assertEqual(self.cli("next")["status"], "WAITING")
        impostor = dict(claim, agent="another-instance")
        self.complete(impostor, valid, success=False)
        self.complete(claim, valid)
        self.assertEqual(self.cli("next")["status"], "DONE")


    def test_rejection_requires_new_plan_and_independent_current_plan_reviews(self) -> None:
        """Neither stale acceptance nor a worker reviewing itself can advance the loop."""
        self.batch()
        self.plan()
        task = self.task("plan_review", "W1")
        self.cli("claim", "--task", task["task_id"], "--agent", "planner-W1", success=False)
        review = self.claim("plan_review", "reviewer", "W1")
        self.complete(review, self.review_packet("plan_review", "old-plan", "ACCEPT"), success=False)
        self.complete(review, self.review_packet("plan_review", "P1", "REJECT"))
        planner = self.claim("planning", "planner-W1", "W1")
        self.complete(planner, self.plan_packet(), success=False)
        self.complete(planner, self.plan_packet(plan_id="P2"))
        review = self.claim("plan_review", "reviewer", "W1")
        self.complete(review, self.review_packet("plan_review", "P1", "ACCEPT"), success=False)
        self.complete(review, self.review_packet("plan_review", "P2", "ACCEPT"))
        claim = self.claim("implementation", "worker-W1", "W1")
        self.complete(claim, self.implementation_packet("P1"), success=False)
        self.complete(claim, dict(self.implementation_packet("P2"), validation=[]), success=False)
        self.complete(claim, self.implementation_packet("P2"))
        task = self.task("implementation_review", "W1")
        self.cli("claim", "--task", task["task_id"], "--agent", "worker-W1", success=False)
        review = self.claim("implementation_review", "reviewer", "W1")
        self.complete(review, self.review_packet("implementation_review", "P1", "ACCEPT_IMPLEMENTATION"),
                      success=False)
        self.complete(review, self.review_packet("implementation_review", "P2", "REJECT_IMPLEMENTATION"))
        self.task("planning", "W1")


    def test_changed_plan_text_is_rejected_before_acceptance_and_before_writing(self) -> None:
        """A reviewed identifier cannot authorise different plan text after submission."""
        self.batch()
        packet = self.plan()
        original = (self.repo / packet["path"]).read_text()
        review = self.claim("plan_review", "reviewer", "W1")
        self.write(packet["path"], original + "Undeclared change.\n")
        self.complete(review, self.review_packet("plan_review", "P1", "ACCEPT"), success=False)
        self.write(packet["path"], original)
        self.complete(review, self.review_packet("plan_review", "P1", "ACCEPT"))
        task = self.task("implementation", "W1")
        self.write(packet["path"], original + "Another undeclared change.\n")
        self.cli("claim", "--task", task["task_id"], "--agent", "worker-W1", success=False)


    def test_required_preflight_is_a_real_gate(self) -> None:
        """The optional default permits SKIPPED while required policy needs PASS."""
        config = self.repo / ".agents/workflow/workflow.toml"
        config.write_text(config.read_text().replace('preflight = "optional"', 'preflight = "required"'))
        self.batch()
        planner = self.claim("planning", "planner-W1", "W1")
        self.complete(planner, self.plan_packet(), success=False)
        self.complete(planner, self.plan_packet(preflight="PASS"))
        self.accept_plan()
        self.task("implementation", "W1")


    def test_scope_and_resource_conflicts_serialize_and_source_changes_invalidate_plans(self) -> None:
        """Conflicting work waits and stale read assumptions force renewed planning."""
        self.batch(3)
        self.plan("W1", "P1", writes=["src/shared.py"], resources=["gpu"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/shared.py"])
        self.plan("W3", "P3", writes=["src/independent.py"], resources=["gpu"])
        for number in range(1, 4):
            self.accept_plan(f"W{number}", f"P{number}")
        tasks = {task["workstream_id"]: task for task in self.cli("next")["tasks"]}
        claim = self.claim("implementation", "worker-W1", "W1")
        for workstream in ["W2", "W3"]:
            self.cli("claim", "--task", tasks[workstream]["task_id"], "--agent", f"worker-{workstream}",
                     success=False)
        self.write("src/shared.py", "value = 1\n")
        self.complete(claim, self.implementation_packet("P1", ["src/shared.py"]))
        self.task("planning", "W2")
        self.perform("implementation_review",
                     self.review_packet("implementation_review", "P1", "ACCEPT_IMPLEMENTATION"),
                     "reviewer-W1", "W1")
        self.claim("implementation", "worker-W3", "W3")


    def test_source_change_invalidates_an_overlapping_queued_implementation_review(self) -> None:
        """A completed implementation cannot be accepted using a now-stale dependency."""
        self.batch(2)
        self.plan("W1", "P1", writes=["src/shared.py"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/shared.py"])
        self.accept_plan("W1", "P1")
        self.accept_plan("W2", "P2")
        self.perform("implementation", self.implementation_packet("P2", ["src/other.py"]), "worker-W2", "W2")
        stale_review = self.task("implementation_review", "W2")
        self.perform("implementation", self.implementation_packet("P1", ["src/shared.py"]), "worker-W1", "W1")
        self.task("planning", "W2")
        self.cli("claim", "--task", stale_review["task_id"], "--agent", "reviewer-W2", success=False)


    def test_interrupted_implementation_blocks_and_resumes_through_planning(self) -> None:
        """Release preserves partial-edit uncertainty and invalidates overlapping plans."""
        self.batch(2)
        self.plan("W1", "P1", writes=["src/shared.py"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/shared.py"])
        self.accept_plan("W1", "P1")
        self.accept_plan("W2", "P2")
        claim = self.claim("implementation", "worker-W1", "W1")
        self.write("src/shared.py", "partial = True\n")
        self.cli("invalidate", "--reason", "Cannot invalidate live work", success=False)
        self.cli("release", "--claim", claim["id"], "--agent", claim["agent"],
                 "--reason", "Worker stopped after a partial edit")
        self.task("planning", "W2")
        ready = self.cli("next")["tasks"]
        self.assertFalse(any(task.get("workstream_id") == "W1" for task in ready), ready)
        self.cli("resume", "--workstream", "W1", "--reason", "Partial edits inspected and replanning is safe")
        self.task("planning", "W1")


    def test_explicit_blocking_never_counts_as_clean_completion(self) -> None:
        """An unavailable global review must be explicitly resumed with a reason."""
        self.cli("init")
        self.perform("conformance", {"operation": "conformance", "verdict": "BLOCKED",
                                     "reason": "Required evidence is unavailable"}, "reviewer")
        self.assertEqual(self.cli("next")["status"], "BLOCKED")
        self.cli("resume", "--reason", "", success=False)
        self.cli("resume", "--reason", "Required evidence is available")
        self.task("conformance")


    def test_concurrent_claims_keep_both_reservations_and_reject_duplicates(self) -> None:
        """Independent processes cannot overwrite another claim during atomic updates."""
        self.batch(2)
        for number in [1, 2]:
            self.plan(f"W{number}", f"P{number}", writes=[f"src/module{number}.py"])
        for number in [1, 2]:
            self.accept_plan(f"W{number}", f"P{number}")
        tasks = {task["workstream_id"]: task for task in self.cli("next")["tasks"]}
        processes = [subprocess.Popen(self.command("claim", "--task", tasks[f"W{number}"]["task_id"],
                                                  "--agent", f"worker-W{number}"),
                                      cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                     for number in [1, 2]]
        claims = []
        for process in processes:
            stdout, stderr = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, stdout + stderr)
            claims.append(json.loads(stdout)["claim"])
        self.assertEqual(self.cli("next")["status"], "WAITING")
        self.cli("claim", "--task", tasks["W1"]["task_id"], "--agent", "worker-W1", success=False)
        for claim in claims:
            self.cli("release", "--claim", claim["id"], "--agent", claim["agent"],
                     "--reason", "Concurrent reservation verified")
        self.assertEqual(self.cli("next")["status"], "BLOCKED")


    def test_failed_validation_cannot_receive_implementation_acceptance(self) -> None:
        """A review can reject failed validation but cannot declare it accepted."""
        self.batch()
        self.plan()
        self.accept_plan()
        self.perform("implementation", self.implementation_packet(exit_code=1), "worker-W1", "W1")
        review = self.claim("implementation_review", "reviewer", "W1")
        self.complete(review, self.review_packet("implementation_review", "P1", "ACCEPT_IMPLEMENTATION"),
                      success=False)
        self.complete(review, self.review_packet("implementation_review", "P1", "REJECT_IMPLEMENTATION"))
        self.task("planning", "W1")


    def test_literal_scopes_reject_escape_and_out_of_plan_changed_files(self) -> None:
        """Only portable repo paths inside accepted write roots may be submitted."""
        self.batch()
        planner = self.claim("planning", "planner-W1", "W1")
        for scope in ["../outside.py", "/absolute.py", "src/*.py", "src/../outside.py"]:
            with self.subTest(scope=scope):
                self.complete(planner, self.plan_packet(writes=[scope]), success=False)
        self.complete(planner, self.plan_packet(writes=["src"]))
        self.accept_plan()
        worker = self.claim("implementation", "worker-W1", "W1")
        self.complete(worker, self.implementation_packet(changed=["src_extra/file.py"]), success=False)
        self.complete(worker, self.implementation_packet(changed=["src/nested/file.py"]))
        self.task("implementation_review", "W1")


    def test_one_instance_cannot_claim_two_parallel_tasks(self) -> None:
        """Agent capacity counts actual active instances, including planning work."""
        self.batch(2)
        first = self.claim("planning", "planner", "W1")
        second_task = self.task("planning", "W2")
        self.cli("claim", "--task", second_task["task_id"], "--agent", "planner", success=False)
        second = self.claim("planning", "different-planner", "W2")
        self.complete(first, self.plan_packet("W1", "P1", writes=["src/one.py"]))
        self.complete(second, self.plan_packet("W2", "P1", writes=["src/two.py"]))
        self.task("plan_review", "W1")
        self.task("plan_review", "W2")


    def test_authority_and_policy_are_pinned_and_unsafe_policy_fails_check(self) -> None:
        """Policy changes cannot silently alter an existing session's authority."""
        config = self.repo / ".agents/workflow/workflow.toml"
        original = config.read_text()
        for number, text in enumerate([original.replace("max_agents = 6", 'max_agents = "six"'),
                     original.replace("version = 1", "version = 1\nunknown = true"),
                     original.replace('REJECT = "planning"', 'REJECT = "implementation"'),
                     original.replace('agent = "research-architect"', 'agent = "missing-agent"'),
                     original.replace('skill = "plan"', 'skill = "missing-skill"')]):
            with self.subTest(invalid_policy=number):
                config.write_text(text)
                self.cli("check", success=False)
        config.write_text(original)
        self.cli("check")
        self.cli("init")
        authority = self.repo / "AI_SPACE/SPEC.md"
        original_authority = authority.read_text()
        authority.write_text(original_authority + "Changed requirement.\n")
        self.cli("next", success=False)
        authority.write_text(original_authority)
        config.write_text(original.replace("max_agents = 6", "max_agents = 2"))
        self.cli("next", success=False)


    def test_collation_and_selection_reject_unowned_findings_and_unresolved_dependencies(self) -> None:
        """The selected batch cannot omit finding ownership or skip its dependencies."""
        self.cli("init")
        self.perform("conformance", {"operation": "conformance", "verdict": "FINDINGS", "coverage": "full",
                                     "report": self.report, "findings": self.findings(2)})
        claim = self.claim("collate", "manager")
        streams = self.workstreams(2)
        streams[1]["findings"] = ["F1"]
        self.complete(claim, {"operation": "collate", "verdict": "COLLATED", "workstreams": streams},
                      success=False)
        streams = self.workstreams(2)
        streams[0]["depends_on"] = ["W2"]
        streams[1]["depends_on"] = ["W1"]
        self.complete(claim, {"operation": "collate", "verdict": "COLLATED", "workstreams": streams},
                      success=False)
        streams[0]["depends_on"] = []
        self.complete(claim, {"operation": "collate", "verdict": "COLLATED", "workstreams": streams})
        claim = self.claim("select", "manager")
        for selection in [[], ["W1", "W1"], ["W1", "W2"], ["W2"]]:
            self.complete(claim, {"operation": "select", "verdict": "SELECTED", "workstreams": selection},
                          success=False)
        self.complete(claim, {"operation": "select", "verdict": "SELECTED", "workstreams": ["W1"]})
        self.task("planning", "W1")


if __name__ == "__main__":
    unittest.main()
