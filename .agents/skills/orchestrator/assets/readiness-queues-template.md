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
  planning: 1
  review: 1
  implementation: 3
  reserve: 1
```
