---
name: verify-finding
description: Use when the prompt contains [VERIFY.FINDING], or before promoting a reported or suspected discrepancy into an implementation workstream.
---

# [VERIFY.FINDING]

Determine whether one reported discrepancy is real, reproducible and sufficiently evidenced. Do not design or schedule the repair.

## Role boundary

- Compare the claim with exact spec authority and repository reality.
- Reproduce behaviour where practical and safe.
- Distinguish the claimed symptom, verified discrepancy and underlying uncertainty.
- Do not edit durable repository files, plan fixes, create workstreams, assign agents or recommend future work.
- Temporary diagnostic output must stay under repo-local `temp/` and be removed or archived before reporting.

## Required inputs

- source finding/report ID;
- exact claim;
- spec authority or expected behaviour;
- affected scope;
- any original evidence or reproduction steps.

## Outcomes

- `VERIFIED`: direct evidence proves the discrepancy.
- `NOT_REPRODUCED`: the stated procedure does not reproduce it; include exact evidence and limitations.
- `INSUFFICIENT_EVIDENCE`: the claim is plausible but cannot be established safely with available authority, tooling or data.
- `SUPERSEDED`: current repository state or stronger evidence makes the claim obsolete or duplicates another verified finding.
- `BLOCKED`: a genuine external blocker prevents verification.

## Output

```yaml
finding_verification_id: FV001
source_finding_id: {report-local or stable ID}
repo_revision: {commit-or-tree-hash}
spec_authority: {exact section/requirement}
claim: {reported discrepancy}
method:
  - {inspection or command}
observations:
  - {path:line, command result or reproducible behaviour}
status: VERIFIED | NOT_REPRODUCED | INSUFFICIENT_EVIDENCE | SUPERSEDED | BLOCKED
verified_discrepancy: {expected versus actual, or null}
affected_scope:
  files: []
  behaviour: {concise description}
resolution_evidence: {what would prove alignment if VERIFIED}
uncertainty: {remaining evidence limits}
```

Only `VERIFIED` findings are implementation-ready. The orchestrator owns stable IDs, deduplication, promotion and state changes.
