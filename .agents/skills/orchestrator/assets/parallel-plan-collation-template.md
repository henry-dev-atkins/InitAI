# Parallel Plan Collation

```yaml
parallel_plan_collation_id: PPCXXX
session: session__YYYYMMDD_HHMMSS
status: PASS | FAIL | BLOCKED
reviewed_plans:
  - PXXX
safe_batches:
  - batch_id: B001
    plans: [PXXX]
blocked_or_conflicting_plans:
  - plan_id: PXXX
    reason: {overlap/dependency/contract/finding-coverage issue}
coverage_gaps:
  - {finding/workstream not preserved}
```
