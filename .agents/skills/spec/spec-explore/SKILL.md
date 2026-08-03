---
name: spec-explore
description: Use when the prompt contains [SPEC.EXPLORE], when a large or uncertain request cannot yet be converted into decision-complete workstreams, or when repeated replanning indicates unresolved specification fog.
---

# [SPEC.EXPLORE]

Map uncertain spec territory until the destination, blocking questions and candidate durable outcomes are explicit enough for portfolio planning. Do not implement, authorise work or disguise unresolved decisions as plans.

## Role boundary

- Explore the destination, terms, constraints, decisions, dependencies and uncertainty.
- Distinguish settled context, answerable questions, evidence-blocked questions and fog.
- Do not create implementation plans, assign agents, change workstream state or choose the next portfolio item.
- Do not rewrite `AI_SPACE/SPEC.md` unless `[SPEC.EDIT_REQUIRED]` is present.
- Use `$prototype` only when one bounded disposable experiment is the cheapest reliable way to settle one explicit decision.

## Required inputs

- governing spec or explicit human authority;
- repository scope;
- known decisions and constraints;
- current findings, campaign map or repeated planning failures when available.

If the destination itself lacks decision-complete authority, return `BLOCKED` with the exact missing decision.

## Exploration model

Classify each relevant question as:

- `SETTLED`: authority or evidence already answers it;
- `ANSWERABLE_NOW`: repository inspection or bounded research can answer it;
- `EVIDENCE_BLOCKED`: the question is precise but needs a named observation, benchmark or prototype;
- `FOG`: the question itself cannot yet be stated precisely enough for implementation planning.

A candidate outcome is `COMMITTED` only when its mission, authority, dependencies and proof can be stated. Otherwise retain it as `PREPARED` or fog.

## Output

```yaml
spec_exploration_id: SE001
destination:
  authority: {exact spec section or human instruction}
  completion_claim: {observable terminal state}
settled_context:
  terms: []
  constraints: []
  decisions: []
decision_nodes:
  - id: D001
    question: {one precise question}
    status: SETTLED | ANSWERABLE_NOW | EVIDENCE_BLOCKED | FOG
    blocking: []
    evidence_needed: {inspection, benchmark, prototype or human decision}
    resolution_evidence: {what would settle it}
candidate_outcomes:
  - id: O001
    outcome: {one durable repository truth}
    horizon: COMMITTED | PREPARED
    depends_on: []
    spec_authority: {exact authority}
    acceptance_evidence: {what proves completion}
fog:
  - id: G001
    area: {uncertain territory}
    why_not_specifiable: {precise reason}
    clearing_action: {one bounded evidence action}
status: READY_FOR_PORTFOLIO | MORE_EXPLORATION_REQUIRED | BLOCKED
```

Do not include agent assignments or process-direction fields. The orchestrator owns promotion into `$plan-portfolio`.
