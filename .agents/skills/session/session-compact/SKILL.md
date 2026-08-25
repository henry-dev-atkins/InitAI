---
name: session-compact
description: Compact a long AI_SPACE session by preserving accepted plans/reviews and replacing noisy transient notes with one short current-state summary.
---

# [SESSION.COMPACT]

Keep:

- latest misalignment list;
- current workstream list;
- accepted/rejected plan history needed to avoid repetition;
- implementation reviews;
- unresolved blockers and reusable learnings.

Move superseded control notes to `AI_SPACE/archive/`. Do not alter `AI_SPACE/SPEC.md` or product source.

The compacted state must still make the next operation in the simple orchestrator loop obvious.
