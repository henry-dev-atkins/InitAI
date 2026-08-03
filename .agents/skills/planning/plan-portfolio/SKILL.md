---
name: plan-portfolio
description: Use when the prompt contains [PLAN.PORTFOLIO], after finding verification/spec exploration, or when open findings must be grouped into several large independent durable outcomes before individual planning.
---

# [PLAN.PORTFOLIO]

Construct the portfolio of durable outcomes required to converge on the spec. Preserve several independent large steps instead of splitting one local issue merely to fill agent capacity.

## Role boundary

- Transform verified findings, committed exploration outcomes and current campaign state into coherent workstreams.
- Do not write individual implementation plans, assign agents, start work or change authoritative workstream state.
- Findings explain why work exists; outcomes define what the work is.
- Split only genuinely independent durable outcomes. Required tests, config changes and behaviour documentation may remain supporting changes within the capability workstream.

## Required inputs

- current verified finding register;
- exact spec authority;
- current campaign map and accepted dependencies when present;
- active workstreams and contracts;
- repository revision.

## Construction tests

Every candidate workstream must:

- establish one durable repository truth;
- be independently valuable and reviewable;
- consume a coherent set of findings or one committed outcome;
- state exact authority, dependencies, contracts and acceptance evidence;
- avoid likely invalidation by unresolved higher-level work;
- be large enough to preserve the spec-level outcome but bounded enough for one controlled implementation attempt.

Reject portfolio shapes that:

- collapse several independent capabilities into one workstream;
- split one local concern across multiple workers merely for utilisation;
- allocate all capacity to support work while major capability outcomes remain available;
- mirror reviewer report boundaries instead of durable repository outcomes;
- rely only on disjoint files while semantic contracts still conflict.

## Output

```yaml
portfolio_plan_id: PP001
repo_revision: {commit-or-tree-hash}
destination: {observable campaign completion claim}
candidate_workstreams:
  - proposed_id: WS-CANDIDATE-001
    outcome: {one durable repository truth}
    source_findings: [F001]
    source_outcomes: [O001]
    spec_authority: []
    primary_work_type: {one ontology value}
    horizon: COMMITTED | PREPARED
    priority:
      spec_impact: 1-5
      critical_path: 1-5
      unlock_value: 1-5
      uncertainty_reduction: 1-5
      conflict_risk: 1-5
      staleness_risk: 1-5
    dependencies: []
    write_scope: []
    contracts_changed: []
    contracts_consumed: []
    acceptance_evidence: []
    rationale: {why this is one coherent outcome}
coverage:
  covered_findings: []
  deferred_findings:
    - finding_id: FXXX
      reason: {dependency, fog, superseded or support-only}
anti_collapse_review:
  independent_major_outcomes_preserved: true | false
  arbitrary_fragmentation_detected: true | false
  support_only_churn_detected: true | false
status: PASS | FAIL | BLOCKED
```

The orchestrator assigns stable workstream IDs and records accepted candidates in the workstream register.
