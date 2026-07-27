---
name: spec-review
description: Use when the prompt contains [SPEC.REVIEW] or [SPEC_REVIEW], or when implementation, plans, worker results, or merge candidates must be compared against AI_SPACE/SPEC.md.
---

# [SPEC.REVIEW] / [SPEC_REVIEW]

Compare repo to the spec. Scope may be a named subset of the spec & repo.

Review categories:

- Capability
- Logic
- Implementation
- Correctness
- Documentation
- Outputs
- Defensibility
- Implementation laziness
- Work Type classification
- Capability progress claims
- Convergence to spec

## Role boundary

Spec-review agents are factual reviewers, not process managers.

- Do not suggest next steps, propose repair packets, choose future work, or tell the orchestrator what to do after the review.
- Do not include fields such as `next_step`, `recommended_next_action`, `recommended_plan`, or similar process-direction text.

## Output

```yaml
spec_review_status: PASS | NON_BLOCKING_FINDINGS | BLOCKING_FINDINGS
scope_reviewed:
  - {spec section/path}
blocking_findings:
  - {finding-or-none}
non_blocking_findings:
  - {finding-or-none}
core_behaviour_gaps:
  - {finding-or-none}
support_software_gaps:
  - {finding-or-none}
priority_evidence: core_behaviour | direct_support_enabler | evidence_insufficient | not_applicable
capability_progress_supported: yes | no | not_applicable
merge_permission: yes | no | not_applicable
```

For planning reviews, order `blocking_findings` and `core_behaviour_gaps` by spec-convergence impact. The order is severity evidence for the orchestrator; it is not an instruction.