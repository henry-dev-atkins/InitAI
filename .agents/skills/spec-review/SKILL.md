---
name: spec-review
description: Use when the prompt contains [SPEC.REVIEW] or [SPEC_REVIEW], or when implementation, plans, worker results, or merge candidates must be compared against AI_SPACE/SPEC.md.
---

# [SPEC.REVIEW] / [SPEC_REVIEW]

Compare implementation to the specification. Scope may be a subset of the spec, but the subset must be named.

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

## Orchestrated review

For worker branches/result packets, check:

- task packet authority
- files changed versus allowed scope
- whether the Primary Work Type is correct
- whether capability progress is genuinely spec-backed
- whether validation proves the claimed behaviour
- whether any dependency/docs/cleanup/workaround work is masquerading as capability completion
- whether temporary diagnostic/fluff artefacts remain

Write each blocking misalignment into `AI_SPACE/TODO.md` only if it is concrete unresolved follow-up work. Do not use TODO updates as closure.

## Output

```yaml
spec_review_status: PASS | NON_BLOCKING_FINDINGS | BLOCKING_FINDINGS
scope_reviewed:
  - {spec section/path}
blocking_findings:
  - {finding-or-none}
non_blocking_findings:
  - {finding-or-none}
capability_progress_supported: yes | no | not_applicable
merge_permission: yes | no | not_applicable
```
