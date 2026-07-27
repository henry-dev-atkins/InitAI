# Implementation Review

```yaml
implementation_review_id: RXXX
workstream_id: WSXXX
plan_id: PXXX
repo_revision: {tree-hash}
verdict: ACCEPT_IMPLEMENTATION | REJECT_IMPLEMENTATION | BLOCKED
findings_resolved:
  - FXXX
findings:
  - source_finding_id: RXXX-F001
    spec_authority: {section/requirement}
    severity: critical | high | medium | low
    expected: {required state}
    actual: {observed state}
    evidence:
      - {path:line/command/result}
    resolution_evidence: {proof required}
scope_review:
  allowed_files: [{paths}]
  actual_files: [{paths}]
  status: PASS | FAIL
validation_review:
  status: PASS | FAIL | INSUFFICIENT
  evidence: [{commands/results}]
```

Rejection returns findings to the orchestrator. Do not prescribe a repair packet.
