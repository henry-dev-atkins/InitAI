---
name: show-me-your-work
description: Keep a compact evidence trail for long or unattended repository work. Use when a reviewer needs decisions, pivots, blockers, and validation linked to real artefacts.
---

# Show me your work

Keep one append-only decision log for the task.

Store it under `AI_SPACE/sessions/` or the task's existing session directory.

Use one row per decision, pivot, blocker, or completed checkpoint.

Each row records the timestamp, workstream, decision, reason, evidence path, and result.

Evidence must point to a file, command result, test, diff, or commit.

Do not log routine tool calls or intentions that did not happen.

When a decision changes, append the correction. Do not rewrite the earlier row.

Keep cells on one line and use a format that the current session tools already support.

Before handoff, check that each row matches the repository state and that each evidence path exists.

Use the normal session handover for the full current state. This log records decisions, not a second handover.
