---
name: maintain-techdebt
description: Review repo/codebase changes for technical debt, future maintenance cost, brittle implementation, unnecessary dependencies, hard-to-change abstractions, duplicated logic, and debt that blocks or slows core spec/capability progress. Use during plan review, spec review, implementation review, cleanup, and learning when repo maintainability is at stake.
---

# Maintain Techdebt

Review technical debt in the repo/codebase and decide whether it should block, shape, or be tracked after the current work.

This is a repo/codebase review output. Do not edit files, move files, stage files, commit, or implement fixes unless a separate workflow explicitly asks for implementation.

## Orchestrator Review-Lens Mode

When invoked inside `$orchestrator` plan review or implementation review:

- return findings, repository evidence, materiality/severity and acceptance evidence only;
- do not return commands, required-change instructions, repair guidance, follow-up actions, scheduling advice or next-step fields;
- do not change finding/workstream state or issue the parent review verdict;
- the parent `plan-review` or implementation reviewer owns the final verdict and the orchestrator owns all subsequent action.

## Review Focus

- Future cost: will this code be hard to change, test, extend, or remove?
- Brittleness: does it depend on hidden state, fragile ordering, machine-local assumptions, or unclear side effects?
- Duplication: does it repeat logic, config ownership, schemas, validation, or data flow in multiple places?
- Dependency cost: does it add or deepen dependencies without clear capability value?
- Debt priority: does the debt block the current capability, shape the current plan, or belong as later cleanup?
- Spec focus: does the debt pull the repo away from the project’s core capabilities?

## Severity

- `BLOCKING`: must be resolved before accepting the work.
- `HIGH`: should be resolved in the same plan unless explicitly deferred.
- `MEDIUM`: should be tracked or handled soon.
- `LOW`: note only when it helps future maintenance.

Do not create a debt list as a substitute for fixing a current blocker. If debt blocks the capability, say so directly.

## Output

Use this short report structure:

```text
Verdict: PASS | NON_BLOCKING_DEBT | BLOCKING_DEBT

Findings
- severity: finding; repository evidence; capability impact; acceptance evidence

Core Capability Impact
- impact-or-none
```

Use `PASS` only when no meaningful repo technical debt affects the work. Use `NON_BLOCKING_DEBT` when the work can proceed with explicit tracking or small changes. Use `BLOCKING_DEBT` when accepting the work would preserve or introduce serious repo debt.
