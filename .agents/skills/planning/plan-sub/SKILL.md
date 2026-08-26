---
name: plan-sub
description: Break an accepted plan step into local execution substeps without changing the accepted workstream outcome, scope, requirements or validation intent. A sub-plan is a plan within a plan.
---

# [PLAN.SUB]

Use only inside an accepted workstream plan when the implementation agent needs a clearer local sequence.

Allowed:

- reorder local execution for safety;
- break one accepted step into smaller coding/testing steps;
- identify a read-only inspection needed before editing.

Forbidden:

- new product requirements;
- broader write scope;
- new workstreams;
- changed acceptance criteria;
- architectural changes outside the accepted plan;
- portfolio or orchestration decisions.

If one of those is needed, stop and return to normal planning.
