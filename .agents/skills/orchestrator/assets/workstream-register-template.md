# Workstream Register

Only the orchestrator creates workstreams or changes state.

| Workstream | Outcome | Findings | Requirement IDs | Work Type | Workflow Class | Depends On | Write Scope | Stable Read Scope | Contracts Changed | Contracts Consumed | Mutable Resources | Plan | Predecessor Plan | Rejected Plans | Rejected Implementations | Threshold State | Baseline Snapshot | Scope Diff | Accepted State | Accepted Tree Hash | State |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---:|---|---|---|---|---|---|
| WS001 | `{coherent result}` | F001 | REQ001 | `{WORK_TYPE}` | STANDARD | none | `{paths}` | `{paths-or-none}` | `{CON IDs}` | `{CON IDs}` | `{resource IDs-or-none}` | P001 | none | 0 | 0 | CLEAR | `{path-or-none}` | `{path-or-none}` | `{path-or-none}` | `{hash-or-none}` | AWAITING_PLAN |

States:

`AWAITING_PLAN`, `PLANNING`, `AWAITING_PLAN_COLLATION`, `AWAITING_PLAN_PREFLIGHT`, `AWAITING_PLAN_REVIEW`, `REPLANNING`, `READY`, `IMPLEMENTING`, `AWAITING_IMPLEMENTATION_REVIEW`, `ACCEPTED`, `REJECTED`, `BLOCKED`, `CANCELLED`, `SUPERSEDED`.

Threshold states:

`CLEAR`, `PLAN_REVIEW_THRESHOLD_EXCEEDED`, `IMPLEMENTATION_REVIEW_THRESHOLD_EXCEEDED`, `DIAGNOSIS_REQUIRED`, `BACK_TO_BASICS_DONE`.
