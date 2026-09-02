---
name: conformance
description: Compare AI_SPACE/SPEC.md with the current repository and return an exhaustive list of material misalignments, or PASS when none remain. This is the outer convergence test for the orchestrator loop. SPEC.REVIEW == SPEC_REVIEW == conformance
---

# [SPEC.REVIEW]

Review the current repository against `AI_SPACE/SPEC.md`.
Compare the assigned repository scope against `AI_SPACE/SPEC.md`. Report facts and evidence; do not plan fixes or manage process.

Review lenses may include:

- requirement coverage;
- behaviour and logic;
- implementation correctness;
- files/modules/configuration/outputs;
- extra or prohibited behaviour;
- validation and edge cases;
- defensibility and implementation laziness;
- Work Type/capability-progress claims;
- minimality, maintainability and convergence;
- archived material is historical recovery evidence only and must not participate in active imports, execution, configuration or product behaviour.

Output only evidence-backed misalignments. Do not plan fixes or choose workstreams.

Each finding contains:

- `Finding ID`: stable when the orchestrator supplied one, otherwise a proposed ID;
- `Spec authority`: exact section or quoted requirement;
- `Repository evidence`: exact files, behaviour, config, tests, or absence;
- `Expected`;
- `Actual`;
- `Severity`;
- `Affected area`.

Return `PASS` with an empty list only when the reviewed spec scope has no material misalignment.

For large specs, divide the spec or repository inspection among read-only sub-agents when useful, then collate their findings without duplication. Coverage should be exhaustive enough that a clean result is meaningful.

Use `$finding-verification` only for disputed, ambiguous, or weakly evidenced findings. A clear finding does not need another workflow stage.
