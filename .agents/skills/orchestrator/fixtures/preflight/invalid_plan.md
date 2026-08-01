# Workstream Plan

## Identity and Traceability

- Workstream ID: WS001
- Plan ID: P002
- Source findings: F001
- Spec authority: AGENTS.md workflow rules
- Owner agent: planner

## Work Classification

- Primary Work Type: `AGENT.WORKFLOW`

## Mission

Invalid command shape.

## Scope and Contracts

Write scope:
- `{missing-path}`

Off-limits:
- `src`

Dependencies:
- none

Contracts changed:
- none

Contracts consumed:
- none

## Protected Invariants / Must Not

- Keep product code untouched.

## Command Manifest

```json
{
  "schema": "plan-command-manifest.v1",
  "commands": [
    {
      "id": "CMD001",
      "argv": ["python", "-m", "pytest", "tests"],
      "cwd": ".",
      "purpose": "invalid pytest command",
      "phase": "final-validation",
      "expected_status": "pass",
      "evidence_target": "F001"
    },
    {
      "id": "CMD001",
      "argv": ["python", "-c", "if True print('bad')"],
      "cwd": ".",
      "purpose": "invalid inline Python",
      "phase": "diagnostic",
      "expected_status": "pass",
      "evidence_target": "F001",
      "temp_root": ".ruff_cache"
    }
  ]
}
```

## Implementation Steps

1. Invalid step.

## Validation and Resolution Evidence

- `CMD001` is intentionally invalid.

## Risks and Assumptions

- This fixture must fail.

## Result Packet Contract

Return failure evidence.

## Executive Summary

Invalid fixture.

## Am I going in Circles?

No.

## Is there a more elegant way of doing this?

No.
