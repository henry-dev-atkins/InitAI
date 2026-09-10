---
name: orchestrator
description: Dispatch the checked spec-convergence workflow through .agents/workflow/run.py. Use to review spec conformance, collate and select workstreams, plan and independently review, implement and independently review, and repeat until fresh full conformance passes.
---

# Orchestrator Procedure

This skill guides the manager in `.codex/agents/orchestrator.toml`.

`AI_SPACE/SPEC.md` is the product authority. If it is absent, follow the explicit-prompt authority rule in `AGENTS.md`. The orchestrator is the control thread. Agents do bounded work and return evidence. The outer spec review decides whether the campaign is finished.

Counterexample-guided convergence toward specification conformance: each evidence-backed misalignment from `$conformance` is a practical counterexample to the claim that the repository satisfies the specification.

## Workflow authority

Use `.agents/workflow/workflow.toml` for mechanical policy, `.agents/workflow/run.py` for checked transitions, and `.agents/workflow/results.schema.json` for typed handoffs. Read `.agents/workflow/README.md` for exact commands, packet examples and limitations. Do not maintain a second transition table or bypass a gate in prose.

The DSL binds seven operations to existing roles and skills. It keeps the simple loop: full conformance review, workstream collation and selection, planning and independent review, implementation and independent review, then fresh full conformance. Supporting skills do not create phases.

The runner owns saved mechanical state. The orchestrator alone chooses work within the permitted operations, launches agents, and submits their facts and verdicts. It does not implement project source code while orchestration is active. Workers do not edit runner state or choose future work.

## Dispatch

1. Run `check` against the repository. Start an explicit session with `init`, using the concrete spec or saved explicit human authority. Keep that session path for every later command.
2. Ask `next` for permitted tasks. It reports `READY`, `WAITING`, `BLOCKED` or `DONE`; an empty task list is not completion.
3. Reuse an idle agent or allocate a standby instance with explicit instructions to await dispatch without starting repository work. Obtain its actual instance ID, then reserve a returned task with `claim` using that ID. Role names are not instance identities. A failed claim leaves the instance idle.
4. After a successful claim, check the returned task and role, then dispatch work to that same instance. Send its operation and skill, authority, current plan where present, result contract and assigned session paths. The task-packet template is a short human-readable brief; it does not replace the JSON contract.
5. Read-only workers return exact plan/report/review content and result fields without editing files. Save their returned content and result JSON at the assigned session paths without changing their facts or verdicts. Write-capable workers save only files already permitted by their accepted scope and existing permissions; save any remaining session content they return. Submit `complete` with the original claim ID, same worker instance ID and result path. Saving returned content does not make you its author. Inspect failure output; never infer success from absent or malformed output.
6. Ask `next` again. Follow the permitted operation after rejection or blocking. Stop only when the runner reports `DONE` after a fresh full conformance `PASS` with an explicit empty findings list.

`next` is a view, not a reservation. Another task can reserve conflicting work before `claim`. A failed claim means no dispatch permission. Do not edit `state.json` to force progress.

Persisting returned plans, reports and results uses your existing control-file authority; it does not permit project source edits. Ask the originating worker for missing content. Keep file contents separate from the result JSON so that its schema stays exact. The default `conformance-reviewer` routes `conformance` to `$conformance` and `plan_review` to `$plan-review`; always pass the task's operation explicitly.

## Agent hierarchy

Indentation means ownership/delegation. A deeper level is an agent or sub-agent working for the level above it. This is an ownership view; the DSL defines operation order.

