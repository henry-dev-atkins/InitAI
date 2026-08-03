---
name: campain-review
description: Use when the prompt contains [CAMPAIN.REVIEW], at major campaign milestones, when the portfolio stalls, or when new evidence may have invalidated the current route to the terminal condition.
---

# [CAMPAIN.REVIEW]

Review whether the current campaign map and portfolio still represent the best evidence-backed route to the terminal condition. This reviews the plan of plans; it does not repeat implementation review.

## Role boundary

- Assess destination, assumptions, dependencies, horizons, critical path, fog, queue health and convergence evidence.
- Do not implement, author individual plans, assign agents, change workstream states or declare completion.
- Do not reopen settled decisions without contradictory evidence.
- Do not recommend activity merely to keep agents busy.

## Invoke when

- a major architectural outcome is accepted;
- repeated plan or implementation rejection suggests route failure;
- the critical path becomes blocked;
- the implementation-ready queue is persistently empty;
- new evidence exposes specification fog;
- a milestone completes;
- full spec review materially changes the finding register;
- convergence stalls despite high activity.

## Required checks

- Is the destination still exact and authoritative?
- Are campaign nodes durable outcomes rather than issue fragments?
- Are dependency and contract assumptions current?
- Which prepared outcomes can now become committed?
- Which plans became stale or unnecessary?
- Is capacity moving critical-path outcomes or support-only churn?
- Is a fresh full review justified, or would an impact-cone review suffice?
- Are we going in circles?
- Is there a more elegant route?

## Output

```yaml
campain_review_id: CR001
campaign_epoch_reviewed: E001
repo_revision: {revision}
destination_status: VALID | UNCLEAR | INVALIDATED
route_status: VALID | REMAP_REQUIRED | BLOCKED
critical_path:
  current: []
  changed: true | false
assumptions:
  confirmed: []
  invalidated: []
horizon_changes:
  promote_to_committed: []
  return_to_prepared: []
  move_to_fog: []
stale_or_redundant_plans: []
queue_health:
  idle_capacity_cause: {none/dependency/review/planning/resource/fog}
  support_only_churn: true | false
review_scope_needed: NONE | IMPACT_CONE | FULL_REMAP
findings: []
status: PASS | FINDINGS | BLOCKED
```

The orchestrator owns campaign-epoch updates, remapping, state changes and any subsequent assignments.
