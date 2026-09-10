# Agent Task Packet

Use this human-readable brief alongside the exact task returned by the DSL runner. Replace template markers before dispatch. The task, current plan and `.agents/workflow/results.schema.json` define the machine handoff; this brief does not add workflow state.

## Identity

- Operation: {operation returned by `next`}
- Task ID: {task_id returned by `next`}
- Claim ID: {claim.id returned by `claim`}
- Agent instance: {actual assigned instance ID; not the role name}
- Agent role: {agent_role returned by the task}
- Parent session: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS`
- Workstream ID: {workstream_id, when present}
- Plan ID: {current plan_id, when present}
- Primary Work Type: {workstream work_type}
- Workflow class: {workstream workflow_class}
- Source findings: {finding IDs}
- Plan: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/plans/WSXXX__PXXX.md`
- Result file: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/results/{operation}__WSXXX__PXXX.json`
- Report/review evidence: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/evidence/{descriptive-name}.md`

## Mission and authority

{one coherent spec-aligned outcome}

- Spec authority: {exact section or requirement in the session's pinned authority}
- Required resolution evidence: {evidence}
- Assigned skill: {skill from task, when present}

## Scope

Copy these declarations from the current plan. Use literal repository-relative files or directory roots; use `.` only when the whole repository is intended. Do not use globs, absolute paths or traversal.

- Write scope: {paths from write_scope}
- Stable read assumptions: {paths from read_scope}
- Shared resources: {consistent resource IDs from resources, including shared git/GPU use}
- Contracts changed or consumed: {important interfaces and assumptions, or none}

Off-limits: every product file outside the write scope, and `AI_SPACE/SPEC.md` without explicit spec-edit authority. Scope declarations reserve work; they do not grant sandbox or tool permissions. A read-only role must not write any files. Required session result and evidence files are control metadata and must stay in the assigned session; the orchestrator saves exact content returned by read-only workers.

## Execution policy

- Work in the current checkout and inside existing sandbox permissions.
- Implement only the accepted current plan. Stop and return to planning if its scope or assumptions must change.
- Do not broaden the workstream, choose future work, or edit the runner state.
- Use safe local git only when the accepted plan authorises it.
- Serialise branch, worktree, stage, commit, merge and rebase work when shared state can change.
- Do not push, clean, hard reset, restore or discard paths unless the human explicitly authorises that exact action.
- Do not ask for repeated command permissions. Use allowed repo-local tools.
- Report unavailable authority, tooling, data or a safe execution path as `BLOCKED` with the exact reason.
- Leave no temporary diagnostics, fluff, workarounds or unrelated changes.
- Return facts and evidence. Do not add unsupported `next_step` or recommendation fields to JSON results.

## Validation gate

- {actual argv} proves {required behaviour}; record actual exit code and log. Save output only where existing permissions and accepted scope permit; otherwise return the exact content for orchestrator persistence.
- When the accepted plan requires a command manifest, use `.agents/skills/orchestrator/scripts/run_command_manifest.py` and its generated ledger. Do not write execution claims into that ledger manually. Copy actual command arguments, exit codes and log paths into the DSL validation result.

Command manifests, ledgers and baseline snapshots are optional plan-specific evidence. The DSL does not require the old nested plan layout or derive a diff from a baseline snapshot.

## Return contract

Return the JSON fields for the assigned operation from `.agents/workflow/results.schema.json`, using the assigned repository-relative session paths. If your role is read-only, return exact plan/report/review text alongside the result fields without writing files; the orchestrator saves that content and result JSON before `complete`. Keep file content outside the schema-defined JSON. Write-capable workers may save only files permitted by their accepted scope and existing permissions, returning their paths and any remaining content for orchestrator persistence.

For implementation, include the current `plan_id`, all changed product files, a report, and actual `argv`/`exit_code`/`log` records. For review, include the current `plan_id`, exact verdict and evidence path. For a blocked task, return only `operation`, `verdict: "BLOCKED"` and `reason`.

The orchestrator preserves the originating worker's facts, verdict, recorded claim and actual instance ID when saving returned content and submitting `complete`. It does not become the plan/review author by saving the file. The runner validates supplied facts; it does not execute commands, authenticate authors, or discover unreported changes. Report every off-protocol edit so the orchestrator can stop active work and invalidate stale session acceptance.
