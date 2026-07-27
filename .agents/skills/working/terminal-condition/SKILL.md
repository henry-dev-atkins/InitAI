---
name: terminal-condition
description: Use when the prompt contains [PLAN.TERMINAL_CONDITION] or [TERMINAL_CONDITION], or when the orchestrator must prove the repository fully matches AI_SPACE/SPEC.md.
---

# [PLAN.TERMINAL_CONDITION] / [TERMINAL_CONDITION]

The terminal condition is an evidence-backed clean spec review of one frozen repository revision.

## Preconditions

Do not start terminal review until:

- the finding register has no open findings;
- no workstream is active, awaiting review, rejected or blocked;
- global validation passes;
- temporary diagnostics, disposable artefacts and unapproved workarounds are absent from active project paths; retained recovery copies may exist only under `archive/`;
- the exact repository revision/tree hash is recorded.

## Review batch

Run six read-only spec-review agents in parallel against the same recorded revision. Assign distinct lenses:

1. atomic requirement coverage;
2. behavioural correctness;
3. files, modules, configuration and outputs;
4. extra/prohibited logic and unnecessary files;
5. validation, edge cases and failure behaviour;
6. holistic integration, minimality and spec convergence.

Each reviewer must return `PASS` or evidence-backed findings using the `$spec-review` schema. Missing evidence is not a pass.

## Pass condition

Terminal review passes only when:

- all six reviewers return `PASS`;
- every atomic spec requirement has implementation and validation evidence;
- no reviewer reports missing logic, extra logic, missing files, extra active product files, fluff, overengineering or unsupported behaviour;
- archived material is confined to `archive/` and is not imported, executed, configured or otherwise part of current behaviour;
- global validation still passes;
- the repository revision/tree hash is unchanged from the start of terminal review.

If any reviewer reports a finding, the orchestrator assigns stable finding IDs, resumes the normal workstream loop and does not declare `[DONE]`.

## Early exit

Early exit is `[BLOCKED]`, never `[DONE]`, and only for unavailable authority, tooling, data or a safe execution path that the current session cannot resolve.
