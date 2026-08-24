---
name: terminal-condition
description: Use when the prompt contains [PLAN.TERMINAL_CONDITION] or [TERMINAL_CONDITION], or when the orchestrator must prove the repository fully matches AI_SPACE/SPEC.md.
---

# [PLAN.TERMINAL_CONDITION] / [TERMINAL_CONDITION]

The terminal condition is an evidence-backed clean spec review of one frozen repository revision.

## Preconditions

Do not start terminal review until:

- the canonical finding register has no open finding or unwaived deferred requirement;
- no workstream is active, awaiting review, rejected or blocked;
- `requirement_register.json` validates against the current `AI_SPACE/SPEC.md` hash and has no uncovered line range;
- the reviewed global validation manifest passes through the trusted runner;
- temporary diagnostics, disposable artefacts and unapproved workarounds are absent from active project paths; retained product recovery copies may exist only under repository-root `archive/`, and retained control-plane copies only under `AI_SPACE/archive/`;
- the session campaign baseline exists and the canonical active repository tree hash from `tree_hash.py` is recorded.

## Review batch

Run six read-only spec-review agents in parallel against the same recorded active-tree hash. Assign explicit requirement ID ranges whose union covers the complete requirement register, plus distinct lenses:

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
- every atomic spec requirement has implementation and validation evidence, or an explicit current human-authorised waiver;
- no reviewer reports missing logic, extra logic, missing files, extra active product files, fluff, overengineering or unsupported behaviour;
- product archive material is confined to repository-root `archive/`, control-plane archive material to `AI_SPACE/archive/`, and neither participates in active imports, execution, configuration or product behaviour;
- global validation still passes through its manifest-bound evidence ledger;
- `validate_terminal_coverage.py` proves that every active-tree mutation since the campaign baseline belongs to the latest accepted state of an `ACCEPTED` workstream;
- the canonical active-tree hash is unchanged from the start of terminal review.

If any reviewer reports a disputed, weakly evidenced or non-mechanical finding, verify it through `$verify-finding` before promotion. The orchestrator assigns stable finding IDs to verified or mechanically proven findings, resumes the normal workstream loop and does not declare `[DONE]`.

## Early exit

Early exit is `[BLOCKED]`, never `[DONE]`, and only for unavailable authority, tooling, data or a safe execution path that the current session cannot resolve.
