---
name: spec-edit
description: Use only when the prompt contains [SPEC.EDIT_REQUIRED]. Plan, review, and apply a minimal edit to AI_SPACE/SPEC.md, then review downstream consequences.
---

# Editing The Spec
The SPEC file may be edited only if `[SPEC.EDIT_REQUIRED]` is present in the prompt.
Edits must follow a strict workflow to ensure consequences are carefully followed, if any phase fails, the workflow must be restarted from the beginning. The workflow is as follows:
1) Is `[SPEC.EDIT_REQUIRED]` present in prompt?
2) Plan the edit
3) [PLAN.REVIEW] of the plan
4) [SPEC.REVIEW] of the proposed plan
5) Implement the edit
