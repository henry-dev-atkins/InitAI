"""Exercise the file protocol through fresh CLI processes and real repository work.

Run from the repository root with Python 3.11 or newer:
    python -m unittest discover -s .agents/workflow/tests -v
"""

from __future__ import annotations

import json
import hashlib
import importlib.util
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
        ignore_bytecode = shutil.ignore_patterns("__pycache__", "*.pyc")
        shutil.copytree(ROOT / ".agents/skills", self.repo / ".agents/skills", ignore=ignore_bytecode)
        shutil.copytree(ROOT / ".codex/agents", self.repo / ".codex/agents", ignore=ignore_bytecode)
        shutil.copytree(ROOT / ".agents/workflow", self.repo / ".agents/workflow", ignore=ignore_bytecode)
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
        return [sys.executable, "-B", str(RUNNER), operation, "--repo", str(self.repo),
                "--session", self.session, *arguments]


    def cli(self, operation: str, *arguments: str, success: bool = True) -> dict[str, Any]:
        """Run a fresh process and require both JSON output and the expected exit status."""
        normalised_arguments = list(arguments)
        for index, value in enumerate(normalised_arguments[:-1]):
            if value == "--workstream":
                normalised_arguments[index + 1] = self.canonical_workstream(normalised_arguments[index + 1])
        arguments = tuple(normalised_arguments)
        process = subprocess.run(self.command(operation, *arguments), cwd=self.repo,
                                 capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode == 0, success,
                         f"{operation}: exit {process.returncode}\n{process.stdout}\n{process.stderr}")
        try:
            result = json.loads(process.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"CLI did not return JSON: {error}\n{process.stdout}\n{process.stderr}")
        for task in result.get("tasks", []):
            if (task.get("workstream_id") or "").startswith("WS"):
                task["workstream_id"] = f"W{int(task['workstream_id'][2:])}"
        self.assertEqual(result["ok"], success, result)
        return result


    def canonical_workstream(self, value: str) -> str:
        """Translate compact fixture names to the current workflow identifier format."""
        if value.startswith("WS"):
            return value
        return f"WS{int(value[1:]):03d}" if value.startswith("W") else value


    def canonical_plan(self, value: str) -> str:
        """Translate compact fixture names to the current plan identifier format."""
        return f"P{int(value[1:]):03d}" if value.startswith("P") else value


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
        self.cli("agent-open", "--agent", agent, "--role", "test-worker")
        return self.cli("claim", "--task", task["task_id"], "--agent", agent)["claim"]


    def complete(self, claim: dict[str, Any], packet: dict[str, Any], *, success: bool = True) -> dict[str, Any]:
        """Submit a distinct JSON packet so retries cannot hide persisted state errors."""
        self.packet_number += 1
        if packet.get("operation") == "collate":
            for item in packet.get("workstreams", []):
                item["id"] = self.canonical_workstream(item["id"])
                item["depends_on"] = [self.canonical_workstream(value) for value in item.get("depends_on", [])]
        elif packet.get("operation") == "select":
            packet["workstreams"] = [self.canonical_workstream(value) for value in packet["workstreams"]]
        path = self.write(f"{self.session}/result-{self.packet_number}.json", json.dumps(packet))
        result = self.cli("complete", "--claim", claim["id"], "--agent", claim["agent"],
                          "--result", path, success=success)
        if success:
            self.cli("agent-close", "--agent", claim["agent"])
        return result


    def perform(self, operation: str, packet: dict[str, Any], agent: str = "manager",
                workstream: str | None = None) -> None:
        """Claim and complete one valid handoff while leaving the packet visible."""
        if operation == "collate":
            for item in packet.get("workstreams", []):
                item["id"] = self.canonical_workstream(item["id"])
                item["depends_on"] = [self.canonical_workstream(value) for value in item.get("depends_on", [])]
        elif operation == "select":
            packet["workstreams"] = [self.canonical_workstream(value) for value in packet["workstreams"]]
        self.complete(self.claim(operation, agent, workstream), packet)


    def findings(self, count: int) -> list[dict[str, str]]:
        """Create distinct, evidence-backed findings for separate test outcomes."""
        return [{"id": f"F{number:03d}", "authority": "AI_SPACE/SPEC.md", "expected": "Correct addition",
                 "actual": f"Fault {number}", "evidence": self.report, "severity": "major"}
                for number in range(1, count + 1)]


    def workstreams(self, count: int) -> list[dict[str, Any]]:
        """Create one independent outcome per source finding."""
        return [{"id": f"WS{number:03d}", "findings": [f"F{number:03d}"], "outcome": f"Correct outcome {number}",
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
                    resources: list[str] | None = None, preflight: str = "PASS") -> dict[str, Any]:
        """Write a durable plan and declare its worker role and reservations."""
        workstream_id = self.canonical_workstream(workstream)
        current_plan_id = self.canonical_plan(plan_id)
        finding_id = f"F{int(workstream_id[2:]):03d}"
        writes = ["src/add.py"] if writes is None else writes
        reads = [] if reads is None else reads
        resources = resources or []
        manifest_path = f"{self.session}/{current_plan_id}-manifest.json"
        manifest = {
            "schema": "plan-command-manifest.v1",
            "workstream_id": workstream_id,
            "plan_id": current_plan_id,
            "commands": [{
                "id": "CMD001", "argv": [sys.executable, "-c", "print('ok')"], "cwd": ".",
                "purpose": "validate the workflow fixture", "phase": "final-validation",
                "expected_status": "pass", "timeout_seconds": 30,
                "requirement_ids": ["REQ001"], "finding_ids": [finding_id],
                "artefact_paths": [], "temp_root": f"temp/workflow/{workstream_id}",
                "requires_existing_paths": [".agents/skills/orchestrator/assets/plan-template.md"],
            }],
        }
        self.write(manifest_path, json.dumps(manifest, indent=2))
        manifest_hash = hashlib.sha256((self.repo / manifest_path).read_bytes()).hexdigest()
        scope_lines = "\n".join(f"- `{value}`" for value in writes)
        read_lines = "\n".join(f"- `{value}`" for value in reads) or "- none"
        path = self.write(f"{self.session}/{current_plan_id}.md", f"""# Workstream Plan

## Identity and Traceability

- Workstream ID: {workstream_id}
- Plan ID: {current_plan_id}
- Predecessor plan: none
- Failed assumption from predecessor: none
- Material causal delta: none
- Source findings: {finding_id}
- Requirement IDs: REQ001
- Spec authority: AI_SPACE/SPEC.md
- Owner agent: planner
- Workflow class: STANDARD

## Work Classification

- Primary Work Type: `FIX.ALIGNMENT`
- Counts as capability progress: no
- Supporting changes: workflow fixture

## Mission

Correct the fixture behaviour and validate the result.

## Scope and Contracts

Write scope:
{scope_lines}

Stable read assumptions:
{read_lines}

Off-limits:
- `AI_SPACE/SPEC.md`

Dependencies:
- none

Contracts changed:
- none

Contracts consumed:
- none

Mutable resources:
{chr(10).join(f"- `{value}`" for value in resources) or "- none"}

## Protected Invariants / Must Not

- Keep the authority unchanged.

## Command Manifest

- Path: `{manifest_path}`
- SHA-256: `{manifest_hash}`

The manifest is the only command source of truth.

## Implementation Steps

1. Apply the declared fixture change.

## Validation and Resolution Evidence

| Command ID | Requirement IDs | Finding IDs | Proof |
|---|---|---|---|
| CMD001 | REQ001 | {finding_id} | Proves the declared validation command runs. |

## Risks and Assumptions

- The fixture is isolated.

## Result Packet Contract

Return the runner-produced validation ledger.

## Executive Summary

Fixture plan for workflow tests.

## Am I going in Circles?

No repeated repair loop is present.

## Is there a more elegant way of doing this?

A single command is the simplest route.
""")
        return {"operation": "planning", "verdict": "PLANNED", "plan_id": current_plan_id, "path": path,
                "write_scope": ["src/add.py"] if writes is None else writes,
                "read_scope": reads, "resources": resources,
                "requirement_ids": ["REQ001"], "off_limits_scope": ["AI_SPACE/SPEC.md"],
                "contracts_changed": [], "contracts_consumed": [], "dependencies": [],
                "implementation_agent": "repo-engineer", "preflight": preflight}


    def plan(self, workstream: str = "W1", plan_id: str = "P1", **policy: Any) -> dict[str, Any]:
        """Submit a plan through the planner instance, with explicit scopes when required."""
        packet = self.plan_packet(workstream, plan_id, **policy)
        self.perform("planning", packet, f"planner-{workstream}", workstream)
        return packet


    def review_packet(self, operation: str, plan_id: str, verdict: str) -> dict[str, str]:
        """Bind a review verdict to one exact plan and an existing evidence document."""
        return {"operation": operation, "verdict": verdict, "plan_id": self.canonical_plan(plan_id), "evidence": self.report}


    def accept_plan(self, workstream: str = "W1", plan_id: str = "P1") -> None:
        """Accept the specified current plan using an independent instance."""
        self.perform("plan_review", self.review_packet("plan_review", plan_id, "ACCEPT"),
                     f"plan-reviewer-{workstream}", workstream)


    def implementation_packet(self, plan_id: str = "P1", changed: list[str] | None = None,
                              exit_code: int = 0) -> dict[str, Any]:
        """Build submitted validation facts for tests that do not claim a real code fix."""
        current_plan_id = self.canonical_plan(plan_id)
        changed_files = ["src/add.py"] if changed is None else changed
        for relative in changed_files:
            path = self.repo / relative
            if not path.exists():
                self.write(relative, "# workflow fixture change\n")
        manifest_path = self.repo / self.session / f"{current_plan_id}-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if exit_code:
            manifest["commands"][0]["argv"] = [sys.executable, "-c", "raise SystemExit(1)"]
            manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        workstream_id = manifest["workstream_id"]
        ledger_path = f"{self.session}/{current_plan_id}-ledger.json"
        manifest_relative = f"{self.session}/{current_plan_id}-manifest.json"
        subprocess.run([sys.executable, "-B", str(self.repo / ".agents/skills/orchestrator/scripts/run_command_manifest.py"),
                        "--manifest", manifest_relative, "--ledger", ledger_path,
                        "--workstream", workstream_id, "--plan-id", current_plan_id, "--repo-root", str(self.repo)],
                       cwd=self.repo, capture_output=True, text=True, check=False, timeout=20)
        return {"operation": "implementation", "verdict": "IMPLEMENTED", "plan_id": current_plan_id,
                "changed_files": changed_files, "report": self.report,
                "validation_ledger": ledger_path}


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
        packet["validation_ledger"] = packet["validation_ledger"]
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
        self.assertEqual(self.cli("next")["status"], "WAITING")


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
        self.complete(planner, self.plan_packet(preflight="SKIPPED"), success=False)
        self.complete(planner, self.plan_packet(preflight="PASS"))
        self.accept_plan()
        self.task("implementation", "W1")


    def test_plan_preflight_function_is_directly_callable(self) -> None:
        """The CLI and runner can share one side-effect-free preflight function."""
        self.batch()
        packet = self.plan_packet()
        module_path = self.repo / ".agents/skills/orchestrator/scripts/validate_plan_preflight.py"
        spec = importlib.util.spec_from_file_location("fixture_plan_preflight", module_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(module_path.parent))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.remove(str(module_path.parent))
        errors = module.validate_plan(
            repo=self.repo,
            plan_path=self.repo / packet["path"],
            plan_text=(self.repo / packet["path"]).read_text(encoding="utf-8"),
            manifest_path=self.repo / self.session / "P001-manifest.json",
            parent_session=self.repo / self.session,
            workstream_id="WS001",
            plan_id="P001",
            expected_findings=["F001"],
            expected_requirements=["REQ001"],
            allowed_write_scope=["src/add.py"],
            stable_read_scope=[],
            off_limits_scope=["AI_SPACE/SPEC.md"],
            contracts_changed=[],
            contracts_consumed=[],
            mutable_resources=[],
            dependencies=[],
        )
        self.assertEqual(errors, [])


    def test_command_timeout_fails_and_stops_later_commands(self) -> None:
        """Timeouts fail the ledger and prevent later commands from running."""
        self.cli("init")
        manifest_path = self.write(f"{self.session}/timeout-manifest.json", json.dumps({
            "schema": "plan-command-manifest.v1",
            "workstream_id": "WS001",
            "plan_id": "P001",
            "commands": [
                {"id": "CMD001", "argv": [sys.executable, "-c", "import time; time.sleep(2)"],
                 "cwd": ".", "purpose": "timeout test", "phase": "final-validation",
                 "expected_status": "pass", "timeout_seconds": 1,
                 "requirement_ids": ["REQ001"], "finding_ids": ["F001"]},
                {"id": "CMD002", "argv": [sys.executable, "-c", "raise SystemExit(99)"],
                 "cwd": ".", "purpose": "must not run", "phase": "final-validation",
                 "expected_status": "pass", "timeout_seconds": 1,
                 "requirement_ids": ["REQ001"], "finding_ids": ["F001"]},
            ],
        }))
        ledger_path = f"{self.session}/timeout-ledger.json"
        runner = self.repo / ".agents/skills/orchestrator/scripts/run_command_manifest.py"
        process = subprocess.run(
            [sys.executable, "-B", str(runner), "--manifest", manifest_path,
             "--ledger", ledger_path, "--workstream", "WS001", "--plan-id", "P001",
             "--repo-root", str(self.repo)],
            cwd=self.repo, capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(process.returncode, 1, process.stderr)
        ledger = json.loads((self.repo / ledger_path).read_text(encoding="utf-8"))
        self.assertEqual(ledger["status"], "FAIL")
        self.assertTrue(ledger["commands"][0]["timed_out"])
        self.assertEqual(ledger["commands"][0]["exit_code"], 124)
        self.assertEqual(ledger["commands"][1]["status"], "NOT_RUN")

        ledger["status"] = "PASS"
        ledger["commands"][0]["status"] = "PASS"
        tampered = self.write(f"{self.session}/timeout-ledger-pass.json", json.dumps(ledger))
        validator = self.repo / ".agents/skills/orchestrator/scripts/validate_evidence_ledger.py"
        invalid = subprocess.run(
            [sys.executable, "-B", str(validator), tampered, "--repo-root", str(self.repo)],
            cwd=self.repo, capture_output=True, text=True, timeout=20,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("timed out command cannot pass", invalid.stdout)


    def test_old_state_requires_a_fresh_session(self) -> None:
        """A state file from the previous contract cannot continue silently."""
        self.cli("init")
        state_path = self.repo / self.session / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["version"] = 1
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        response = self.cli("status", success=False)
        self.assertIn("version", response["error"])


    def test_standard_command_policy_and_obsolete_helpers(self) -> None:
        """Required command forms remain explicit and obsolete helpers are archived."""
        rules = (ROOT / ".codex/rules/dev-checks.rules").read_text(encoding="utf-8")
        commit_rules = (ROOT / ".codex/rules/orchestrator-final-commit.rules").read_text(encoding="utf-8")
        self.assertIn('"uv sync"', rules)
        self.assertIn('"uv python --version"', rules)
        self.assertIn('"uv run python -m unittest discover -s .agents/workflow/tests -v"', rules)
        self.assertIn("./tools/orchestrator_final_commit.ps1", commit_rules)
        self.assertNotIn('pattern = ["git", "commit"]',
                          (ROOT / ".codex/rules/team-orchestration.rules").read_text(encoding="utf-8"))
        active_scripts = list((ROOT / ".agents/skills/orchestrator/scripts").glob("*.py"))
        archived_scripts = list((ROOT / "AI_SPACE/archive/superseded/skills-orchestrator/scripts").glob("*.py"))
        self.assertEqual(len(archived_scripts), 2)
        self.assertTrue(
            {path.name for path in archived_scripts}.isdisjoint({path.name for path in active_scripts})
        )


    def test_scope_and_resource_conflicts_serialize_and_source_changes_invalidate_plans(self) -> None:
        """Conflicting work waits and stale read assumptions force renewed planning."""
        self.batch(3)
        self.plan("W1", "P1", writes=["src/shared.py"], resources=["gpu"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/unrelated.py"])
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
        self.task("implementation", "W2")


    def test_source_change_invalidates_an_overlapping_queued_implementation_review(self) -> None:
        """A completed implementation cannot be accepted using a now-stale dependency."""
        self.batch(2)
        self.plan("W1", "P1", writes=["src/shared.py"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/unrelated.py"])
        self.accept_plan("W1", "P1")
        self.accept_plan("W2", "P2")
        self.task("implementation", "W1")
        self.task("implementation", "W2")


    def test_interrupted_implementation_blocks_and_resumes_through_planning(self) -> None:
        """Release preserves partial-edit uncertainty and invalidates overlapping plans."""
        self.batch(2)
        self.plan("W1", "P1", writes=["src/shared.py"])
        self.plan("W2", "P2", writes=["src/other.py"], reads=["src/unrelated.py"])
        self.accept_plan("W1", "P1")
        self.accept_plan("W2", "P2")
        claim = self.claim("implementation", "worker-W1", "W1")
        self.write("src/shared.py", "partial = True\n")
        self.cli("invalidate", "--reason", "Cannot invalidate live work", success=False)
        self.cli("release", "--claim", claim["id"], "--agent", claim["agent"],
                 "--reason", "Worker stopped after a partial edit")
        self.task("implementation", "W2")
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
        for number in [1, 2]:
            self.cli("agent-open", "--agent", f"worker-W{number}", "--role", "test-worker")
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
        """A failed ledger cannot advance to implementation review."""
        self.batch()
        self.plan()
        self.accept_plan()
        claim = self.claim("implementation", "worker-W1", "W1")
        self.complete(claim, self.implementation_packet(exit_code=1))
        self.assertEqual(self.cli("next")["status"], "BLOCKED")


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
        self.complete(worker, self.implementation_packet(changed=["src_extra/file.py"]))
        self.assertEqual(self.cli("next")["status"], "BLOCKED")


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
