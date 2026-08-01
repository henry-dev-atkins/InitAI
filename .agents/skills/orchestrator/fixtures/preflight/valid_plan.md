# Workstream Plan

## Identity and Traceability

- Workstream ID: WS001
- Plan ID: P001
- Source findings: F001
- Spec authority: AGENTS.md workflow rules
- Owner agent: planner

## Work Classification

- Primary Work Type: `AGENT.WORKFLOW`
- Counts as capability progress: no
- Supporting changes: validation fixtures

## Mission

Add a workflow validator fixture.

## Scope and Contracts

Write scope:
- `agents/skills/orchestrator/fixtures`

Off-limits:
- `src`

Dependencies:
- none

Contracts changed:
- `plan-command-manifest.v1`

Contracts consumed:
- none

## Protected Invariants / Must Not

- Keep product code untouched.
- Must not edit AI_SPACE/SPEC.md.

## Command Manifest

```json
{
  "schema": "plan-command-manifest.v1",
  "commands": [
    {
      "id": "CMD001",
      "argv": [
        "python",
        "-m",
        "pytest",
        "agents/skills/orchestrator/fixtures",
        "--basetemp",
        "temp/pytest/WS001"
      ],
      "cwd": ".",
      "purpose": "prove workflow fixture validation",
      "phase": "final-validation",
      "expected_status": "pass",
      "evidence_target": "F001",
      "artefact_paths": [],
      "temp_root": "temp/pytest/WS001",
      "requires_existing_paths": [
        "agents/skills/orchestrator/assets/plan-template.md"
      ]
    },
    {
      "id": "CMD002",
      "argv": [
        "python",
        "-c",
        "print('ok')"
      ],
      "cwd": ".",
      "purpose": "compile inline Python probe",
      "phase": "diagnostic",
      "expected_status": "pass",
      "evidence_target": "F001",
      "artefact_paths": [],
      "temp_root": "temp/python/WS001"
    }
  ]
}
```

## Implementation Steps

1. Create the fixture.

## Validation and Resolution Evidence

- `CMD001` proves F001.
- `CMD002` proves inline Python command syntax.

## Risks and Assumptions

- The fixture is workflow-only.

## Result Packet Contract

Return the result packet and evidence ledger.

## Executive Summary

Workflow fixture for preflight validation.

## Am I going in Circles?

No repeated repair loop is present.

## Is there a more elegant way of doing this?

A single small fixture is the simplest route.
