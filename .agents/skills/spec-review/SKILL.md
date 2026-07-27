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

## Role boundary

  Spec-review agents are factual reviewers, not process managers.

  - Compare the named scope against the spec and report pass/fail evidence.
  - Rank findings only by stated review criteria and cited evidence.
  - Do not suggest next steps, propose repair packets, choose future work, or tell the orchestrator what to do after the review.
  - Do not include fields such as `next_step`, `recommended_next_action`, `recommended_plan`, or similar process-direction text.
  - `merge_permission` and `capability_progress_supported` are review gates only. They are not instructions to merge, commit, spawn, defer, split or continue.
  - The orchestrator owns sequencing, portfolio decisions, commits, deferrals, splits and stop/pivot decisions.

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

For planning reviews, order `blocking_findings` and `core_behaviour_gaps` by convergence impact and include the required finding fields. The order is part of the review result and must be preserved by orchestration unless a permitted dependency exception is evidenced. The order is evidence for the orchestrator; it is not an instruction.