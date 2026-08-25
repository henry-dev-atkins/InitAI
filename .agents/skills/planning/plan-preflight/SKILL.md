---
name: plan-preflight
description: Optional quick mechanical completeness check for one plan before semantic plan review.
---

# [PLAN.PREFLIGHT]

Check that one plan contains the fields required by `$plan` and references real files/spec sections where applicable.

Return `PASS` or `FAIL` with missing/invalid fields.

Do not judge architecture or rewrite the plan. `$plan-review` owns semantic acceptance.
