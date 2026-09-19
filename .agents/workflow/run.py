#!/usr/bin/env python3
"""Check workflow handoffs and persist resumable session state."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import tomllib
from typing import Any, Iterator


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ORCHESTRATOR_SCRIPTS = HERE.parent / "skills/orchestrator/scripts"
if str(ORCHESTRATOR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ORCHESTRATOR_SCRIPTS))

from workflow_common import (  # noqa: E402
    diff_inventories,
    repository_inventory,
    repository_tree_hash,
)
from validate_plan_preflight import validate_plan  # noqa: E402


GLOBAL_OPERATIONS = {"conformance", "collate", "select"}
STATE_VERSION = 2
AUDIT_EXCLUDES = (".git", "AI_SPACE/sessions", "temp")


class WorkflowError(Exception):
    """Report a rejected CLI request without modifying the saved session."""


class UnexpectedRepositoryChange(WorkflowError):
    """Report a repository change that was not declared by the worker."""


def require(condition: bool, message: str) -> None:
    """Reject a false invariant with a useful error for the caller."""
    if not condition:
        raise WorkflowError(message)


def read_json(path: Path) -> Any:
    """Read one UTF-8 JSON document and reject duplicate object keys."""
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        """Build an object only when each submitted field is unambiguous."""
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON field {key!r}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)


def validate_packet(value: Any, filename: str) -> None:
    """Check a dict against the harness's existing JSON Schema subset."""
    validator_path = HERE.parent / "skills/orchestrator/scripts/schema_validation.py"
    spec = importlib.util.spec_from_file_location("workflow_schema_validation", validator_path)
    require(spec is not None and spec.loader is not None, "Schema validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    errors = module.validate(value, read_json(HERE / filename))
    require(not errors, f"{filename}: " + "; ".join(errors))


def repo_path(repo: Path, value: str) -> str:
    """Return a portable literal repo-relative path, with '.' meaning root."""
    require(isinstance(value, str) and bool(value.strip()), "Path must be nonempty text")
    require(value == value.strip(), f"Path has leading or trailing whitespace: {value!r}")
    require(not any(character in value for character in "\\:*?[]\x00\n\r"),
            f"Path must be a portable literal without globs: {value!r}")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts, f"Path must stay inside repository: {value!r}")
    relative = path.as_posix()
    resolved = (repo / relative).resolve()
    require(resolved.is_relative_to(repo), f"Path escapes repository through a symlink: {value!r}")
    # Compare resolved aliases as well as text when reserving scopes.
    return resolved.relative_to(repo).as_posix()


def evidence_file(repo: Path, value: str, markdown: bool = False) -> tuple[str, str]:
    """Read existing nonempty evidence, optionally requiring a Markdown file."""
    relative = repo_path(repo, value)
    path = repo / relative
    require(path.is_file(), f"Evidence file does not exist: {relative}")
    require(not markdown or path.suffix.lower() == ".md", "Plan path must end in .md")
    content = path.read_text(encoding="utf-8-sig")
    require(bool(content.strip()), f"Evidence file is empty: {relative}")
    return relative, content


def session_file(repo: Path, session: str, value: str, markdown: bool = False,
                 require_nonempty: bool = True) -> tuple[str, str]:
    """Read existing nonempty evidence from the active session only."""
    relative = repo_path(repo, value)
    session_path = PurePosixPath(repo_path(repo, session))
    require(PurePosixPath(relative).is_relative_to(session_path),
            f"Evidence path is outside the active session: {relative}")
    path = repo / relative
    require(path.is_file(), f"Evidence file does not exist: {relative}")
    require(not markdown or path.suffix.lower() == ".md", "Plan path must end in .md")
    content = path.read_text(encoding="utf-8-sig")
    require(not require_nonempty or bool(content.strip()), f"Evidence file is empty: {relative}")
    return relative, content


def audit_inventory(repo: Path) -> dict[str, dict[str, str]]:
    """Return source and control files that a worker must declare before completion."""
    return repository_inventory(repo, excludes=AUDIT_EXCLUDES)


def plan_manifest_path(plan_text: str) -> str:
    """Read the command manifest path from the required plan section."""
    section = re.search(
        r"^##\s+Command Manifest\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        plan_text,
        re.MULTILINE | re.DOTALL,
    )
    require(section is not None, "Plan is missing the Command Manifest section")
    match = re.search(r"^-\s*Path:\s*`?([^`\n]+)`?\s*$", section.group("body"), re.MULTILINE)
    require(match is not None, "Plan is missing the Command Manifest path")
    return match.group(1).strip()


