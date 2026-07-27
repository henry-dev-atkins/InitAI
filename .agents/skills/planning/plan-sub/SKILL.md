---
name: plan-sub
description: Use when the prompt contains [PLAN.SUB] or [SUBPLAN], or when an accepted workstream plan needs a bounded supporting subplan.
---

# [PLAN.SUB] / [SUBPLAN]

A subplan is a bounded supporting component of one parent workstream. It does not create a separate workflow or bypass plan review.

Rules:

- Name the parent workstream and plan.
- Keep the parent's Primary Work Type unless the subplan is temporary diagnostic/support work explicitly labelled as such.
- If the work has an independent durable outcome, the orchestrator must create a separate workstream instead.
- Temporary diagnostics must not be committed and must be removed/archived before terminal completion.
- A separate owner requires orchestrator-approved locks, dependencies and contract scope.
- Completion returns to the parent workstream; only the orchestrator changes workstream state.

Store subplan artefacts inside the parent `workstream__WSXXX__short-name/` folder according to `$workflow-structure`.
