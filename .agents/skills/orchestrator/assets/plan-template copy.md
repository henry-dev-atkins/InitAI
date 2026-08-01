# Workstream Plan

## Identity and Traceability

- Workstream ID: WSXXX
- Plan ID: PXXX
- Source findings: FXXX
- Spec authority: {section/requirement}
- Owner agent: {agent}

## Work Classification

- Primary Work Type: `{WORK_TYPE}`
- Counts as capability progress: yes | no
- Supporting changes: {tests/config/docs/dependency/none}

## Mission

{one coherent outcome}

## Scope and Contracts

Write scope:
- `{path}`

Off-limits:
- `{path/pattern}`

Dependencies:
- `{WS ID-or-none}`

Contracts changed:
- `{interface/schema/config/output-or-none}`

Contracts consumed:
- `{interface/schema/config/output-or-none}`

## Protected Invariants / Must Not

- `{invariant}`
- Must not `{prohibited behaviour}`

## Command Manifest

```json
{
  "schema": "plan-command-manifest.v1",
  "commands": [
    {
      "id": "CMD001",
      "argv": ["python", "-m", "pytest", "tests/example.py", "--basetemp", "temp/pytest/WSXXX"],
      "cwd": ".",
      "purpose": "prove assigned behaviour",
      "phase": "final-validation",
      "expected_status": "pass",
      "evidence_target": "FXXX",
      "artefact_paths": [],
      "temp_root": "temp/pytest/WSXXX"
    }
  ]
}
```

## Implementation Steps

1. `{step}`

## Validation and Resolution Evidence

- `CMD001` proves `{spec requirement/finding}`

## Risks and Assumptions

- `{risk/assumption}`

## Result Packet Contract

Return `.agents/skills/orchestrator/assets/result-packet-template.md` fields and write an evidence ledger matching `evidence-ledger.schema.json`.

## Executive Summary

{short human-facing summary}

## Am I going in Circles?

{state whether the plan repeats prior failed work, adds reactive iterations, or can converge more directly}

## Is there a more elegant way of doing this?

{compare the chosen approach with simpler repository-fitting alternatives and explain why this is the minimal complete route}
