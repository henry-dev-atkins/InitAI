# Plan Review

```yaml
plan_review_id: PRXXX
workstream_id: WSXXX
plan_id: PXXX
predecessor_plan_id: {PXXX-or-null}
preflight_status: PASS | FAIL | BLOCKED | NOT_RUN
capability_first_status: PASS | FAIL
causal_delta_status: PASS | FAIL | NOT_APPLICABLE
verdict: ACCEPT | REJECT | BLOCKED
blocking_issues:
  - criterion: {dimension}
    evidence: {specific defect or missing evidence}
non_blocking_observations:
  - {observation-or-none}
acceptance_evidence:
  - {why the plan is sufficient, or what evidence is missing}
```
