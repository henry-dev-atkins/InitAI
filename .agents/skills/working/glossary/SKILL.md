---
name: glossary
description: Resolve repository workflow, agent and skill terms using the accepted project vocabulary.
---

# Glossary

Use this skill when a workflow, agent, plan or skill term is unclear.
Use the term defined here in plans, reviews and handovers.
The active `AGENTS.md` and project specification remain authoritative.

## Skills

- A skill is a directory that contains a `SKILL.md` file.
- `SKILL.md` contains frontmatter and procedural instructions.
- A skill may contain scripts or reference files when they directly support its instructions.
- Skill metadata should stay short. Load detailed instructions when the skill is used.
- A skill is not an agent. A skill provides knowledge or procedure. An agent provides a role and execution behaviour.

## Agents

- An agent role is the named configuration in `.codex/agents/`.
- An agent instance is one running copy of an agent role.
- The orchestrator assigns work to an agent instance through the checked workflow.
- A write-capable agent edits only its accepted write scope.
- A read-only agent inspects and reports without editing repository files.

## Workflows and authority

- Standalone work follows an explicit human prompt.
- Orchestration follows `AI_SPACE/SPEC.md` when that file exists.
- A source authority states which requirement controls the work.
- A finding records one material difference between the authority and the repository.
- A workstream groups findings into one independent durable outcome.
- A dependency states which workstream must complete first.
- A resource identifies a shared item that must be serialised, such as a checkout or GPU.
- A contract is a public interface, schema, config rule or behaviour that callers rely on.
- A terminal condition is the evidence required before the work is complete.

## Workflow actions

Capitalised bracket keywords are human-facing actions.
Lowercase hyphenated names refer to folders under `.agents/skills/`.

- `[SESSION.START]` -> `$session-start`
- `[SESSION.CLEAN]` -> `$session-clean`
- `[SESSION.COMPACT]` -> `$session-compact`
- `[SESSION.END]` -> `$session-end`
- `[PROGRESS.REPORT]` -> `$progress-report`
- `[PLAN]` -> `$plan`
- `[PLAN.PORTFOLIO]` -> `$outcome-decomposition`
- `[PORTFOLIO.NEXT]` -> `$select-ready-work`
- `[PLAN.BLASTRADIUS]` -> `$change-impact-analysis`
- `[PLAN.PREFLIGHT]` -> `$plan-preflight`
- `[PLAN.PARALLEL_SAFETY]` -> `$parallel-safety`
- `[PLAN.REVIEW]` or `[PLAN_REVIEW]` -> `$plan-review`
- `[PLAN.SUB]` or `[SUBPLAN]` -> `$plan-sub`
- `[PLAN.TERMINAL_CONDITION]` or `[TERMINAL_CONDITION]` -> `$conformance`
- `[LEARN]` -> `$learn`
- `[DIAGNOSE]` -> `$diagnose`
- `[SPEC.EXPLORE]` -> `$requirements-discovery`
- `[VERIFY.FINDING]` -> `$finding-verification`
- `[SPEC.REVIEW]` or `[SPEC_REVIEW]` -> `$conformance`
- `[SPEC.IMPLEMENT]` or `[SPEC_IMPLEMENT]` -> the project-scoped `orchestrator` agent
- `[SPEC.EDIT_REQUIRED]` or `[SPEC EDIT REQUIRED]` -> `$spec-edit`
- `[WORK_TYPE]` or `[WORKFLOW_ONTOLOGY]` -> `$workflow-ontology`
- `[WORKFLOW_STRUCTURE]` -> `$workflow-structure`
- `[DONE]` or `[BLOCKED]` -> `$done`
- `[STRATEGY.REVIEW]` -> `$strategy-review`
- `[TEAM]`, `[agentic]` or `[ORCHESTRATOR]` -> the project-scoped `orchestrator` agent

## Work types

- `CAPABILITY.RESEARCH`: spec-backed durable research behaviour.
- `CAPABILITY.PRODUCT`: spec-backed durable product or user behaviour.
- `EVIDENCE.VALIDATION`: durable reusable validation evidence.
- `FIX.ALIGNMENT`: durable root-cause correction to match the spec.
- `DEPENDENCY.LOCAL`: portable local or repository infrastructure required by implementation.
- `TEMPORARY.DIAGNOSTIC`: scratch probing or logging that is never committed.
- `ENVIRONMENT.ADAPTATION`: isolated local or platform adaptation.
- `WORKAROUND.QUARANTINED`: explicit temporary workaround that is never capability progress.
- `FLUFF.DISPOSABLE`: one-off plots, dumps, screenshots or exploratory artefacts.
- `DOCS.MEMORY`: TODOs, learnings, handovers and durable documentation.
- `AGENT.WORKFLOW`: agent instructions, skills, rules and templates.
- `CLEANUP.HYGIENE`: organisation without behaviour change.
- `SPEC.EDIT`: spec change with explicit spec-edit authority.

Workflow classes are `SMALL`, `STANDARD` and `CAMPAIGN`.
They control planning depth. They do not lower the terminal correctness standard.

## Plans and reviews

- A plan fixes the authorised outcome, scope, contracts, validation and protected invariants.
- A plan preflight checks mechanical completeness before semantic review.
- A plan review independently returns `ACCEPT`, `REJECT` or `BLOCKED`.
- Implementation reports changed files and validation evidence within the accepted scope.
- Implementation review checks the change against the accepted plan.
- Conformance compares the active authority with the repository.
- `PASS` with an empty findings list is the clean conformance result.
- `BLOCKED` names the external condition that prevents safe progress.

## Scope and evidence

- Write scope lists the paths an agent may edit.
- Read scope lists the stable paths an agent may inspect.
- Off-limits scope lists paths that the agent must not edit.
- Validation evidence is the recorded output that proves a required behaviour or invariant.
- A validation ledger records command results when the workflow requires one.

## AI workspace

- `AI_SPACE/SPEC.md` is the default project authority for orchestration.
- `AI_SPACE/sessions/` stores current workflow state and evidence.
- `AI_SPACE/handovers/` stores resumable end-of-session context.
- `AI_SPACE/AI_LEARNINGS_LOG.md` stores durable lessons.
- `AI_SPACE/TODO.md` stores concrete unresolved work.
- `AI_SPACE/archive/` stores retired control-plane material.
- `AI_SPACE/tools/` stores repository control-plane helper tools.

