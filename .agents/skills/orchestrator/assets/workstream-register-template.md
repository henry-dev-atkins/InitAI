# Workstream Register

Only the orchestrator creates workstreams or changes state.

| Workstream | Outcome | Findings | Work Type | Depends On | Write Scope | Contracts Changed | Contracts Consumed | Plan | State |
|---|---|---|---|---|---|---|---|---|---|
| WS001 | `{coherent result}` | F001 | `{WORK_TYPE}` | none | `{paths}` | `{contracts}` | `{contracts}` | P001 | AWAITING_PLAN |

States:

`AWAITING_PLAN`, `PLANNING`, `AWAITING_PLAN_REVIEW`, `REPLANNING`, `READY`, `IMPLEMENTING`, `AWAITING_IMPLEMENTATION_REVIEW`, `ACCEPTED`, `REJECTED`, `BLOCKED`.
