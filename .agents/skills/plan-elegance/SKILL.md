---
name: plan-elegance
description: Review proposed repo changes for solution elegance before implementation. Use when Codex needs to decide whether a plan is the simplest coherent route to the requested capability, fits the existing repo cleanly, avoids unnecessary files/classes/configs/runners/abstractions, and preserves elegant codebase structure.
---

# Plan Elegance

Review whether a proposed change is the most elegant practical route to the requested outcome and whether it fits the repo as cleanly as possible.

This is a plan review output. Do not edit files, stage files, commit, or implement fixes unless a separate workflow explicitly asks for implementation.

## Review Focus

- Goals: Can we acheive the stated goal in a simpler way? how many simpler ways are there?
  - Are we adding software for softwares sake?
  - Can we drop an API and maintain capability and logic?
- Directness: does the plan reach the requested capability without avoidable support work?
- Repo fit: does it reuse existing patterns, ownership boundaries, and execution paths where they are still appropriate?
- Simplicity: can the plan use fewer concepts, files, classes, config keys, runners, or abstractions?
- Integration: will the result feel like part of this repo rather than an attached subsystem?
- Sequencing: does the plan build the core behaviour before polishing surrounding software unless support work directly enables it?
- Consequences: does the plan avoid likely follow-up cleanup, tangled ownership, or duplicated implementation paths?
- Validation: does the validation prove the behaviour that matters, not just the scaffolding around it?

## Revision Triggers

- A simpler implementation path is visible and not addressed.
- The plan adds new structure where existing repo structure can carry the work.
- The plan standardises execution before proving the relevant behaviour.
- The plan creates future migration or cleanup work that a more direct design would avoid.
- The plan hides capability logic behind abstractions that do not remove real complexity.

## Output

Use this short report structure:

```text
Verdict: ELEGANT | NEEDS_REVISION | BLOCKED

Findings
- finding-or-none

Repo Fit
- fit-or-none

Required Plan Changes
- change-or-none

Follow-up
- follow-up-or-none
```

Use `ELEGANT` only when no clearly simpler or cleaner plan is visible. Use `NEEDS_REVISION` when the plan can be tightened before implementation. Use `BLOCKED` when the proposed solution is too misaligned with repo structure or core capability order to implement safely.
