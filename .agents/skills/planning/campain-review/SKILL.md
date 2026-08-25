---
name: campain-review
description: Optional back-to-basics review when repeated plan or implementation failures suggest the current workstream split or direction is wrong.
---

# [CAMPAIN.REVIEW]

Use after repeated failure, persistent blocking, or evidence that the current workstream decomposition is wrong.

Ask:

- `Am I going in Circles?`
- `Is there a more elegant way of doing this?`

Review the current misalignments, workstream boundaries, repeated failures, and actual repository evidence.

Return one of:

- `CONTINUE`: the current workstream structure is still sound;
- `RECOLLATE`: return the current misalignments to `$plan-portfolio`;
- `REREVIEW_SPEC`: run a fresh `$spec-review` now.

Do not create a second campaign state machine.
