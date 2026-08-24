---
name: plan-parallel-collate
description: Use when the prompt contains [PLAN.PARALLEL_COLLATE], or after a batch of planning agents returns to collate portfolio safety before individual plan review.
---

# [PLAN.PARALLEL_COLLATE]

Collate a batch of submitted workstream plans before individual `[PLAN.REVIEW]`. This skill preserves the large-step signal from spec review, detects unsafe parallelism and reports which plans may proceed to mechanical preflight.

## Inputs

- parent session path;
- candidate plan paths;
- canonical current finding register;
- current workstream register;
- canonical contract register;
- current file, contract and mutable-resource locks;
- dependency, stable-read, contract and resource records from each plan.

If any required register or plan is missing, return `BLOCKED` with the exact missing path.

## Required checks

- Every candidate has a unique plan ID and workstream ID.
- Every candidate maps to an open or replanning workstream.
- Authorised findings and requirement IDs remain covered by their candidate plans.
- No candidate broadens beyond its assigned workstream.
- Planned write scopes and stable read assumptions use exact canonical roots. Write/write and write/stable-read intersections are empty for any proposed parallel batch.
- Contract changes do not conflict with another plan's changes or consumers.
- Mutable resources do not conflict across a proposed parallel batch.
- Dependencies are read from the workstream register and are already `ACCEPTED`.
- Planning output does not collapse the portfolio into support-only churn when capability findings remain open.

## Output

```yaml
parallel_plan_collation_id: PPCXXX
session: session__YYYYMMDD_HHMMSS
status: PASS | FAIL | BLOCKED
safe_batches:
  - batch_id: B001
    plans: [PXXX]
blocked_or_conflicting_plans:
  - plan_id: PXXX
    reason: {overlap/dependency/contract/finding-coverage issue}
coverage_gaps:
  - {finding/workstream not preserved}
```

Only plans in a safe batch may proceed to `[PLAN.PREFLIGHT]`. Collation is a safety gate, not a replacement for full plan review.
