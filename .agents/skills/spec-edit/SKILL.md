---
name: spec-edit
description: Use only when the prompt contains [SPEC.EDIT_REQUIRED] or [SPEC EDIT REQUIRED]. Plan, review, and apply a minimal edit to AI_SPACE/SPEC.md, then review downstream consequences.
---

# [SPEC.EDIT_REQUIRED] / [SPEC EDIT REQUIRED]

The spec may be edited only if `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` is present in the prompt.

Workflow:

1. Confirm the spec-edit trigger is present.
2. Classify as `SPEC.EDIT` using `[WORK_TYPE]`.
3. Plan the edit.
4. Run `[PLAN.REVIEW]`.
5. Run `[SPEC.REVIEW]` of the proposed plan.
6. Apply the smallest spec edit.
7. Review downstream consequences.
8. Update TODOs/plans if the target changed.

Do not use spec edits to evade implementation work.
