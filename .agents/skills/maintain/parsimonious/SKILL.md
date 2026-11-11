---
name: parsimonious
description: Review a caller-supplied plan, diff, file, test scope, repository area, or wider scope for unnecessary cost and unjustified complexity while preserving the requested outcome.
---

# Parsimonious

Review exactly the scope supplied by the caller. The scope may be a plan, diff, file, test scope, repository area, or wider repository scope. 
Treat that scope as the review boundary. 
Expand only into directly connected dependencies when their evidence is needed to judge the scoped element. 
Review a wider area only when the caller explicitly asks for it.

This is a report-only review.
Do not edit files, create workstreams, assign work, choose future work, or create workflow phases.
Optional skills do not create workflow stages. Do not claim capability progress for this review.

Review plans before implementation when a plan is supplied. 
When an accepted plan is supplied, compare the diff with that plan.
Review tests only when tests are inside the supplied scope. 
Review every active artefact type in scope, including code, files, dependencies, abstractions, steps, fields, tests, configuration, documentation, fixtures, workflows, and behaviour.

## Review questions

For each scoped element:

- What requirement, invariant, or user outcome does it serve?
- Is the supporting work minimal and directly necessary?
- Does the requirement itself impose unnecessary scope or cost? Label this as a requirement concern, separately from implementation findings.
- Is duplication justified by isolation, readability, or independent validation? Flag it only when none of those benefits has evidence.
- Would removing or simplifying it preserve the requested outcome and relevant invariants?

Assess only cost supported by evidence. Use one or more of these cost types:

- concept count
- cognitive load
- future change cost
- failure surface
- maintenance burden
- operational risk
- permission surface
- startup cost
- dependency lock-in
- migration burden
- user friction
- proof burden
- requirement scope

## Verdicts

Use exactly one verdict:

- `PARSIMONIOUS` means no meaningful unjustified cost was found.
- `NEEDS_TIGHTENING` means a local simplification preserves the required outcome.
- `WASTEFUL` means excess cost materially obscures, delays, weakens, or outweighs the requested capability.

Use `NEEDS_INVESTIGATION` confidence when evidence is insufficient for a rejection.
Every finding still needs an exact element, traceability, evidence, concrete cost, confidence, and the smallest preserving simplification.

## Output

Return exactly this structure. 
Rank findings from highest material cost to lowest.
 Report `none` under Core Capability Impact when there is no impact.

```text
Verdict: PARSIMONIOUS | NEEDS_TIGHTENING | WASTEFUL

Findings
- rank: 1
  severity: HIGH | MEDIUM | LOW
  confidence: CONFIRMED | PROBABLE | NEEDS_INVESTIGATION
  cost_type: <one or more allowed cost types>
  element: <exact file, symbol, step, field, dependency, test, or behaviour>
  requirement_or_invariant: <what it is meant to serve>
  evidence: <scope evidence>
  cost: <concrete cost>
  smallest_preserving_simplification: <smaller end state>

Core Capability Impact
- <impact or none>
```

Do not invent findings, costs, or evidence. A clean result reports no findings and does not list every element that passed.