```text
USER: project intent and authority
    ORCHESTRATOR: checked dispatch and session control
        CONFORMANCE REVIEW AGENT(S): full scope evidence
            Optional read-only sub-agents: bounded inspection
        COLLATION / SELECTION: orchestrator skills within claimed tasks
        PLANNING AGENT: one selected workstream
            Optional supporting skills: first-principles, bounded-execution, plan-desk-check
        PLAN REVIEW AGENT: independent judgement of the current plan
            Optional review lenses: plan-preflight, change-impact-analysis, plan-elegance, peer-review
        IMPLEMENTATION AGENT: one accepted current plan
            Relevant implementation skills and bounded read-only sub-agents
            plan-sub: local execution decomposition only
        IMPLEMENTATION REVIEW AGENT: independent evidence and exact verdict
```
### Diagram
```text
USER: input prompt
|
v
ORCHESTRATOR
    |
    +-> CONFORMANCE REVIEW AGENT(S)
    |       |
    |       +-> optional read-only sub-agent(s) for bounded inspection
    |       |
    |       +-> output: misalignments
    |
    +-> $outcome-decomposition
    |       |
    |       +-> output: independent workstreams
    |
    +-> $select-ready-work
    |       |
    |       +-> output: selected workstreams
    |
    +-> PLANNING AGENT per selected workstream
    |       |
    |       +-> $plan
    |       |       |
    |       |       +-> optional supporting skill
    |       |           $first-principles
    |       |           $bounded-execution
    |       |
    |       +-> output: plan
    |
    +-> PLAN REVIEW AGENT per plan
    |       |
    |       +-> $plan-review
    |       |       |
    |       |       +-> optional review lens
    |       |           $plan-preflight
    |       |           $change-impact-analysis
    |       |           $plan-elegance
    |       |           $peer-review
    |       |           maintenance review skills
    |       |
    |       +-> output: ACCEPT / REJECT / BLOCKED
    |               |
    |               +-> REJECT -> planning agent replans that workstream
    |
    +-> PARALLEL IMPLEMENTATION AGENT(S)
    |       |
    |       +-> accepted plan is fixed authority
    |       |
    |       +-> any useful implementation skill
    |       |       $adversarial-review
    |       |       $vertical-slicing
    |       |       $test-driven-development
    |       |       $comprehensive-testing
    |       |       $plan-sub for local execution decomposition only
    |       |
    |       +-> output: code + validation facts
    |
    +-> IMPLEMENTATION REVIEW AGENT per implemented workstream
            |
            +-> output exactly:
                ACCEPT_IMPLEMENTATION
                REJECT_IMPLEMENTATION
                BLOCKED
                    |
                    +-> REJECT_IMPLEMENTATION -> planning failure -> replan

After the selected workstreams finish, return to SPEC REVIEW.
If SPEC REVIEW returns no misalignments, report DONE.
```


The runner limits active DSL claims; it does not count every live agent. Reserve every DSL operation before dispatch. Optional supporting sub-agents are not additional DSL operations and are not visible to that claim counter. The orchestrator must count them against real platform/agent capacity and keep their read-only work inside the parent task's reserved scope. They cannot create a new workflow stage.

## Judgement inside operations

Conformance review must cover the whole relevant authority. Each finding needs a stable ID, exact authority, repository evidence, expected and actual behaviour, and severity. Aim for maximum discovery so that a clean result is meaningful. Use `$finding-verification` only when evidence is disputed, weak or ambiguous. Missing findings or an incomplete review is not `PASS`.

Collation uses `$outcome-decomposition`. Split only genuinely independent durable outcomes. Required tests, config changes and behaviour documentation may remain supporting changes within the capability workstream. Each current finding has one owning workstream; represent dependencies between workstreams explicitly rather than duplicating finding ownership. Keep one Primary Work Type and one Workflow Class per workstream.

Selection uses `$select-ready-work`. Prefer the largest useful ready workstreams: material spec misalignment, work that unblocks others, then core behaviour before cleanup. Capacity is a limit, not a target. Never split, duplicate or invent work to fill it. Do not select blocked dependencies.

Planning uses `$plan`. Include source findings, exact spec authority, one outcome, bounded write scope, read assumptions, ordered steps, meaningful validation, protected invariants and prohibited shortcuts. Declare shared git/GPU resources consistently. Include `Am I going in Circles?` and `Is there a more elegant way of doing this?`. The structured packet points to the plan; it does not replace its reasoning. Every revised plan needs a new plan ID within its workstream and independent review. Never reuse an earlier ID for that workstream.

