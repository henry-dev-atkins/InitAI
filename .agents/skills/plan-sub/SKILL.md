---
name: plan-sub
description: Use when the prompt contains [PLAN.SUB] or [SUBPLAN], or when a plan needs a temporary aside/subplan that returns to the parent plan after completion.
---

# [PLAN.SUB] / [SUBPLAN]

A subplan is a bounded temporary aside from a parent plan. Name the parent `[PLAN_A]` and the subplan `[PLAN_B]`.

Rules:

- The agent must return to `[PLAN_A]` after `[PLAN_B]` completion.
- Every subplan still needs exactly one Primary Work Type.
- If the subplan has a different durable purpose, record it as a separate plan package.
- If the subplan is temporary diagnostic work, it must not be committed and must be removed/archived before parent `[DONE]`.
- In orchestrated work, a subplan may get its own owner agent only if the orchestrator updates locks and the session board.

Store subplans inside the parent plan folder according to `$workflow-structure`.
