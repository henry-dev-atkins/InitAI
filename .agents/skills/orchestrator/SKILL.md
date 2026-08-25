---
name: orchestrator
description: Procedural workflow for the project-scoped orchestrator custom agent. Use to repeatedly review the repository against AI_SPACE/SPEC.md, turn misalignments into independent workstreams, plan and review them, implement accepted plans, review the work, and repeat until spec review is clean.
---

# Orchestrator Procedure

This skill defines the simple convergence loop for `.codex/agents/orchestrator.toml`.

`AI_SPACE/SPEC.md` is the product authority. The orchestrator is the control thread. Agents do bounded work and return evidence. The outer spec review decides whether the campaign is finished.

The workflow has seven operations:

1. review the spec against the repository;
2. output misalignments;
3. collate misalignments into independent workstreams;
4. select the next N workstreams;
5. plan and review each selected workstream;
6. implement accepted plans and independently review the work;
7. return to spec review.

Stop only when a fresh spec review finds no material misalignment.

## Agent hierarchy

Indentation means ownership/delegation. A deeper level is an agent or sub-agent working for the level above it.

```text
USER: input prompt
|
v
ORCHESTRATOR
    |
    +-> SPEC REVIEW AGENT(S)
    |       |
    |       +-> optional read-only sub-agent(s) for bounded inspection
    |       |
    |       +-> output: misalignments
    |
    +-> $plan-portfolio
    |       |
    |       +-> output: independent workstreams
    |
    +-> $portfolio-next
    |       |
    |       +-> output: selected workstreams
    |
    +-> PLANNING AGENT per selected workstream
    |       |
    |       +-> $plan
    |       |       |
    |       |       +-> optional supporting skill
    |       |           $planning-and-task-breakdown
    |       |           $first-principles
    |       |           $flowguard
    |       |
    |       +-> output: plan
    |
    +-> PLAN REVIEW AGENT per plan
    |       |
    |       +-> $plan-review
    |       |       |
    |       |       +-> optional review lens
    |       |           $plan-preflight
    |       |           $plan-blastradius
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
    |       |       $api-and-interface-design
    |       |       $doubt-driven-development
    |       |       $incremental-implementation
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

## Core loop

```text
SPEC REVIEW
    -> misalignments[]

COLLATE
    -> workstreams[]

SELECT NEXT N
    -> selected_workstreams[]

PLAN EACH
    -> plans[]

REVIEW EACH PLAN
    -> accepted_plans[]

PARALLEL IMPLEMENT + REVIEW
    -> accepted implementations
    -> rejected implementations return to planning

BACK TO SPEC REVIEW

STOP when misalignments[] is empty.
```

## Pseudocode

```python
while True:
    findings = spec_review(spec, repo)

    if not findings:
        return DONE

    workstreams = collate(findings)
    selected = select_next_n(workstreams, N)

    plans = parallel(
        plan(ws)
        for ws in selected
    )

    accepted_plans = []

    for plan in plans:
        while True:
            verdict = review_plan(plan)

            if verdict == ACCEPT:
                accepted_plans.append(plan)
                break

            if verdict == BLOCKED:
                mark_blocked(plan.workstream)
                break

            plan = replan(plan.workstream, verdict.findings)

    results = parallel(
        implement(plan)
        for plan in accepted_plans
        if parallel_safe(plan)
    )

    for result in results:
        verdict = review_implementation(result)

        if verdict == ACCEPT_IMPLEMENTATION:
            mark_accepted(result.workstream)

        elif verdict == REJECT_IMPLEMENTATION:
            # Implementation failure is always planning failure.
            mark_for_replanning(result.workstream, verdict.findings)

        elif verdict == BLOCKED:
            mark_blocked(result.workstream)

    # Return to the product authority after every batch.
    # The next spec review decides what still matters.