Plan review uses `$plan-review` on the current saved plan. The reviewer must be a different actual instance from its planner. Preflight follows the workflow file: optional may be `SKIPPED`; required must `PASS`. Known mechanical defects require correction. `$parallel-safety`, `$plan-elegance`, `$change-impact-analysis`, `$peer-review` and maintenance skills remain useful supporting lenses. Command manifests and old ledgers are used only when the accepted plan requires them.

Implementation follows the accepted current plan. Relevant implementation skills and `$plan-sub` may help within that authority. Material scope or requirement changes return to planning. Record all changed product files, actual validation command arguments, exit codes, logs and a report. The external worker runs commands; the DSL runner only checks submitted evidence.

Implementation review uses a different actual instance from the implementer. It checks the work against the current accepted plan, source findings, scope and meaningful validation. Return `ACCEPT_IMPLEMENTATION`, `REJECT_IMPLEMENTATION` or `BLOCKED` through the result contract. Passing exit codes alone do not prove useful validation.

## Parallel work and stale plans

Use the DSL's capacity, declared read/write scopes and shared resources. Global and planning operations hold conservative repository-wide read reservations. Implementation review holds the plan's read and write scopes as read reservations. This may serialise tasks whose independence has not been established.

Identify semantic dependency conflicts as well as path overlaps. Serialise uncertain cases or use `$parallel-safety`. Scope declarations schedule work; they do not grant filesystem or tool permissions. Use the existing sandbox and `AGENTS.md` authority rules for actual access.

Submitted implementation changes invalidate other pending plans whose declared read/write scopes overlap. Interrupted or blocked implementation uses its whole write scope because its partial changes are unknown. The affected work returns to planning with the invalidation reason. A changed plan file cannot retain its old acceptance.

After source changes outside this protocol, stop active work, explicitly release outstanding claims as needed, and use `invalidate` before trusting any saved acceptance or completion. The runner cannot detect unreported edits. Changed workflow configuration or spec authority requires a new explicit session.

## Failure discipline

Implementation failure is always planning failure, either in the plan itself or in campaign/orchestration after multiple failures. A rejected implementation returns to planning. Reviewer next-step text is evidence only; it cannot authorise an ad hoc repair phase.

Do not create repair phases, fix-forward packets, emergency patch stages or special retry workflows. Source-writing tasks are never retried automatically. After an interrupted task, `release` records a block. Resolve the exact need and use `resume` with an explicit reason; an interrupted implementation resumes through planning.

A tooling/access failure before source edits may retry once within this explicit protocol. `BLOCKED` is for unavailable authority, tooling, data or a safe execution path. A blocked task is not an accepted task and cannot make a session complete.

After repeated failure ask:

- `Am I going in Circles?`
- `Is there a more elegant way of doing this?`

Use `$diagnose`, `$first-principles` or `$strategy-review` when the workstream boundary, plan or campaign direction is wrong. Then return to the same simple loop.

Workers may use safe local git only when the accepted plan authorises it. Safe local git includes local branches, worktrees, stage, commit, merge and rebase. Serialise git work when shared checkout state can change. Do not push, clean, hard reset, restore or discard paths unless the human explicitly authorises that exact action.

## Session memory and progress

Use the minimal session layout in `.agents/workflow/README.md`: runner state, current plans, result packets and required evidence. Add readable findings or workstream summaries only when they help review or resumption. Do not require old ledgers, snapshots or requirement registers by default. These files are durable memory, not a second product authority.

When the human requests `$progress-report`, delegate it to `progress-reporter`. Pass the explicit session path, report timestamp and supplied chat timestamps. The worker may read session evidence and write only that session's `progress_reports/` directory. The report is optional and adds no stage to the convergence loop.
