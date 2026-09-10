---
name: workflow-structure
description: Define the minimal AI_SPACE file layout for the simplified conformance, workstreams, plans, and implementation-review loop.
---

# [WORKFLOW_STRUCTURE]

Use this structure for substantial orchestrated work:

```text
AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/
  misalignments.md
  workstreams.md
  selected_workstreams.md
  plans/
    WS001__P001.md
  plan_reviews/
    WS001__P001.md
  implementation_reviews/
    WS001.md
```

Optional diagnostics, prototypes, learnings and handovers stay in their existing intentional locations.

Do not create additional workflow files merely because a template exists. The spec remains the product authority.
