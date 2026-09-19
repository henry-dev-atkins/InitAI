# Workflow DSL v1

This adds checked handoffs and saved state to the existing spec-convergence loop. 
Run from the repository root with Python 3.11 or newer. 
No third-party packages are required.

```sh
python .agents/workflow/run.py check --repo .
```

The TOML file owns mechanical policy. 
The Python runner validates results, reserves tasks and advances the fixed loop. 
Existing Markdown skills own planning and review judgement. 
The orchestrator launches agents and runs tools through its normal environment.

## Files and changes

| File | Purpose |
| --- | --- |
| `workflow.toml` | Operation bindings, policy and permitted verdict transitions. |
| `workflow.schema.json` | Exact v1 configuration shape and invariant gates. |
| `results.schema.json` | Exact result shapes for all seven operations and blocking. |
| `run.py` | Standard-library CLI with checked transitions and resumable state. |
| `tests/test_workflow.py` | Executable workflow, rejection, conflict and recovery tests. |

The harness routing, team guide, orchestrator instructions, skill map, plan-review skill and task-packet template now use this protocol. 
Preflight is required for every plan.
The runner checks the saved plan and command manifest before semantic review.

## Policy

Read `workflow.toml` for the complete procedural definition; do not duplicate its transitions in other configuration. This is one fixed convergence workflow, not a general graph language.

| Field | Allowed change |
| --- | --- |
| `name` | Nonempty workflow name. |
| `max_agents` | Capacity from 1 to 6. |
| `max_plan_rejections` | Plan-review rejection threshold from 1 to 3. |
| `preflight` | `required`. The runner executes mechanical preflight and accepts only `PASS`. |
| `operations.<operation>.agent` | An existing agent role from `.codex/agents/`. |
| `operations.<operation>.skill` | An existing skill frontmatter name, for operations that use a skill. |
| `version`, `independent_reviews`, `completion`, transitions | Fixed v1 invariants; unsafe changes are rejected. |

Run `check` after changing policy. Unknown fields, roles, skills and verdict transitions fail validation. A planning result may override its implementation role through `implementation_agent`; when omitted, it uses `operations.implementation.agent` from the TOML file.

The parsed configuration and authority text are pinned at session creation. Changing either requires a new explicit session; there is no silent migration. Skills and agent instruction files are not frozen by the runner.

## Start and dispatch

The default authority is `AI_SPACE/SPEC.md`. Create a unique session:

```sh
python .agents/workflow/run.py init --repo . --session AI_SPACE/sessions/session__20260909_160000
python .agents/workflow/run.py next --repo . --session AI_SPACE/sessions/session__20260909_160000
python .agents/workflow/run.py agent-open --repo . --session AI_SPACE/sessions/session__20260909_160000 --agent ACTUAL_INSTANCE_ID --role repo-engineer
```

If the spec is absent, `AGENTS.md` permits an explicit human prompt only when it supplies concrete intent and acceptance criteria. Save that exact authority in a repository-local text file, then pass its path with `init --authority PATH`. Do not invent substitute authority.

All session commands use `--repo` and `--session`; `--workflow` selects a repository-relative TOML file and defaults to `.agents/workflow/workflow.toml`. Sessions must be below `AI_SPACE/sessions/`. Paths use `/`, are repository-relative and cannot contain traversal, absolute paths, backslashes or globs.

`next` returns `status` and `tasks`. A task has `task_id`, `operation`, `workstream_id`, `agent_role`, `skill` and the relevant authority/workstream/plan context. Copy IDs from returned data. Reuse an idle agent instance or allocate a standby instance with explicit instructions to await dispatch without starting repository work. Obtain its actual instance ID, claim the task with that ID, and dispatch work to that same instance only after the claim succeeds. Role names are not instance identities.

The following is a command template; replace its uppercase IDs and result path with actual returned values:

```sh
python .agents/workflow/run.py claim --repo . --session AI_SPACE/sessions/session__20260909_160000 --task TASK_ID --agent ACTUAL_INSTANCE_ID
python .agents/workflow/run.py complete --repo . --session AI_SPACE/sessions/session__20260909_160000 --claim CLAIM_ID --agent ACTUAL_INSTANCE_ID --result AI_SPACE/sessions/session__20260909_160000/results/conformance.json
```

`claim` returns `claim.id`, `claim.agent` and `claim.task`. The caller dispatches that task to the reserved instance with assigned session paths. Read-only workers return exact plan/report/review content and result fields; the orchestrator saves that content and the result JSON at those paths, then submits `complete` using the original claim ID and worker instance ID. Saving a review does not make the orchestrator its author. Preserve returned facts and verdicts exactly; missing content must be obtained from the worker, not invented. If the claim fails, the standby instance must remain idle. `next` alone does not reserve work.

Write-capable workers may save files only where their accepted scope and existing permissions already allow it. They can return remaining session content for the orchestrator to save. This handoff uses the orchestrator's existing control-file authority and gives it no project source-writing authority. Keep returned file content separate from the result JSON; do not add content fields that the result schema does not support.

