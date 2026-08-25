---
name: plan-blastradius
description: Optional impact check for a plan or accepted implementation that changes a shared interface, schema, config contract or other widely consumed behaviour.
---

# [PLAN.BLASTRADIUS]

Identify concrete consumers that may be affected by the proposed or completed change.

Output:

- affected files/components;
- why they are affected;
- whether the current plan already covers the impact;
- `CLEAR`, `REVIEW_REQUIRED`, or `REPLAN_REQUIRED`.

Use only when shared behaviour makes blast radius material. Do not turn every local plan into a dependency-analysis phase.
