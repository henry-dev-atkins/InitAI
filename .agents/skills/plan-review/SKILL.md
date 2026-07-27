---
name: plan-review
description: Use when the prompt contains [PLAN.REVIEW] or [PLAN_REVIEW], or when a plan needs review for minimalism, work type correctness, spec alignment, orchestration safety, technical debt and implementation risk.
---

# [PLAN.REVIEW] / [PLAN_REVIEW]

Review a plan before implementation or agent spawning.

## Required review dimensions

- Work Type classification correctness
- Spec alignment and authority
- Source finding traceability and convergence-impact priority
- Minimalism: smallest coherent repo change
- Overengineering
- Technical debt
- Solution elegance: use `plan-elegance` when the plan may miss a simpler, cleaner, more repo-fitting implementation
- Repo maintainability: use `maintain-review` when the plan may drift away from core spec capabilities through avoidable surrounding software or repo complexity
- Repo structure: use `maintain-despaghettify` when the plan changes code/module boundaries, introduces broad abstractions, or risks tangled responsibilities
- Technical debt: use `maintain-techdebt` when the plan introduces durable code, dependency, data-flow, or maintenance cost
- Missing consequences
- Implementation order: the plan explains why its first steps are the right starting point
- File ownership and orchestration safety
- Validation strength
- Cleanup before `[DONE]`
- Commit policy
- Risks and blockers

## Work Type rejection rules

Reject the plan if:

- no Primary Work Type is declared
- more than one Primary Work Type is declared
- it cites no stable spec-review finding ID and evidence
- it does not remove or materially reduce the cited misalignment
- it drops the cited finding's behavioural context to implement an isolated ingredient
- it is a bottom up implementation - we want top down implementation
- it will need a repair pass after being implemented
- a capability plan is mostly dependency/docs/cleanup/temp/agent-workflow work
- capability progress is claimed for code that no working spec path consumes
- a plan starts with support work while a core capability or alignment target is still missing, and the ordering rationale does not show that the support work directly enables the next behaviour step
- `plan-elegance` finds a clearly simpler repo-fitting solution and the plan does not adopt it or justify rejecting it
- temporary diagnostics are allowed to survive into commit
- one-off plots are being treated as validation evidence without reproducibility
- local environment adaptation changes core behaviour
- workaround work is used to claim capability progress
- `DEPENDENCY.LOCAL` work adds a dependency without justification
- `SPEC.EDIT` appears without `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]`
- the commit policy does not match the work type

## Orchestration rejection rules

Plan reviews provide evidence. The orchestrator decides whether and how that evidence affects implementation.
Reject the plan if:

- write ownership overlaps another active plan without serialisation
- exact file ownership or integration order is missing for durable parallel work
- validation gate is missing or vague
- the owner agent is not named for orchestrated work
- task packet return schema is missing for worker agents
- merge order is unclear
- GPU-heavy validation is scheduled concurrently without explicit human approval


Plan-review agents are factual reviewers, not process managers.

  - Report whether the submitted plan passes or fails the review criteria.
  - Name concrete plan defects and the evidence needed for the plan to pass.
  - Do not suggest next steps, propose a follow-up plan, choose the next packet, or tell the orchestrator what to do after the review.
  - Do not include fields such as `next_step`, `recommended_next_action`, `recommended_plan`, or similar process-direction text.
  - `implementation_permission` is only a gate on the reviewed plan. It is not an instruction to spawn a worker.
  - The orchestrator owns sequencing, portfolio decisions, commits, deferrals, splits and stop/pivot decisions


## Output

Return:

```yaml
review_status: PASS | NEEDS_REVISION | BLOCKED
blocking_findings:
  - {finding-or-none}
non_blocking_findings:
  - {finding-or-none}
required_plan_changes:
  - {change-or-none}
implementation_permission: yes | no
```

Return `NEEDS_REVISION` with `implementation_permission: no` when the implementation order rationale is missing or weak. Do not block useful compromises: early support work is acceptable when the plan shows it is the shortest practical route to the next spec-backed behaviour. 

Plan reviews must feed back into implementation. Do not stop at "plan reviewed".
