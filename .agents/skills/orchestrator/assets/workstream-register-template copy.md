# Workstream Register

Only the orchestrator creates workstreams or changes state.

| Workstream | Outcome | Findings | Work Type | Depends On | Write Scope | Contracts Changed | Contracts Consumed | Plan | Rejected Plans | Rejected Implementations | Threshold State | State |
|---|---|---|---|---|---|---|---|---|---:|---:|---|---|
| WS001 | `{coherent result}` | F001 | `{WORK_TYPE}` | none | `{paths}` | `{contracts}` | `{contracts}` | P001 | 0 | 0 | CLEAR | AWAITING_PLAN |

States:

`AWAITING_PLAN`, `PLANNING`, `AWAITING_PLAN_COLLATION`, `AWAITING_PLAN_PREFLIGHT`, `AWAITING_PLAN_REVIEW`, `REPLANNING`, `READY`, `IMPLEMENTING`, `AWAITING_IMPLEMENTATION_REVIEW`, `ACCEPTED`, `REJECTED`, `BLOCKED`.

Threshold states:

`CLEAR`, `PLAN_REVIEW_THRESHOLD_EXCEEDED`, `IMPLEMENTATION_REVIEW_THRESHOLD_EXCEEDED`, `DIAGNOSIS_REQUIRED`, `BACK_TO_BASICS_DONE`.
