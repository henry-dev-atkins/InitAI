---
name: plan-parallel-collate
description: Optional safety check for a set of accepted plans before parallel implementation. Use only when parallel independence is not obvious.
---

# [PLAN.PARALLEL_COLLATE]

Input: two or more accepted plans.

Output: `SAFE`, `SERIALISE`, or `REPLAN`, plus the exact collision when one exists.

Check only what matters for parallel work:

- overlapping write scope;
- one plan writing an important file another plan assumes stable;
- shared generated outputs, database, port, GPU-heavy job, or other exclusive resource;
- explicit dependency between the workstreams.

Do not redesign the plans. Do not create a new workflow phase. The orchestrator uses this result when deciding whether accepted plans may run in parallel.
