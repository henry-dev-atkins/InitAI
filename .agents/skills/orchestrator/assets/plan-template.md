# Workstream Plan

## Identity and Traceability

- Workstream ID: WSXXX
- Plan ID: PXXX
- Predecessor plan: none
- Failed assumption from predecessor: none
- Material causal delta: none
- Source findings: FXXX
- Requirement IDs: REQXXX
- Spec authority: {section/requirement}
- Owner agent: {agent}
- Workflow class: SMALL | STANDARD | CAMPAIGN

## Work Classification

- Primary Work Type: `{WORK_TYPE}`
- Counts as capability progress: yes | no
- Supporting changes: {tests/config/docs/dependency/none}

## Mission

{one coherent outcome}

## Scope and Contracts

Write scope:
- `{exact repo-relative file or directory root}`

Stable read assumptions:
- `{exact repo-relative file or directory root-or-none}`

Off-limits:
- `{exact repo-relative file or directory root}`

Dependencies:
- `{WS ID-or-none}`

Contracts changed:
- `{CON ID-or-none}`

Contracts consumed:
- `{CON ID-or-none}`

Mutable resources:
- `{stable resource ID-or-none}`

## Protected Invariants / Must Not

- `{invariant}`
- Must not `{prohibited behaviour}`

## Command Manifest

- Path: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/plan_command_manifest.json`
- SHA-256: `{manifest-sha256}`

The manifest is the only command source of truth. It uses `plan-command-manifest.v1`, repeats this workstream and plan ID, uses argv arrays only, and gives every command a timeout from 1 to 300 seconds.

## Implementation Steps

1. `{step}`

## Validation and Resolution Evidence

| Command ID | Requirement IDs | Finding IDs | Proof |
|---|---|---|---|
| CMD001 | REQXXX | FXXX | `{behaviour or requirement proved}` |

## Risks and Assumptions

- `{risk/assumption}`

## Result Packet Contract

Return `.agents/skills/orchestrator/assets/result-packet-template.md` fields. Run the reviewed manifest through `run_command_manifest.py`. Return the generated validation ledger path. Do not write execution claims into the evidence ledger manually.

## Executive Summary

{short human-facing summary}

## Am I going in Circles?

{state whether the plan repeats prior failed work, adds reactive iterations, or can converge more directly}

## Is there a more elegant way of doing this?

{compare the chosen approach with simpler repository-fitting alternatives and explain why this is the minimal complete route}
