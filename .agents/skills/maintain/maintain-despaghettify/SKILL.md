---
name: maintain-despaghettify
description: Review repo/codebase structure for spaghettification, tangled responsibilities, code explosions, unclear module boundaries, excessive indirection, duplicated logic, dependency spread, and coupling that distracts from core spec/capability work. Use when Codex is asked to despaghettify, untangle, simplify, or review spaghetti-like code/repo structure, including misspelt prompts such as spagetti.
---

# Maintain Despaghettify

Review whether the repo/codebase structure is becoming tangled and identify the smallest coherent untangling action.

This is a repo/codebase review output. Do not rewrite files, move files, stage files, commit, or implement restructuring unless a separate workflow explicitly asks for implementation.

## Review Focus

- Module boundaries: each module, file, script, and config area should have a clear repo responsibility.
- Data flow: capability logic should be easy to trace through the codebase.
- Coupling: unrelated behaviours should not need to change together.
- Duplication: repeated logic or config ownership should be reduced when it raises real maintenance cost.
- Indirection: abstractions should remove real complexity, not hide straightforward capability code.
- Code growth: new files/classes/functions should earn their place by serving the spec or core capability.
- Goal focus: restructuring should make capability work easier, not become a substitute for it.

## Untangling Rules

- Prefer the smallest repo change that restores clear ownership.
- Prefer deleting duplication by replacing it with one direct implementation path; do not preserve legacy alternatives.
- Prefer simple module boundaries over broad frameworks.
- Do not recommend a large restructure when a narrow move, rename, or simplification would solve the problem.
- Raise a blocker if the current structure makes the core capability difficult to implement, validate, or review.

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

Use `PASS` only when repo responsibilities are clear and no smaller simplification is needed. Use `NEEDS_REVISION` when local untangling or contract tightening is enough. Use `BLOCKED` when the repo structure prevents credible capability progress.
