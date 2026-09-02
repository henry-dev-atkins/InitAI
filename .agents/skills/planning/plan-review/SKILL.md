---
name: plan-review
description: Independently review one workstream plan for spec alignment, completeness, scope, validation and implementation clarity. Return ACCEPT, REJECT or BLOCKED.
---

# [PLAN.REVIEW]

Review one plan against its workstream findings, `AI_SPACE/SPEC.md`, and the relevant repository state.

Return exactly one verdict:

- `ACCEPT`;
- `REJECT`;
- `BLOCKED`.

Accept only when the plan:

- addresses the source findings and spec authority;
- has one coherent outcome;
- has a clear bounded write scope;
- gives an implementation agent enough detail to work without product invention;
- includes meaningful validation;
- protects important invariants;
- avoids legacy compatibility, band-aids, silent fallback and unrelated work;
- answers `Am I going in Circles?`;
- answers `Is there a more elegant way of doing this?`

- preflight status and unresolved mechanical defects;
- source finding and spec traceability;
- one coherent workstream outcome;
- correct Primary Work Type;
- capability-first alignment with assigned findings;
- top-down convergence impact;
- minimal complete implementation;
- exact write/off-limits scope;
- dependencies and parallel-safety;
- contracts changed/consumed;
- protected invariants and prohibited behaviour;
- implementation-order logic;
- behavioural validation strength;
- structured command/evidence manifest quality;
- result-packet and evidence-ledger completeness;
- overengineering, technical debt and repository fit;
- whether `Am I going in Circles?` honestly identifies repeated or reactive work;
- whether `Is there a more elegant way of doing this?` considers a simpler complete repository-fitting route.

Use retained supporting lenses when relevant:

- `plan-elegance`;
- `maintain-review`;
- `maintain-elegance`;
- `maintain-techdebt`;
- `maintain-despaghettify`;
- `maintain-declutter`;
- `peer-review`.

They inform this single plan-review verdict; they do not create additional workflow phases.

A rejection returns concrete findings about the plan. Do not write the replacement plan inside the review.

Use `$plan-preflight`, `$change-impact-analysis`, `$plan-elegance`, `$peer-review`, or maintenance skills as optional review lenses when their question matters. They do not add stages to the orchestrator loop.


## Capability-first gate

Reject support-only churn unless it directly unlocks the assigned capability or evidence required by the workstream. Planning may include workflow, validation or local infrastructure only when it is the shortest complete route to resolving the source findings.

## Reject when

- preflight has not passed;
- the workstream/finding/spec traceability is absent or incorrect;
- the plan does not fully remove the assigned misalignment;
- it broadens into unrelated work or fragments one coherent result unnecessarily;
- it starts with support software without showing that it is the shortest route to required behaviour;
- support-only work claims capability progress or displaces open capability findings;
- exact file scope, dependencies, contract effects or owner are missing;
- it conflicts with another active workstream;
- validation is vague, toy-only or does not prove the assigned behaviour;
- command manifest or evidence ledger requirements are incomplete;
- temporary/workaround/fluff output may survive;
- capability progress is claimed for support-only work;
- a simpler repository-fitting solution is clearly available and unaddressed;
- it relies on an assumed later repair pass;
- There is a more elegant way of doing it;
- either required reflection section is missing, superficial or contradicted by the plan.

`BLOCKED` is only for missing authority, tooling, data or a safe execution path, not ordinary plan defects.