def run_plan_preflight(
    repo: Path,
    session: str,
    plan_path: str,
    plan_text: str,
    workstream_id: str,
    plan_id: str,
    expected_findings: list[str],
    expected_requirements: list[str],
    allowed_write_scope: list[str],
    stable_read_scope: list[str],
    off_limits_scope: list[str],
    contracts_changed: list[str],
    contracts_consumed: list[str],
    mutable_resources: list[str],
    dependencies: list[str],
) -> list[str]:
    """Run the shared mechanical plan validator before semantic review."""
    manifest_path = plan_manifest_path(plan_text)
    return validate_plan(
        repo=repo,
        plan_path=repo / plan_path,
        plan_text=plan_text,
        manifest_path=repo / manifest_path,
        parent_session=repo / session,
        workstream_id=workstream_id,
        plan_id=plan_id,
        expected_findings=expected_findings,
        expected_requirements=expected_requirements,
        allowed_write_scope=allowed_write_scope,
        stable_read_scope=stable_read_scope,
        off_limits_scope=off_limits_scope,
        contracts_changed=contracts_changed,
        contracts_consumed=contracts_consumed,
        mutable_resources=mutable_resources,
        dependencies=dependencies,
    )


def roles_and_skills(repo: Path) -> tuple[set[str], set[str]]:
    """Read existing agent names and skill frontmatter for binding checks."""
    roles: set[str] = set()
    for path in (repo / ".codex/agents").glob("*.toml"):
        role = tomllib.loads(path.read_text(encoding="utf-8-sig")).get("name")
        if isinstance(role, str):
            roles.add(role)
    skill_paths: dict[str, Path] = {}
    for path in (repo / ".agents/skills").rglob("SKILL.md"):
        content = path.read_text(encoding="utf-8-sig")
        if content.startswith("---\n"):
            frontmatter = content.split("---", 2)[1]
            match = re.search(r"^name:\s*([^\n]+)", frontmatter, re.MULTILINE)
            if match:
                name = match.group(1).strip().strip("\"'")
                require(name not in skill_paths,
                        f"Duplicate skill name {name!r}: {skill_paths.get(name)} and {path}")
                skill_paths[name] = path
    return roles, set(skill_paths)


def load_workflow(repo: Path, filename: str) -> tuple[str, dict[str, Any], set[str]]:
    """Validate the policy and resolve every role and skill against this repo."""
    relative = repo_path(repo, filename)
    workflow = tomllib.loads((repo / relative).read_text(encoding="utf-8-sig"))
    validate_packet(workflow, "workflow.schema.json")
    roles, skills = roles_and_skills(repo)
    for operation, binding in workflow["operations"].items():
        require(binding["agent"] in roles, f"Unknown agent role for {operation}: {binding['agent']}")
        if "skill" in binding:
            require(binding["skill"] in skills, f"Unknown skill for {operation}: {binding['skill']}")
    return relative, workflow, roles


@contextmanager
def session_lock(session: Path) -> Iterator[None]:
    """Hold one OS advisory lock across reading and replacing session state."""
    with (session / ".lock").open("a+b") as handle:
        if handle.tell() == 0:
            handle.write(b"\0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def save_state(session: Path, state: dict[str, Any]) -> None:
    """Flush a complete UTF-8 state file before atomically replacing the old one."""
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=session,
                                         prefix=".state-", suffix=".tmp", delete=False) as handle:
            temporary = handle.name
            json.dump(state, handle, indent=2, ensure_ascii=False, allow_nan=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, session / "state.json")
    finally:
        if temporary is not None and Path(temporary).exists():
            Path(temporary).unlink()


def overlap(first: str, second: str) -> bool:
    """Treat each literal scope as its path and all descendants, conservatively."""
    first_path, second_path = PurePosixPath(first.casefold()), PurePosixPath(second.casefold())
    return first_path.is_relative_to(second_path) or second_path.is_relative_to(first_path)


