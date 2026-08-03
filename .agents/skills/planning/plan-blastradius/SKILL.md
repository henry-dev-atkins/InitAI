---
name: plan-blastradius
description: Use when the prompt contains [PLAN.BLASTRADIUS], before accepting a plan that changes contracts, or after accepted implementation to identify affected consumers, validations and stale plans.
---

# [PLAN.BLASTRADIUS]

Determine the prospective or actual impact cone of one planned or accepted change. Name affected contracts, consumers, plans, tests, generated outputs and invalidation boundaries without broadening the workstream.

## Modes

- `PROSPECTIVE`: analyse what the proposed plan could affect before implementation.
- `RETROSPECTIVE`: analyse what an accepted diff actually invalidated or unlocked.

## Role boundary

- Inspect dependency, import, schema, configuration, data-flow and behavioural contract relationships.
- Do not implement, repair, assign agents or change plan/workstream state.
- Do not treat file disjointness as proof of semantic independence.
- Return evidence and invalidation facts; the orchestrator decides replanning and scheduling.

## Required checks

- public and internal interfaces;
- behavioural invariants, ordering, errors and performance facts callers rely on;
- configuration ownership and generated outputs;
- direct and transitive consumers;
- tests and real-run validation affected;
- accepted, prepared or active plans that consume changed contracts;
- concurrent write or resource conflicts;
- whether the change unlocks dependent outcomes.

## Output

```yaml
blast_radius_id: BR001
mode: PROSPECTIVE | RETROSPECTIVE
subject:
  workstream_id: WS001
  plan_id: P001
  repo_revision: {revision}
contracts_changed:
  - name: {stable contract name}
    current_version: {version or unknown}
    proposed_or_new_version: {version or unknown}
    evidence: []
impact_cone:
  direct_consumers: []
  transitive_consumers: []
  affected_tests_and_validation: []
  generated_outputs: []
  affected_plans:
    - plan_id: PXXX
      effect: VALID | RECHECK | INVALIDATE
      reason: {evidence}
parallel_conflicts: []
unlocked_workstreams: []
unknowns: []
status: PASS | RECHECK_REQUIRED | BLOCKED
```

A `RECHECK_REQUIRED` result is not rejection by itself; it identifies where plan review or orchestrator state reconciliation must act.