The default `conformance-reviewer` role handles two explicit operations: `conformance` uses `$conformance`; `plan_review` uses `$plan-review`. Dispatch the returned operation and skill together so that the reviewer uses the correct verdict contract.

Call `next` after each result. `READY` means tasks are available; `WAITING` means outstanding claims must settle; `BLOCKED` requires an explicit resolution; `DONE` means a fresh full conformance review returned `PASS` with an explicit empty findings list. Missing results never mean success.

| Command | Additional arguments | Effect |
| --- | --- | --- |
| `check` | No session needed. | Validate policy and resolve role/skill bindings. |
| `init` | Optional `--authority PATH`. | Create a session with pinned policy and authority. |
| `status` | None. | Return the saved state. |
| `next` | None. | Show permitted, currently available tasks. |
| `agent-open` | `--agent INSTANCE --role ROLE`, optional `--kind supporting`. | Register a live workflow or supporting agent. |
| `agent-close` | `--agent INSTANCE`. | Close an idle registered agent. |
| `claim` | `--task ID --agent INSTANCE`. | Reserve a task and its declared scopes/resources. |
| `complete` | `--claim ID --agent INSTANCE --result PATH`. | Validate and record one result, then advance state. |
| `release` | `--claim ID --agent INSTANCE --reason TEXT`. | Mark an interrupted claim blocked. |
| `resume` | `--reason TEXT`, optionally `--workstream ID`. | Resume a resolved block; omit workstream for a global operation. |
| `invalidate` | `--reason TEXT`. | With no active claims, discard reliance on old acceptance and require fresh conformance. |

Commands return JSON with `ok`; failures return a JSON error and a nonzero exit code. Do not edit state to bypass an error.

## Minimal session

A DSL session needs `state.json`, plans, result JSON and the evidence those results reference. Use a layout such as:

```text
AI_SPACE/sessions/session__20260909_160000/
  state.json
  plans/WS001__P001.md
  results/conformance.json
  results/planning__WS001__P001.json
  evidence/conformance.md
  evidence/plan-review__WS001__P001.md
  evidence/implementation__WS001__P001.md
  evidence/implementation-review__WS001__P001.md
  evidence/validation__WS001__P001.log
```

Create only files needed by the work. The runner creates its state and lock. The orchestrator saves exact content returned by read-only planners and reviewers; write-capable workers save only files permitted by their accepted scope and existing permissions. Use a new evidence filename for each attempt/review. Markdown findings and workstream summaries are optional readable views of the saved state, not another authority.

## Result examples

Each block is a complete JSON shape for one operation. Replace example facts with actual findings and evidence. The orchestrator saves the returned result as a separate JSON file when the worker is read-only, along with its exact returned plan/report/review content. Plans, reports and review evidence must exist and be nonempty before `complete`; the plan must be Markdown. Validation logs must exist and may be empty when the actual command produced no output. A current claim supplies the workstream, so result packets do not repeat `workstream_id`. Unsupported extra fields are rejected.

Conformance must cover the full relevant authority. `FINDINGS` requires at least one finding; `PASS` requires `findings: []`.

```json
{
  "operation": "conformance",
  "verdict": "FINDINGS",
  "coverage": "full",
  "report": "AI_SPACE/sessions/session__20260909_160000/evidence/conformance.md",
  "findings": [{
    "id": "F001",
    "authority": "AI_SPACE/SPEC.md: empty input behaviour",
    "expected": "An empty batch returns an empty result.",
    "actual": "Processing an empty batch raises IndexError.",
    "evidence": "src/batch.py indexes the first item before checking its length.",
    "severity": "major"
  }]
}
```

Collation gives every current finding exactly one owner. Dependencies must refer to other workstreams and form an acyclic graph. Work type and class follow `AGENTS.md`.

```json
{
  "operation": "collate",
  "verdict": "COLLATED",
  "workstreams": [{
    "id": "WS001",
    "findings": ["F001"],
    "outcome": "Empty batches return an empty result.",
    "depends_on": [],
    "work_type": "FIX.ALIGNMENT",
    "workflow_class": "STANDARD"
  }]
}
```

Selection contains one to `max_agents` distinct ready workstreams. Unresolved dependencies cannot be selected together as if they were independent.

```json
{"operation": "select", "verdict": "SELECTED", "workstreams": ["WS001"]}
```

The plan text contains the reasoning and requirements from `$plan`. The packet carries its identity and mechanical declarations. The `(workstream_id, plan_id)` pair is unique across the session history, including rejected plans and later cycles. Different workstreams may each start at `P001`; one workstream cannot reuse its earlier ID. Revise into a new ID and file. `resources` contains caller-defined exclusive resource names; use the same name for the same git checkout, GPU or other shared resource across plans. The optional `implementation_agent` below is a role override; omit it to use the TOML default.

