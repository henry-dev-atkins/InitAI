---
name: spec-review
description: Use when the prompt contains [SPEC.REVIEW] or [SPEC_REVIEW], or when the repository, a plan or an implementation must be compared with AI_SPACE/SPEC.md.
---

# [SPEC.REVIEW] / [SPEC_REVIEW]

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

## Role boundary

- Do not choose future work, create workstreams, write plans, recommend packets or tell the orchestrator what to do.
- Do not edit files.
- Do not include `next_step`, `recommended_next_action`, `recommended_plan` or similar process-direction fields.
- A lack of evidence is a finding, not a reason to assume PASS.

## Finding rules

Each finding must identify:

- a report-local source finding ID;
- exact spec requirement/section;
- exact repository evidence;
- expected behaviour/state;
- actual behaviour/state;
- severity and why it matters;
- affected files/behaviour;
- evidence that would prove resolution.

The orchestrator owns deduplication and stable global finding IDs.

## Output

```yaml
review_id: RXXX
review_lens: requirement_coverage | behaviour | files_and_config | extra_logic | validation | holistic | assigned_scope
repo_revision: {commit-or-tree-hash}
scope_reviewed:
  spec:
    - {section-or-requirement}
  repo:
    - {path-or-component}
review_status: PASS | FINDINGS
findings:
  - source_finding_id: RXXX-F001
    spec_authority: {exact section/requirement}
    severity: critical | high | medium | low
    expected: {spec-required state}
    actual: {observed repo state}
    evidence:
      - {path:line, command result, or reproducible observation}
    affected_files:
      - {path}
    affected_behaviour: {concise description}
    resolution_evidence: {what would prove alignment}
coverage_evidence:
  - spec_requirement: {requirement}
    implementation_evidence: {path/behaviour}
    validation_evidence: {test/command/result or missing}
```

Return `PASS` only when the assigned scope has no findings and sufficient coverage evidence.
