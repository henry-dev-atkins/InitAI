# Readiness Queues

```yaml
campaign_epoch: E001
updated_at: {ISO-8601}
planning_ready: []
plan_collation_ready: []
plan_preflight_ready: []
plan_review_ready: []
implementation_ready: []
implementation_review_ready: []
validation_ready: []
fog_clearing_ready: []
blocked_on_dependency: []
blocked_on_human: []
active_assignments:
  - workstream_id: WS001
    stage: {stage}
    role: {agent role}
    locks: []
capacity:
  maximum_agents: 6
  available_agents: 0
  active_by_role:
    planning: 0
    review: 0
    implementation: 0
    validation: 0
```

Queue mapping:

- `validation_ready` contains `READY` workstreams whose Primary Work Type is `EVIDENCE.VALIDATION`; assignment uses the normal `READY -> IMPLEMENTING` transition.
- `fog_clearing_ready` contains campaign-map fog actions, not workstream states. A fog action may create evidence or a new workstream only through the orchestrator.
- Capacity values are current limits, not fixed reservations. The orchestrator fills any safe ready queue while keeping within the total and resource locks.