def reservations(task: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    """Return declared read, write and exclusive resource reservations for a task."""
    operation = task["operation"]
    if operation in GLOBAL_OPERATIONS or operation == "planning":
        return ["."], [], []
    plan = task["plan"]
    if operation == "implementation":
        return plan["read_scope"], plan["write_scope"], plan["resources"]
    return plan["read_scope"] + plan["write_scope"], [], plan["resources"]


def conflict(first: dict[str, Any], second: dict[str, Any]) -> bool:
    """Reject write/read overlaps and shared exclusive resources between claims."""
    first_reads, first_writes, first_resources = reservations(first)
    second_reads, second_writes, second_resources = reservations(second)
    if set(first_resources) & set(second_resources):
        return True
    return (any(overlap(write, other) for write in first_writes for other in second_reads + second_writes)
            or any(overlap(write, read) for write in second_writes for read in first_reads))


def validate_selected_plan_set(state: dict[str, Any]) -> None:
    """Reject path overlaps between current plans before implementation starts."""
    plans = [
        state["workstreams"][identifier]["plan"]
        for identifier in state["selected"]
        if state["workstreams"][identifier]["plan"] is not None
    ]
    for left, right in combinations(plans, 2):
        path_overlap = any(
            overlap(write, other)
            for write in left["write_scope"]
            for other in right["read_scope"] + right["write_scope"]
        ) or any(
            overlap(write, other)
            for write in right["write_scope"]
            for other in left["read_scope"]
        )
        require(not path_overlap,
                "Selected plans have overlapping read/write scopes")


def task_packet(state: dict[str, Any], operation: str, workstream_id: str | None = None) -> dict[str, Any]:
    """Describe one permitted task with pinned authority and its current plan."""
    binding = state["workflow"]["operations"][operation]
    task: dict[str, Any] = {
        "task_id": f"{state['cycle']}:global:{operation}", "operation": operation,
        "workstream_id": workstream_id, "agent_role": binding["agent"],
        "skill": binding.get("skill"), "authority": state["authority"],
        "result_schema": ".agents/workflow/results.schema.json",
        }
    if workstream_id is not None:
        workstream = state["workstreams"][workstream_id]
        task["task_id"] = f"{state['cycle']}:{workstream_id}:{workstream['attempt']}:{operation}"
        task["workstream"] = {key: workstream[key] for key in
                              ("id", "findings", "outcome", "depends_on", "work_type", "workflow_class")}
        if workstream["plan"] is not None:
            task["plan"] = workstream["plan"]
        if workstream.get("implementation") is not None:
            task["implementation"] = workstream["implementation"]
        if operation == "implementation":
            task["agent_role"] = workstream["plan"]["implementation_agent"]
        task["reason"] = workstream.get("reason")
    elif operation == "collate":
        task["findings"] = state["findings"]
    elif operation == "select":
        task["workstreams"] = list(state["workstreams"].values())
        task["max_agents"] = state["workflow"]["max_agents"]
    return task


def next_tasks(state: dict[str, Any]) -> dict[str, Any]:
    """List unclaimed tasks whose reservations fit the current active claims."""
    candidates: list[dict[str, Any]] = []
    if state["stage"] == "done":
        return {"ok": True, "status": "DONE", "tasks": []}
    if state["stage"] in GLOBAL_OPERATIONS and state["global_blocked"] is None:
        candidates.append(task_packet(state, state["stage"]))
    elif state["stage"] == "batch":
        for identifier in state["selected"]:
            workstream = state["workstreams"][identifier]
            if workstream["stage"] != "accepted" and workstream["blocked"] is None:
                candidates.append(task_packet(state, workstream["stage"], identifier))
    claims = list(state["claims"].values())
    available = [task for task in candidates if all(
                 task["task_id"] != claim["task"]["task_id"] and not conflict(task, claim["task"])
                 for claim in claims)]
    live_agents = sum(
        item["status"] == "live"
        for item in state.get("agents", {}).values()
    )
    if live_agents >= state["workflow"]["max_agents"]:
        available = []
    status = "READY" if available else "WAITING" if claims else "BLOCKED"
    return {"ok": True, "status": status, "tasks": available}


def current_plan(repo: Path, workstream: dict[str, Any], plan_id: str | None = None) -> dict[str, Any]:
    """Require the current plan's identifier and submitted Markdown text to match."""
    plan = workstream["plan"]
    require(plan is not None, "Workstream has no current plan")
    require(plan_id is None or plan_id == plan["plan_id"], "Result must name the current plan_id")
    _, text = evidence_file(repo, plan["path"], markdown=True)
    require(text == plan["text"], "Plan text changed. Release and resume the task, or invalidate the session")
    return plan


def replan(workstream: dict[str, Any], reason: str) -> None:
    """Discard previous gates while preserving the reason for a new planning attempt."""
    workstream.update(stage="planning", plan=None, planner=None, implementer=None,
                      implementation=None, blocked=None, reason=reason)
    workstream["attempt"] += 1


def invalidate_overlaps(state: dict[str, Any], writer: str, changed_files: list[str], reason: str) -> None:
    """Replan pending work whose assumptions overlap submitted or interrupted edits."""
    for identifier in state["selected"]:
        workstream = state["workstreams"][identifier]
        plan = workstream["plan"]
        if identifier != writer and workstream["stage"] != "accepted" and plan is not None:
            if any(overlap(changed, scope) for changed in changed_files
                   for scope in plan["read_scope"] + plan["write_scope"]):
                require(not any(claim["task"]["workstream_id"] == identifier
                                for claim in state["claims"].values()),
                        "Overlapping active task exists. Reservation invariants were violated")
                replan(workstream, reason)
                state["history"].append({"event": "plan_invalidated", "workstream_id": identifier,
                                         "reason": reason})


def block_task(state: dict[str, Any], task: dict[str, Any], reason: str) -> None:
    """Pause one task and invalidate overlapping assumptions after possible partial writes."""
    identifier = task["workstream_id"]
    blocked = {"operation": task["operation"], "reason": reason}
    if identifier is None:
        state["global_blocked"] = blocked
    else:
        workstream = state["workstreams"][identifier]
        workstream["blocked"] = blocked
        workstream["reason"] = reason
        if task["operation"] == "implementation":
            invalidate_overlaps(state, identifier, workstream["plan"]["write_scope"],
                                f"Possible partial writes in {identifier}: {reason}")


def validate_collation(state: dict[str, Any], result: dict[str, Any]) -> None:
    """Check exact finding ownership and an acyclic graph of durable workstreams."""
    workstreams = result["workstreams"]
    identifiers = [workstream["id"] for workstream in workstreams]
    require(len(set(identifiers)) == len(identifiers), "Workstream IDs must be unique")
    owned = [identifier for workstream in workstreams for identifier in workstream["findings"]]
    require(len(set(owned)) == len(owned), "Each finding must have exactly one workstream owner")
    require(set(owned) == {finding["id"] for finding in state["findings"]},
            "Collation must own every current finding exactly once, with no unknown findings")
    remaining = {workstream["id"]: set(workstream["depends_on"]) for workstream in workstreams}
    for identifier, dependencies in remaining.items():
        require(dependencies <= set(identifiers) and identifier not in dependencies,
                f"Invalid dependencies for {identifier}")
    while remaining:
        ready = {identifier for identifier, dependencies in remaining.items() if not dependencies}
        require(bool(ready), "Workstream dependencies contain a cycle")
        remaining = {identifier: dependencies - ready for identifier, dependencies in remaining.items()
                     if identifier not in ready}


def normalise_plan(repo: Path, state: dict[str, Any], result: dict[str, Any], roles: set[str],
                   workstream_id: str) -> dict[str, Any]:
    """Validate one new plan and pin its current text with normalised reservations."""
    require(f"{workstream_id}:{result['plan_id']}" not in state["plan_ids"],
            "plan_id must be unique for this workstream across the session")
    implementation_agent = result.get("implementation_agent", state["workflow"]["operations"]["implementation"]["agent"])
    require(implementation_agent in roles, "Unknown implementation_agent")
    require(result["preflight"] == "PASS", "Workflow policy requires preflight PASS")
    plan = dict(result)
    plan["implementation_agent"] = implementation_agent
    plan["path"], plan["text"] = session_file(
        repo,
        state["session"],
        result["path"],
        markdown=True,
    )
    preflight_errors = run_plan_preflight(
        repo,
        state["session"],
        plan["path"],
        plan["text"],
        workstream_id,
        result["plan_id"],
        state["workstreams"][workstream_id]["findings"],
        result.get("requirement_ids", []),
        result["write_scope"],
        result["read_scope"],
        result.get("off_limits_scope", []),
        result.get("contracts_changed", []),
        result.get("contracts_consumed", []),
        result["resources"],
        result.get("dependencies", []),
    )
    require(not preflight_errors, "Plan preflight failed: " + "; ".join(preflight_errors))
    for key in ("write_scope", "read_scope"):
        plan[key] = [repo_path(repo, value) for value in result[key]]
        require(len(plan[key]) == len(set(plan[key])), f"Duplicate normalised paths in {key}")
        require(not any(overlap(path, "AI_SPACE") for path in plan[key]),
                f"Worker scope cannot include AI_SPACE: {key}")
    for resource in plan["resources"]:
        require(resource == resource.strip(), "Resource names must not have surrounding whitespace")
    if plan["write_scope"]:
        matching = [tomllib.loads(path.read_text(encoding="utf-8-sig"))
                    for path in (repo / ".codex/agents").glob("*.toml")]
        role = next(item for item in matching if item.get("name") == plan["implementation_agent"])
        require(role.get("sandbox_mode") in {"workspace-write", "danger-full-access"},
                "A plan with write_scope requires a write-capable implementation_agent")
    return plan


def apply_result(repo: Path, state: dict[str, Any], claim: dict[str, Any],
                 result: dict[str, Any], roles: set[str]) -> None:
    """Check the current operation's facts, then advance exactly one permitted gate."""
    validate_packet(result, "results.schema.json")
    task = claim["task"]
    operation, identifier = task["operation"], task["workstream_id"]
    require(result["operation"] == operation, "Result operation does not match the claim")
    observed = diff_inventories(claim["audit_inventory"], audit_inventory(repo))
    observed_paths = sorted(observed["added"] + observed["modified"] + observed["deleted"])
    if operation != "implementation" and observed_paths:
        raise UnexpectedRepositoryChange(
            f"Non-implementation task changed repository paths: {observed_paths}"
        )
    verdict = result["verdict"]
    target = state["workflow"]["operations"][operation]["transitions"][verdict]
    workstream = state["workstreams"].get(identifier)
    if verdict == "BLOCKED":
        block_task(state, task, result["reason"])
    elif operation == "conformance":
        session_file(repo, state["session"], result["report"])
        findings = result["findings"]
        ids = [finding["id"] for finding in findings]
        require(len(set(ids)) == len(ids), "Finding IDs must be unique")
        require((verdict == "PASS") == (len(findings) == 0),
                "PASS requires an explicit empty findings list. FINDINGS requires at least one finding")
        state["findings"] = findings
        state["stage"] = target
    elif operation == "collate":
        validate_collation(state, result)
        state["workstreams"] = {item["id"]: {**item, "stage": "pending", "attempt": 0,
                                "plan_rejections": 0,
                                "plan": None, "planner": None, "implementer": None,
                                "implementation": None, "blocked": None, "reason": None}
                                for item in result["workstreams"]}
        state["selected"] = []
        state["stage"] = target
    elif operation == "select":
        selected = result["workstreams"]
        require(len(selected) <= state["workflow"]["max_agents"], "Selection exceeds max_agents")
        require(all(identifier in state["workstreams"] for identifier in selected),
                "Selection contains an unknown workstream")
        for identifier in selected:
            workstream = state["workstreams"][identifier]
            require(all(state["workstreams"][dependency]["stage"] == "accepted"
                        for dependency in workstream["depends_on"]),
                    f"Selected workstream has unresolved dependencies: {identifier}")
            workstream["stage"] = target
            workstream["attempt"] = 1
        state["selected"] = selected
        state["stage"] = "batch"
    elif operation == "planning":
        plan = normalise_plan(repo, state, result, roles, identifier)
        workstream.update(plan=plan, planner=claim["agent"], stage=target)
        state["plan_ids"].append(f"{identifier}:{plan['plan_id']}")
    elif operation == "plan_review":
        current_plan(repo, workstream, result["plan_id"])
        session_file(repo, state["session"], result["evidence"])
        require(claim["agent"] != workstream["planner"], "Plan reviewer must differ from the planner instance")
        if verdict == "REJECT":
            workstream["plan_rejections"] += 1
            rejection_reason = f"Plan rejected. Evidence: {result['evidence']}"
            if workstream["plan_rejections"] >= state["workflow"]["max_plan_rejections"]:
                workstream["blocked"] = {
                    "operation": "plan_review",
                    "reason": "Plan rejection threshold reached. Diagnosis evidence is required.",
                    "evidence": result["evidence"],
                }
                workstream["reason"] = workstream["blocked"]["reason"]
            else:
                replan(workstream, rejection_reason)
        else:
            validate_selected_plan_set(state)
            workstream["stage"] = target
    elif operation == "implementation":
        plan = current_plan(repo, workstream, result["plan_id"])
        changes = [repo_path(repo, value) for value in result["changed_files"]]
        require(len(changes) == len(set(changes)), "Duplicate normalised changed_files")
        observed = diff_inventories(claim["audit_inventory"], audit_inventory(repo))
        observed_paths = sorted(observed["added"] + observed["modified"] + observed["deleted"])
        if observed_paths != sorted(changes):
            raise UnexpectedRepositoryChange(
                "Repository changes do not match changed_files: "
                f"observed={observed_paths}; declared={sorted(changes)}"
            )
        for changed in changes:
            if not any(PurePosixPath(changed).is_relative_to(PurePosixPath(scope))
                       for scope in plan["write_scope"]):
                raise UnexpectedRepositoryChange(f"Changed file is outside write_scope: {changed}")
            if (repo / changed).is_dir():
                raise UnexpectedRepositoryChange(f"changed_files must name files: {changed}")
            for protected in ("AI_SPACE", state["workflow_path"], state["authority"]["path"], state["session"]):
                if overlap(changed, protected):
                    raise UnexpectedRepositoryChange(
                        f"Changed file is protected workflow state or authority: {changed}"
                    )
        session_file(repo, state["session"], result["report"])
        ledger = session_file(repo, state["session"], result["validation_ledger"])[0]
        ledger_data = read_json(repo / ledger)
        evidence_paths = [ledger_data.get("manifest_path", "")]
        for command in ledger_data.get("commands", []):
            evidence_paths.extend([command.get("stdout_path", ""), command.get("stderr_path", "")])
            evidence_paths.extend(artefact.get("path", "") for artefact in command.get("artefacts", []))
        for evidence_path in evidence_paths:
            require(bool(evidence_path), "Validation ledger contains an empty evidence path")
            session_file(repo, state["session"], evidence_path, require_nonempty=False)
        ledger_validator = HERE.parent / "skills/orchestrator/scripts/validate_evidence_ledger.py"
        ledger_check = subprocess.run(
            [sys.executable, "-B", str(ledger_validator), ledger, "--repo-root", str(repo)],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        require(ledger_check.returncode == 0,
                "Validation ledger failed: "
                + (ledger_check.stdout + ledger_check.stderr).strip())
        require(ledger_data.get("status") == "PASS",
                "Implementation requires a passing validation ledger")
        require(ledger_data.get("repository_tree_hash_after") == repository_tree_hash(repo),
                "Validation ledger does not describe the current repository tree")
        result["validation_ledger"] = ledger
        result["changed_files"] = changes
        result["observed_changes"] = observed_paths
        invalidate_overlaps(state, identifier, changes, f"Completed writes in {identifier}: {', '.join(changes)}")
        workstream.update(implementation=result, implementer=claim["agent"], stage=target)
    elif operation == "implementation_review":
        current_plan(repo, workstream, result["plan_id"])
        session_file(repo, state["session"], result["evidence"])
        require(claim["agent"] != workstream["implementer"],
                "Implementation reviewer must differ from the implementer instance")
        if verdict == "ACCEPT_IMPLEMENTATION":
            require(workstream["implementation"] is not None
                    and workstream["implementation"]["validation_ledger"],
                    "Acceptance requires passing recorded validation")
            workstream["stage"] = target
        else:
            replan(workstream, f"Implementation rejected. Evidence: {result['evidence']}")
    state["history"].append({"event": "complete", "claim_id": claim["id"], "agent": claim["agent"],
                             "task_id": task["task_id"], "result": result})
    if operation == "planning" and verdict == "PLANNED":
        state["history"][-1]["plan_text"] = workstream["plan"]["text"]
    if state["stage"] == "batch" and all(state["workstreams"][item]["stage"] == "accepted"
                                         for item in state["selected"]):
        state["stage"] = "conformance"
        state["cycle"] += 1


def run_command(args: argparse.Namespace) -> dict[str, Any]:
    """Execute one CLI operation under the session lock, saving only valid changes."""
    repo = Path(args.repo).resolve()
    require(repo.is_dir(), f"Repository does not exist: {repo}")
    workflow_path, workflow, roles = load_workflow(repo, args.workflow)
    if args.command == "check":
        return {"ok": True, "workflow": workflow}
    require(args.session is not None, "--session is required for this command")
    session_relative = repo_path(repo, args.session)
    session = repo / session_relative
    session_root = repo / "AI_SPACE/sessions"
    require(session.is_relative_to(session_root) and session != session_root,
            "--session must name a directory inside AI_SPACE/sessions")
    if args.command == "init":
        session.mkdir(parents=True, exist_ok=True)
    require(session.is_dir(), "Session does not exist. Run init first")
    with session_lock(session):
        state_path = session / "state.json"
        if args.command == "init":
            require(not state_path.exists(), "Session already exists. Use its saved state or choose a new session")
            authority_path, authority_text = evidence_file(repo, args.authority)
            if (repo / "AI_SPACE/SPEC.md").is_file():
                require(authority_path == repo_path(repo, "AI_SPACE/SPEC.md"),
                        "AI_SPACE/SPEC.md is present and must be the authority")
            state: dict[str, Any] = {
                "version": STATE_VERSION, "repo": str(repo), "session": session_relative,
                "workflow_path": workflow_path, "workflow": workflow,
                "authority": {"path": authority_path, "text": authority_text},
                "stage": "conformance", "cycle": 1, "claims": {}, "next_claim": 1,
                "findings": [], "workstreams": {}, "selected": [], "plan_ids": [],
                "agents": {},
                "global_blocked": None, "history": [],
                }
            save_state(session, state)
            return {"ok": True, "state": state}
        state = read_json(state_path)
        require(state["version"] == STATE_VERSION and state["repo"] == str(repo)
                and state["session"] == session_relative, "State belongs to another repository, session or version")
        require(state["workflow_path"] == workflow_path and state["workflow"] == workflow,
                "Workflow policy changed. Start a fresh session explicitly")
        _, authority_text = evidence_file(repo, state["authority"]["path"])
        require(authority_text == state["authority"]["text"], "Authority text changed. Start a fresh session explicitly")
        if (repo / "AI_SPACE/SPEC.md").is_file():
            require(state["authority"]["path"] == repo_path(repo, "AI_SPACE/SPEC.md"),
                    "Project spec was added. Start a fresh session with that authority")
        if args.command == "status":
            return {"ok": True, "state": state}
        elif args.command == "next":
            return next_tasks(state)
        elif args.command == "agent-open":
            require(bool(args.agent.strip()) and "\n" not in args.agent,
                    "--agent must name an actual agent instance")
            existing_agent = state["agents"].get(args.agent)
            require(existing_agent is None or existing_agent["status"] in {"idle", "closed"},
                    "Agent instance is already live or busy")
            live_agents = sum(item["status"] == "live" for item in state["agents"].values())
            require(live_agents < state["workflow"]["max_agents"],
                    "Agent capacity is full")
            state["agents"][args.agent] = {
                "role": args.role,
                "kind": args.kind,
                "status": "live",
                "claim_id": None,
            }
            response = {"ok": True, "agent": state["agents"][args.agent]}
        elif args.command == "agent-close":
            require(args.agent in state["agents"], "Unknown agent instance")
            record = state["agents"][args.agent]
            require(record["status"] == "idle", "Agent must be idle before closure")
            record["status"] = "closed"
            response = {"ok": True, "agent": record}
        elif args.command == "claim":
            require(bool(args.agent.strip()) and "\n" not in args.agent, "--agent must name an actual agent instance")
            require(args.agent in state["agents"], "Agent must be opened before claiming work")
            require(state["agents"][args.agent]["status"] == "live",
                    "Agent is not live")
            require(state["agents"][args.agent]["claim_id"] is None,
                    "Agent already has an active claim")
            require(all(claim["agent"] != args.agent for claim in state["claims"].values()),
                    "Agent instance already has an active claim")
            task = next((task for task in next_tasks(state)["tasks"] if task["task_id"] == args.task), None)
            require(task is not None, "Task is not available. Run next for current permitted tasks")
            if task["workstream_id"] is not None:
                workstream = state["workstreams"][task["workstream_id"]]
                if task["operation"] != "planning":
                    current_plan(repo, workstream)
                if task["operation"] == "plan_review":
                    require(args.agent != workstream["planner"], "Plan reviewer must differ from the planner instance")
                elif task["operation"] == "implementation_review":
                    require(args.agent != workstream["implementer"],
                            "Implementation reviewer must differ from the implementer instance")
            claim_id = f"C{state['next_claim']:06d}"
            claim = {
                "id": claim_id,
                "agent": args.agent,
                "task": task,
                "audit_inventory": audit_inventory(repo),
            }
            state["claims"][claim_id] = claim
            state["agents"][args.agent]["status"] = "busy"
            state["agents"][args.agent]["claim_id"] = claim_id
            state["next_claim"] += 1
            response = {"ok": True, "claim": claim}
        elif args.command in {"complete", "release"}:
            require(args.claim in state["claims"], "Unknown or completed claim")
            claim = state["claims"][args.claim]
            require(claim["agent"] == args.agent, "Claim belongs to another agent instance")
            if args.command == "complete":
                result = read_json(repo / session_file(repo, state["session"], args.result)[0])
                try:
                    apply_result(repo, state, claim, result, roles)
                except UnexpectedRepositoryChange as exc:
                    block_task(state, claim["task"], str(exc))
                    state["history"].append({
                        "event": "unexpected_repository_change",
                        "claim_id": args.claim,
                        "reason": str(exc),
                    })
                    state["agents"][args.agent]["status"] = "idle"
                    state["agents"][args.agent]["claim_id"] = None
                    del state["claims"][args.claim]
                    response = next_tasks(state)
                else:
                    state["agents"][args.agent]["status"] = "idle"
                    state["agents"][args.agent]["claim_id"] = None
                    del state["claims"][args.claim]
                    response = next_tasks(state)
            else:
                require(bool(args.reason.strip()), "Release requires a nonempty reason")
                block_task(state, claim["task"], args.reason)
                state["history"].append({"event": "release", "claim_id": args.claim, "reason": args.reason})
                state["agents"][args.agent]["status"] = "idle"
                state["agents"][args.agent]["claim_id"] = None
                del state["claims"][args.claim]
                response = next_tasks(state)
        elif args.command == "resume":
            require(bool(args.reason.strip()), "Resume requires a nonempty reason")
            if args.workstream is None:
                require(state["global_blocked"] is not None, "No global task is blocked")
                state["global_blocked"] = None
            else:
                require(args.workstream in state["selected"], "Workstream is not in the current batch")
                workstream = state["workstreams"][args.workstream]
                require(workstream["blocked"] is not None, "Workstream is not blocked")
                stale = False
                if workstream["plan"] is not None:
                    try:
                        current_plan(repo, workstream)
                    except (WorkflowError, OSError, UnicodeError):
                        stale = True
                if workstream["blocked"]["operation"] == "implementation" or stale:
                    replan(workstream, f"Resumed through planning: {args.reason}")
                elif workstream["blocked"]["operation"] == "plan_review":
                    require(args.diagnosis_evidence is not None,
                            "Plan rejection threshold requires diagnosis evidence")
                    evidence_path, _ = session_file(
                        repo,
                        state["session"],
                        args.diagnosis_evidence,
                        markdown=True,
                    )
                    workstream["plan_rejections"] = 0
                    workstream["blocked"] = None
                    workstream["reason"] = args.reason
                    replan(workstream, f"Resumed through planning: {args.reason}")
                    state["history"].append({
                        "event": "plan_rejection_diagnosis",
                        "workstream_id": args.workstream,
                        "evidence": evidence_path,
                    })
                else:
                    workstream["blocked"] = None
                    workstream["reason"] = args.reason
            state["history"].append({"event": "resume", "workstream_id": args.workstream, "reason": args.reason})
            response = next_tasks(state)
        elif args.command == "invalidate":
            require(not state["claims"], "Release all active claims before invalidating the session")
            require(bool(args.reason.strip()), "Invalidation requires a nonempty reason")
            state.update(stage="conformance", global_blocked=None, selected=[], findings=[], workstreams={})
            state["cycle"] += 1
            state["history"].append({"event": "invalidate", "reason": args.reason})
            response = next_tasks(state)
        else:
            raise WorkflowError(f"Unknown command: {args.command}")
        save_state(session, state)
        return response


class JsonArgumentParser(argparse.ArgumentParser):
    """Keep invalid CLI invocations on the same JSON error contract as runtime checks."""

    def error(self, message: str) -> None:
        """Raise one user-facing error instead of argparse's text exit."""
        raise WorkflowError(message)


def main() -> int:
    """Parse one command and print JSON with exit 0 for success or 1 for rejection."""
    parser = JsonArgumentParser(description=__doc__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--repo", default=".")
    common.add_argument("--workflow", default=".agents/workflow/workflow.toml")
    common.add_argument("--session")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "init", "status", "next", "agent-open", "agent-close",
                 "claim", "complete", "release", "resume", "invalidate"):
        command = commands.add_parser(name, parents=[common])
        if name == "init":
            command.add_argument("--authority", default="AI_SPACE/SPEC.md")
        elif name == "claim":
            command.add_argument("--task", required=True)
            command.add_argument("--agent", required=True)
        elif name in {"agent-open", "agent-close"}:
            command.add_argument("--agent", required=True)
            if name == "agent-open":
                command.add_argument("--role", required=True)
                command.add_argument("--kind", choices=["workflow", "supporting"], default="workflow")
        elif name in {"complete", "release"}:
            command.add_argument("--claim", required=True)
            command.add_argument("--agent", required=True)
            if name == "complete":
                command.add_argument("--result", required=True)
        if name in {"release", "resume", "invalidate"}:
            command.add_argument("--reason", required=True)
        if name == "resume":
            command.add_argument("--workstream")
            command.add_argument("--diagnosis-evidence")
    try:
        result = run_command(parser.parse_args())
    except (WorkflowError, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
