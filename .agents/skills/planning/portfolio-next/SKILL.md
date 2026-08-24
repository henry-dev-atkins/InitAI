---
name: portfolio-next
description: Use when the prompt contains [PORTFOLIO.NEXT], whenever agent capacity becomes free, or when the orchestrator must select the highest-value safe items from mixed readiness queues.
---

# [PORTFOLIO.NEXT]

Evaluate the current portfolio and return the highest-convergence-value safe candidates that may advance now. This is a scheduling analysis skill, not a second orchestrator.

## Role boundary

- Read current queues, dependencies, locks, contract versions, capacity and critical path.
- Rank only work already authorised for its current transition.
- Do not assign agents, change states, acquire locks, author plans or start implementation.
- Do not invent, split or duplicate work to fill capacity.

## Required inputs

- campaign map;
- finding and workstream registers;
- readiness queues;
- active locks and write scopes;
- canonical contract register with changed/consumed contract IDs and versions;
- exact write/stable-read locks and mutable-resource locks;
- available total agent capacity and resource constraints.

## Selection principles

Prefer work that:

1. advances major spec behaviour;
2. lies on or unlocks the critical path;
3. retires uncertainty that blocks expensive work;
4. is safe under write/write, write/stable-read, contract and mutable-resource constraints;
5. can refill capacity without waiting for unrelated slow siblings.

Defer work that is likely to be invalidated by unresolved architectural decisions. Planning, review, implementation and validation candidates may be returned together because phase order is local to each workstream.

## Output

```yaml
portfolio_next_id: PN001
campaign_epoch: E001
capacity:
  planning: 0
  review: 0
  implementation: 0
  validation: 0
selected:
  - workstream_id: WS001
    current_state: {state}
    eligible_transition: {one allowed next transition}
    queue: planning_ready | plan_review_ready | implementation_ready | implementation_review_ready | validation_ready | fog_clearing_ready
    priority_reason: {critical-path/convergence explanation}
    required_role: {bounded agent role}
    resource_constraints: []
not_selected:
  - workstream_id: WSXXX
    reason: {dependency, conflict, staleness, lower value or no capacity}
status: READY | NOTHING_READY | BLOCKED
```

The orchestrator validates the recommendation, performs state transitions and authorises assignments. `validation_ready` uses the normal `READY -> IMPLEMENTING` transition for `EVIDENCE.VALIDATION` workstreams. `fog_clearing_ready` contains campaign-map evidence actions and does not imply a workstream state. Capacity fields are current limits, not fixed role reservations.
