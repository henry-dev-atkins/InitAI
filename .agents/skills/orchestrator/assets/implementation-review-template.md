# Implementation Review

```yaml
implementation_review_id: IRXXX
workstream_id: WSXXX
plan_id: PXXX
requirement_ids:
  - REQXXX
repo_tree_hash: {active-tree-hash}
baseline_snapshot_path: {path}
scope_diff_path: {path}
evidence_ledger_path: {path}
verdict: ACCEPT_IMPLEMENTATION | REJECT_IMPLEMENTATION | BLOCKED
findings_resolved:
  - FXXX
findings:
  - source_finding_id: IRXXX-F001
    requirement_ids: [REQXXX]
    spec_authority: {section/requirement}
    severity: critical | high | medium | low
    expected: {required state}
    actual: {observed state}
    evidence:
      - {path:line/command/result}
    resolution_evidence: {proof required}
scope_review:
  allowed_files: [{paths}]
  actual_files: [{paths from scope_diff.json}]
  out_of_scope_files: [{paths-or-none}]
  stable_read_invalidations: [{paths-or-none}]
  status: PASS | FAIL
validation_review:
  status: PASS | FAIL | INSUFFICIENT
  evidence: [{ledger path and command IDs}]
accepted_state_path: {path-or-null}
```

Rejection returns findings to the orchestrator. Do not prescribe a repair packet.
