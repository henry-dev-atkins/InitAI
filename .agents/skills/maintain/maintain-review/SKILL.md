---
name: maintain-review
description: Review repo/codebase changes, plans, implementations, or merge candidates for drift away from the project spec and core capabilities. Use when Codex needs to check whether work adds avoidable surrounding software, abstractions, runners, framework code, documentation-only progress, or other repo complexity instead of advancing the project goal.
---

# Maintain Review

Review the repo change against the project goal: avoid spaghettification, tech debt, and code explosions while keeping implementation focused on core spec capabilities.

This is a repo/codebase review output. Do not edit files, move files, stage files, commit, or implement fixes unless a separate workflow explicitly asks for implementation.

## Review Focus

- Goal focus: does the change advance the spec-backed capability or explicit repo goal?
- Capability priority: does the work build or repair the core behaviour before polishing surrounding software?
- Repo complexity: does the change add unnecessary modules, runners, config machinery, abstractions, reporting, or support code?
- Minimalism: is there a smaller coherent repo change that would deliver the same capability progress?
- Elegance: would `maintain-elegance` likely find a simpler whole-repo shape for this capability?
- Closure: does validation prove the repo behaviour, not only the surrounding tool or structure?
- Work Type: is support work being claimed as capability progress?

## Red Flags

- Building a framework, runner, or abstraction layer before the underlying behaviour exists.
- Adding broad infrastructure when a direct script, function, or focused module would move the capability forward.
- Expanding repo surface area without a clear spec-backed reason.
- Treating docs, cleanup, dependency work, or validation scaffolding as if it were capability implementation.
- Deferring the real implementation behind a new support layer.
- Leaving the repo harder to reason about after the change.

These are warning signs, not fixed bans. Support software is acceptable when it is the shortest practical route to the next repo capability and the plan explains why.

## Output

Use this short report structure:

```text
Verdict: PASS | NEEDS_REVISION | BLOCKED

Findings
- finding-or-none

Core Capability Impact
- impact-or-none

Required Changes
- change-or-none

Follow-up
- follow-up-or-none
```

Use `PASS` only when the repo change stays focused, preserves maintainability, and supports the claimed capability progress. Use `NEEDS_REVISION` when the work can continue after tightening. Use `BLOCKED` when the change cannot be accepted without re-targeting the core repo goal.
