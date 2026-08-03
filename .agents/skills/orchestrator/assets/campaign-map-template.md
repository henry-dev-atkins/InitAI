# Campaign Map

```yaml
campaign_id: C001
campaign_epoch: E001
repo_revision: {commit-or-tree-hash}
destination:
  authority: {AI_SPACE/SPEC.md section or explicit human authority}
  completion_claim: {observable terminal state}
settled_context:
  decisions: []
  constraints: []
nodes:
  - outcome_id: O001
    outcome: {one durable repository truth}
    horizon: COMMITTED | PREPARED
    state: OPEN | ACTIVE | ACCEPTED | BLOCKED | SUPERSEDED
    source_findings: []
    workstream_id: null
    depends_on: []
    unlocks: []
    contracts_changed: []
    contracts_consumed: []
    acceptance_evidence: []
fog:
  - fog_id: G001
    area: {uncertain territory}
    why_not_specifiable: {reason}
    clearing_action: {bounded evidence action}
critical_path: []
last_campain_review: null
```
