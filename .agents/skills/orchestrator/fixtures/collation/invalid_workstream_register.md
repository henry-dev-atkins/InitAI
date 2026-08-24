# Workstream Register

| Workstream | Outcome | Findings | Requirement IDs | Work Type | Workflow Class | Depends On | Write Scope | Stable Read Scope | Contracts Changed | Contracts Consumed | Mutable Resources | Plan | Predecessor Plan | Rejected Plans | Rejected Implementations | Threshold State | Baseline Snapshot | Scope Diff | Accepted State | Accepted Tree Hash | State |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WS003 | escaped plan | F003 | REQ003 | AGENT.WORKFLOW | STANDARD | WS004 | src/../../outside | src/shared | CON003 | none | GPU0 | P003 | none | 0 | 0 | CLEAR | none | none | none | none | AWAITING_PLAN_COLLATION |
| WS004 | unaccepted dependency | F004 | REQ004 | AGENT.WORKFLOW | STANDARD | none | src/shared | none | CON003 | none | GPU0 | P004 | none | 0 | 0 | CLEAR | none | none | none | none | READY |
| WS005 | duplicate plan | F005 | REQ005 | AGENT.WORKFLOW | STANDARD | none | src/shared/sub | none | none | CON003 | GPU0 | P003 | none | 0 | 0 | CLEAR | none | none | none | none | AWAITING_PLAN_COLLATION |
