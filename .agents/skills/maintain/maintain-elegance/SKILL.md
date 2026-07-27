---
name: maintain-elegance
description: Review repo-wide codebase elegance across features, APIs, execution paths, logic flow, module boundaries, data flow, abstractions, and capability fit. Use when Codex needs to assess whether the existing repo or merged implementation is as simple, coherent, direct, and spec-focused as reasonably possible.
---

# Maintain Elegance

Review whole-codebase elegance: whether the repo expresses its core spec capabilities with the fewest useful concepts, the clearest flow, and the least avoidable complexity.

This is a repo/codebase review output. Do not edit files, move files, stage files, commit, or implement fixes unless a separate workflow explicitly asks for implementation.

## Orchestrator Review-Lens Mode

When invoked inside `$orchestrator` plan review or implementation review:

- return findings, repository evidence, materiality/severity and acceptance evidence only;
- do not return commands, required-change instructions, repair guidance, follow-up actions, scheduling advice or next-step fields;
- do not change finding/workstream state or issue the parent review verdict;
- the parent `plan-review` or implementation reviewer owns the final verdict and the orchestrator owns all subsequent action.

## Review Focus

- Capability expression: does the repo make the core behaviour easy to find, run, validate, and change?
- Concept count: are there unnecessary features, APIs, configuration layers, runners, abstractions, or execution paths?
- Logic flow: can a reader trace data, control, and errors through the repo without detours?
- Repo fit: do new and old parts share clear patterns, naming, ownership, and boundaries?
- Simplicity: could the same capability be expressed with fewer moving parts?
- Change cost: would a likely next capability change be local and understandable?
- Removal pressure: are there concepts that no longer earn their place?

## Elegance Signals

- One clear path for each important behaviour.
- Small, named boundaries that match real domain or capability concepts.
- Direct implementation where abstraction would not remove real complexity.
- Config, scripts, and APIs that serve behaviour rather than becoming the product.
- Code that makes unsupported states obvious and failure modes loud.

## Output

Use this short report structure:

```text
Verdict: ELEGANT | NEEDS_TIGHTENING | INELEGANT

Findings
- severity: finding; repository evidence; capability impact; acceptance evidence

Core Capability Impact
- impact-or-none
```

Use `ELEGANT` only when the repo is already clear and no meaningful simplification is visible. Use `NEEDS_TIGHTENING` when local simplification would improve repo fit. Use `INELEGANT` when the repo-wide shape obscures or slows core capability progress.
