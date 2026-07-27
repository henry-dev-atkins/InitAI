---
name: plan-review
description: Use when the prompt contains [PLAN.REVIEW] or [PLAN_REVIEW], or when one workstream plan needs an accept/reject gate before implementation.
---

# [PLAN.REVIEW] / [PLAN_REVIEW]

Review one submitted workstream plan. Return evidence for `ACCEPT`, `REJECT` or genuine `BLOCKED`; do not manage sequencing or implement changes.

## Required dimensions

- source finding and spec traceability;
- one coherent workstream outcome;
- correct Primary Work Type;
- top-down convergence impact;
- minimal complete implementation;
- exact write/off-limits scope;
- dependencies and parallel-safety;
- contracts changed/consumed;
- protected invariants and prohibited behaviour;
- implementation-order logic;
- behavioural validation strength;
- result-packet completeness;
- overengineering, technical debt and repository fit.

Use retained supporting lenses when relevant:

- `plan-elegance`;
- `maintain-review`;
- `maintain-elegance`;
- `maintain-techdebt`;
- `maintain-despaghettify`;
- `maintain-declutter`;
- `peer-review`.

They inform this single plan-review verdict; they do not create additional workflow phases.

## Reject when

- the workstream/finding/spec traceability is absent or incorrect;
- the plan does not fully remove the assigned misalignment;
- it broadens into unrelated work or fragments one coherent result unnecessarily;
- it starts with support software without showing that it is the shortest route to required behaviour;
- exact file scope, dependencies, contract effects or owner are missing;
- it conflicts with another active workstream;
- validation is vague, toy-only or does not prove the assigned behaviour;
- temporary/workaround/fluff output may survive;
- capability progress is claimed for support-only work;
- a simpler repository-fitting solution is clearly available and unaddressed;
- it relies on an assumed later repair pass.

`BLOCKED` is only for missing authority, tooling, data or a safe execution path—not ordinary plan defects.

## Role boundary

- Do not choose the next workstream, propose a replacement plan, schedule agents or recommend process actions.
- Name concrete defects and evidence required for acceptance.
- The orchestrator owns replanning and state transitions.

## Output

```yaml
plan_review_id: RXXX
workstream_id: WSXXX
plan_id: PXXX
verdict: ACCEPT | REJECT | BLOCKED
blocking_issues:
  - criterion: {dimension}
    evidence: {specific defect or missing evidence}
non_blocking_observations:
  - {observation-or-none}
acceptance_evidence:
  - {why the plan is sufficient, or what evidence is missing}
```
