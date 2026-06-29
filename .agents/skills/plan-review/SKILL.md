---
name: plan-review
description: Use when the prompt contains [PLAN.REVIEW] or [PLAN_REVIEW], or when a plan needs review for minimalism, work type correctness, spec alignment, orchestration safety, technical debt and implementation risk.
---

# [PLAN.REVIEW] / [PLAN_REVIEW]

Review a plan before implementation or agent spawning.

## Required review dimensions

- Work Type classification correctness
- Spec alignment and authority
- Minimalism: smallest coherent repo change
- Overengineering
- Technical debt
- Missing consequences
- File ownership and orchestration safety
- Validation strength
- Cleanup before `[DONE]`
- Commit policy
- Risks and blockers

## Work Type rejection rules

Reject the plan if:

- no Primary Work Type is declared
- more than one Primary Work Type is declared
- a capability plan is mostly dependency/docs/cleanup/temp/agent-workflow work
- temporary diagnostics are allowed to survive into commit
- one-off plots are being treated as validation evidence without reproducibility
- local environment adaptation changes core behaviour
- workaround work is used to claim capability progress
- `DEPENDENCY.LOCAL` work adds a dependency without justification
- `SPEC.EDIT` appears without `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]`
- the commit policy does not match the work type

## Orchestration rejection rules

Reject the plan if:

- write ownership overlaps another active plan without serialisation
- branch/worktree is missing for durable parallel work
- validation gate is missing or vague
- the owner agent is not named for orchestrated work
- task packet return schema is missing for worker agents
- merge order is unclear
- GPU-heavy validation is scheduled concurrently without explicit human approval

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

Plan reviews must feed back into implementation. Do not stop at "plan reviewed".