```

The pseudocode is policy, not a requirement to implement a software scheduler.

## 1. Review the spec

Run `$spec-review` against the current repository and the whole relevant `AI_SPACE/SPEC.md`.

The output is a list of material misalignments. Each misalignment needs:

- a stable finding ID such as `F001`;
- exact spec authority;
- exact repository evidence;
- expected behaviour or state;
- actual behaviour or state;
- severity.

A clean review returns `PASS` and an empty misalignment list.

Use `$verify-finding` only when a finding is disputed, weakly evidenced, or materially ambiguous. Do not add a verification stage to findings that are already clear.

## 2. Collate misalignments into workstreams

Run `$plan-portfolio` on the current misalignment list.

Split only genuinely independent durable outcomes. Required tests, config changes and behaviour documentation may remain supporting changes within the capability workstream.

Each misalignment belongs to one active workstream unless an explicit dependency makes shared ownership unavoidable.

A workstream needs only:

- workstream ID;
- title and durable outcome;
- source finding IDs;
- relevant spec authority;
- rough affected area;
- dependencies, if any;
- status.

Do not build a second requirements system around the spec. The spec review will run again after implementation.

## 3. Select the next N workstreams

Run `$portfolio-next`.

Select up to the available agent capacity. Prefer the largest useful independent workstreams that are ready now. Do not select blocked work merely to fill capacity.

Prioritise:

1. large amounts of material spec misalignment;
2. work that unblocks other work;
3. core behaviour before cleanup;
4. work that can proceed independently with low collision risk.

N is a capacity limit, not a target. Use fewer workstreams when independence is uncertain.

## 4. Plan each workstream

Delegate one selected workstream to one planning agent. Run `$plan`.

A plan needs:

- workstream ID and finding IDs;
- exact spec authority;
- one coherent intended outcome;
- exact or bounded write scope;
- important read/dependency assumptions;
- ordered implementation steps;
- meaningful validation;
- protected invariants and prohibited shortcuts;
- `Am I going in Circles?`;
- `Is there a more elegant way of doing this?`.

The planner may use supporting skills such as `$planning-and-task-breakdown`, `$first-principles`, `$flowguard`, `$prototype`, or domain skills when they help. Supporting skills do not create workflow stages.

## 5. Review each plan

Every plan gets independent `$plan-review` before source writing begins.

The reviewer returns exactly one plan verdict:

- `ACCEPT`;
- `REJECT`;
- `BLOCKED`.

`REJECT` returns the workstream to planning with concrete findings. It is not permission for an implementation worker to improvise a repair.

Use `$plan-preflight`, `$plan-parallel-collate`, `$plan-blastradius`, `$plan-elegance`, `$peer-review`, or maintenance skills only when their specific question matters. They are review tools, not mandatory global phases.

Before parallel implementation, compare accepted plans. Parallelise only workstreams whose write scopes and important shared dependencies do not conflict. If that is unclear, use `$plan-parallel-collate`.

## 6. Implement and review

Assign each accepted plan to the most suitable write-capable implementation agent.

Implementation agents are deliberately flexible. They may use any relevant implementation skill or read-only sub-agent. They may not change the accepted workstream outcome, broaden its write scope, invent new product requirements, choose future work, or change orchestration state.

`$plan-sub` is allowed only for local execution decomposition inside the accepted plan. If a material plan change is required, stop implementation and return to planning.

Workers do not create/switch branches or worktrees, merge, rebase, stage or commit.

Review every implementation independently. The review decision uses exactly:

- `ACCEPT_IMPLEMENTATION`;
- `REJECT_IMPLEMENTATION`;
- `BLOCKED`.

`ACCEPT_IMPLEMENTATION` means the work matches the accepted plan and its source findings, and its meaningful validation passes.

`REJECT_IMPLEMENTATION` means the result does not deserve acceptance. Rejection findings must describe what is wrong. They must not authorise an ad hoc patch.

Implementation failure is always planning failure. Anything that goes wrong during implementation means the accepted plan was not clear, complete or correct enough for one controlled implementation attempt. Return the workstream to planning with a new or revised plan that addresses the evidence.

A tooling/access failure before source edits may retry once. `BLOCKED` is for unavailable authority, tooling, data, or a safe execution path.

## 7. Return to spec review

After the selected workstreams have been reviewed, run a fresh `$spec-review` against the current repository.

Do not rely on old workstream status as proof of completion. The repository must now satisfy the spec.

The new review may:

- find nothing, in which case report `[DONE]`;
- rediscover a previous finding, in which case it was not actually closed;
- expose a new consequence of earlier work;
- produce a smaller remaining misalignment list.

Then repeat the same loop.

## Failure discipline

Implementation failure is always planning failure, eitehr in planning itself, or in campaign/orchestration after multiple plan failures.

Do not create repair phases, fix-forward packets, emergency patch stages, or special retry workflows.

After repeated failure ask:

- `Am I going in Circles?`
- `Is there a more elegant way of doing this?`

Use `$diagnose`, `$first-principles`, or `$campain-review` when repeated failure shows that the workstream boundary, plan, or campaign direction is wrong. Then return to the same simple loop.

## Authority

The orchestrator alone:

- owns the current finding and workstream lists;
- selects N;
- assigns agents;
- records plan and implementation verdicts;
- decides whether a workstream returns to planning;
- declares `[DONE]` only after a clean outer spec review.

Workers and reviewers return facts and verdicts. They do not choose future work.

## Minimal session artefacts

For substantial orchestrated work use:

```text
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/
  misalignments.md
  workstreams.md
  selected_workstreams.md
  plans/
    WS001__P001.md
  plan_reviews/
    WS001__P001.md
  implementation_reviews/
    WS001.md
```

Use these files as durable memory, not as a second product authority. Small work can remain lighter when the same loop is still clear.