```json
{
  "operation": "planning",
  "verdict": "PLANNED",
  "plan_id": "P001",
  "path": "AI_SPACE/sessions/session__20260909_160000/plans/WS001__P001.md",
  "write_scope": ["src/batch.py", "tests/test_batch.py"],
  "read_scope": ["src/batch.py", "pyproject.toml"],
  "resources": [],
  "requirement_ids": ["REQ001"],
  "off_limits_scope": ["AI_SPACE/SPEC.md"],
  "contracts_changed": [],
  "contracts_consumed": [],
  "dependencies": [],
  "implementation_agent": "repo-engineer",
  "preflight": "PASS"
}
```

Scopes are literal files or directory roots; `.` reserves the repository root. Scope comparisons are conservatively case-insensitive for Windows portability. Resource names are exact, case-sensitive identifiers. Paths need not exist yet when a plan creates new files. The runner saves the submitted plan text and rejects stale edits before review or implementation. Plan preflight is mandatory and runs before semantic review.

Plan review is performed by an actual instance different from the planner. Replace `ACCEPT` with `REJECT` for a rejected plan and give concrete evidence; rejection returns to planning.

```json
{
  "operation": "plan_review",
  "verdict": "ACCEPT",
  "plan_id": "P001",
  "evidence": "AI_SPACE/sessions/session__20260909_160000/evidence/plan-review__WS001__P001.md"
}
```

Implementation reports every changed file in its authorised scope and submits a runner-produced validation ledger. The command manifest is the command source of truth. The reviewer must assess whether the ledger proves the required behaviour.

```json
{
  "operation": "implementation",
  "verdict": "IMPLEMENTED",
  "plan_id": "P001",
  "changed_files": ["src/batch.py", "tests/test_batch.py"],
  "report": "AI_SPACE/sessions/session__20260909_160000/evidence/implementation__WS001__P001.md",
  "validation_ledger": "AI_SPACE/sessions/session__20260909_160000/evidence/evidence_ledger__WS001__P001.json"
}
```

Implementation review uses an actual instance different from the implementer. Acceptance requires the current accepted plan and passing recorded validation. `REJECT_IMPLEMENTATION` returns to planning and clears the old acceptance. Implementation failure is always planning failure.

```json
{
  "operation": "implementation_review",
  "verdict": "ACCEPT_IMPLEMENTATION",
  "plan_id": "P001",
  "evidence": "AI_SPACE/sessions/session__20260909_160000/evidence/implementation-review__WS001__P001.md"
}
```

After the selected batch, the runner requires fresh conformance. A clean review is explicit:

```json
{
  "operation": "conformance",
  "verdict": "PASS",
  "coverage": "full",
  "report": "AI_SPACE/sessions/session__20260909_160000/evidence/conformance-final.md",
  "findings": []
}
```

Any operation may instead return exactly this blocked shape, using its own operation name:

```json
{"operation": "implementation", "verdict": "BLOCKED", "reason": "The required project dataset is unavailable."}
```

## Conflicts, recovery and limits

At most `max_agents` registered agents may be live, with one task per instance. Declared write/write and read/write overlaps and equal resource names conflict. Global and planning operations hold a conservative whole-repository read reservation. Reviews hold the plan's read/write scopes as read reservations and reserve its resources. Undeclared semantic dependencies remain the orchestrator's responsibility.

The runner records live workflow and supporting agents. Open an agent before claiming work. Close an idle agent when it finishes. Supporting agents count against `max_agents`.

An implementation result invalidates other pending plans whose declared scopes overlap its submitted changed files, including queued implementation reviews. Interrupted or blocked implementation uses its whole authorised write scope because partial changes are unknown. The runner records the reason and routes those workstreams back to planning. Plans produced after the writes are unaffected.

State replacement is atomic and protected by an OS advisory lock. Outstanding claims survive process restarts. Do not assume the worker stopped merely because the caller did. Confirm it has stopped, then `release` the interrupted claim. After resolving the need, `resume --workstream WS001 --reason "..."` resumes that workstream. Interrupted implementation always resumes through planning. There are no automatic source-writing retries.

The runner records an inventory at every claim and compares it at completion. Only implementation tasks may change repository paths, and their declared files must match exactly. It does not launch or authenticate models, execute worker validation commands, or intercept platform writes. An unexpected repository change blocks the task before the next gate. Declared scopes do not grant OS or tool access. Existing sandbox and human authority rules still apply.

For an edit outside the protocol, stop active work, release outstanding claims as needed, then run `invalidate --reason "Describe the external edit"`. This requires no active claims and returns even a completed session to fresh conformance. Do not trust old acceptance after unreported changes. Configuration or authority changes instead require a new session.

## Verify the runner

```sh
python -m unittest discover -s .agents/workflow/tests -v
```

The tests use temporary fixture repositories, including a real code edit and a real validation subprocess. They test protocol behaviour; they do not establish that a model's reasoning or a project's implementation is correct.

Recorded verification: all 15 behavioural tests passed with Python 3.12 on Linux. Windows locking is implemented but has not been exercised here.
