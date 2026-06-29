---
name: EDIT_SPEC
description: Use only when the prompt includes [SPEC EDIT REQUIRED]. Plans, reviews, and applies a minimal edit to AI_SPACE/SPEC.md, then reviews downstream consequences.
--- 

# Workflow
The SPEC file may be edited only if `[SPEC EDIT REQUIRED]` is present in the prompt.
Edits must follow a strict workflow to ensure consequences are carefully followed, if any phase fails, the workflow must be restarted from the beginning. The workflow is as follows:
1) Is [EDIT_SPEC] present in prompt?
2) Plan the edit
3) PLAN_REVIEW of the plan
4) SPEC_REVIEW of the prosed plan
5) Implement the edit