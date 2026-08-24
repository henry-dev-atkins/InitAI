# Workstream Plan

## Identity and Traceability

- Workstream ID: WS001
- Plan ID: P002
- Predecessor plan: none
- Failed assumption from predecessor: none
- Material causal delta: none
- Source findings: F001
- Requirement IDs: REQ001
- Spec authority: AGENTS.md workflow rules
- Owner agent: planner
- Workflow class: STANDARD

## Work Classification

- Primary Work Type: `AGENT.WORKFLOW`
- Counts as capability progress: no
- Supporting changes: validation fixtures

## Mission

Add a workflow validator fixture.

## Scope and Contracts

Write scope:
- `src/../../outside`

Stable read assumptions:
- `.agents/skills/orchestrator/assets`

Off-limits:
- `AI_SPACE/SPEC.md`

Dependencies:
- none

Contracts changed:
- `CON001`

Contracts consumed:
- none

Mutable resources:
- none

## Protected Invariants / Must Not

- Keep product code untouched.
- Must not edit AI_SPACE/SPEC.md.

## Command Manifest

- Path: `.agents/skills/orchestrator/fixtures/preflight/invalid_manifest.json`
- SHA-256: `5d2718e7d63a0cde32fb1a70dbb2df833ad7f148f5c0e8c80c27189c030b815c`

The manifest is the only command source of truth.

## Implementation Steps

1. Create the fixture.

## Validation and Resolution Evidence

| Command ID | Requirement IDs | Finding IDs | Proof |
|---|---|---|---|
| CMD001 | REQ999 | F001 | Invalid evidence binding. |

## Risks and Assumptions

- The fixture is workflow-only.

## Result Packet Contract

Return the result packet and trusted evidence ledger.

## Executive Summary

Workflow fixture for preflight validation.

## Am I going in Circles?

No repeated repair loop is present.

## Is there a more elegant way of doing this?

A single small fixture is the simplest route.
