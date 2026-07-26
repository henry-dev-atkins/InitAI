---
name: final-report
description: Use before final reports for implementation, proof, debugging, refactoring, orchestration and spec-alignment tasks, especially when deciding whether [DONE] or [BLOCKED] is justified.
---

# [DONE] / [BLOCKED]

## `[DONE]` requires

- The requested change exists in repo state, not only in docs/plans/reports.
- The change is complete, coherent and aligned with the spec or explicit human instruction.
- Relevant checks or real runs have passed at the right stage.
- Exact validation commands/checks and pass results are reported.
- Config, docs and outputs are updated where behaviour changed.
- Obsolete assumptions and replaced logic in touched areas are cleaned up.
- Learnings, TODOs and handovers are updated when relevant.
- Required spec alignment passes `[SPEC.REVIEW]`.
- No in-scope gaps, stubs, workarounds, cosmetic completions or silently deferred items remain.
- Work Type rules were followed.

## Orchestrated `[DONE]`

A worker `[DONE]` means only that the worker task packet is complete.

A session `[DONE]` additionally requires:

- session board updated
- result packets collected
- merge/integration status reported
- accepted worker changes integrated in the current checkout or explicitly left for human review
- global validation complete
- final `[SPEC.REVIEW]` complete
- no unresolved in-scope worker remains

## `[BLOCKED]` requires

Use `[BLOCKED]` only after a concrete implementation/validation attempt fails for a reason outside current authority, available tools or safe operating limits.

Report:

- exact failed/unavailable command or check
- exact remaining error/blocker
- concrete repair attempts already made
- files changed
- smallest next human decision/action needed
- checkout/worker/integration status when orchestrated

Do not report `[DONE]` if validation failed, validation was skipped by choice, or the requested behaviour is still absent.
