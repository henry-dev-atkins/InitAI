---
name: campain-review
description: Perform a double-loop review when no-progress detection indicates that retrying within the current framing is unlikely to converge.
---

# [CAMPAIN.REVIEW]

Instead of asking:

  Is the current implementation/plan correct?

We ask:

  Are we solving/decomposing/framing the problem correctly in the first place?

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
