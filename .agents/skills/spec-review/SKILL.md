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

Use `maintain-review` when implementation or worker results may be claiming progress through repo complexity, dependency work, cleanup, documentation, wrapper code, or support software instead of spec-backed behaviour. Use `maintain-elegance` when repo-wide implementation shape affects capability clarity or merge readiness. Use `maintain-techdebt` for repo technical debt that affects merge permission. If `AI_SPACE/SPEC.md` is absent, do not infer project intent; report the missing spec and limit review to explicit prompt/task authority.

When returning findings for planning, separate core behaviour gaps from surrounding support/software gaps. Do not force one universal ordering rule: use reviewer judgement and the Work Type ontology. The next plan should generally target core behaviour first unless a support item directly enables the next spec-backed behaviour step.

Spec review's shoudl highlight large misalignments over smaller ones. This means that successive `spec-review`->impleentation loops progressivly handle lower level work after high llevel alignment. This minimises code bloat. 

## Orchestrated review

For worker result packets and the accumulated checkout, check:

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
core_behaviour_gaps:
  - {finding-or-none}
support_software_gaps:
  - {finding-or-none}
planning_priority: core_behaviour | direct_support_enabler | reviewer_judgement | not_applicable
capability_progress_supported: yes | no | not_applicable
merge_permission: yes | no | not_applicable
```
