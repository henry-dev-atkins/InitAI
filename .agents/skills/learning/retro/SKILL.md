---
name: retro
description: Use when the prompt contains [RETRO], asks for a retrospective, asks whether the agents worked well across sessions, or asks to review process quality, progress rate, efficiency, validation cost, orchestration, handovers, parallelisation, worker behaviour, or AI_SPACE session history. This skill reviews how work was done, not whether the product/research result was good.
---

# [RETRO]

Run a retrospective on agent work quality using repo evidence. The purpose is to improve future worker behaviour, orchestration, planning, validation, and memory. Do not grade the product or research result except where product facts explain process quality.

## Ground Rules

- Treat `AI_SPACE/` as the source of truth for process evidence.
- Read before judging. Inspect session boards, locks, plans, task packets, result packets, TODOs, learnings, handovers, and relevant archive records.
- Separate "the work outcome" from "the way the work was conducted".
- Do not rewrite `AI_SPACE/SPEC.md` during a retro.
- Do not invent metrics. Mark a metric as unavailable when the evidence is absent.
- Do not use a failing or missing record as proof of bad work without checking nearby artefacts, commits, outputs, and result packets.
- Preserve secrets policy: do not copy secrets into retro reports.
- Use UK English.

## Role Boundary

  Retro agents are factual process reviewers, not managers of the next development loop.

  - Report evidence-backed process findings, impacts and rule/template improvements.
  - Do not choose the next implementation packet, tell the orchestrator what to run next, or convert findings into a development queue.
  - Do not include fields such as `next_step`, `recommended_next_action`, `recommended_plan`, or similar process-direction text.
  - If follow-up work exists, record it as a factual unresolved decision or TODO candidate. The orchestrator or human decides sequencing.

## Evidence Sources

Inspect the narrowest relevant time window first, then widen if needed:

- `AI_SPACE/sessions/session__*/session_board.md` for mission, constraints, dependency graph, work packages, status, evidence, GPU schedule, stop conditions, and global done gate.
- `AI_SPACE/sessions/session__*/locks.md` for file ownership, read/write scope, overlap, off-limits areas, and merge safety.
- `AI_SPACE/sessions/session__*/plan__*/plan.md` for work classification, assumptions, scope, validation gate, risks, and review requirements.
- `AI_SPACE/sessions/session__*/plan__*/task_packet.md` for delegation quality, worker authority, file scope, required checks, and expected result schema.
- `AI_SPACE/sessions/session__*/plan__*/result_packet.md` for actual changes, validation, failures, repairs, temporary files, spec review, and worker closure status.
- `AI_SPACE/TODO.md` for live unresolved work, stale carry-over, cleanup records, and whether retro findings already have tracked actions.
- `AI_SPACE/AI_LEARNINGS_LOG.md` for repeated mistakes, durable lessons, and whether prior lessons influenced later work.
- `AI_SPACE/handovers/` for resumability, exact commands, current state, and deferred work.
- `archive/` for moved historical records when live files reference them.
- Output roots and run metadata only when they are needed to understand validation effort, GPU usage, or repair loops.

## Work Classification

Classify the retro itself before writing durable output:

- Use `DOCS.MEMORY` when producing a durable retro report, TODO update, handover note, or learning update.
- Use `AGENT.WORKFLOW` when editing skills, agent instructions, templates, or orchestration rules.
- Use `TEMPORARY.DIAGNOSTIC` for scratch analysis that will not be committed and must be removed or archived.
- Use a separate plan if the retro discovers implementation, validation, cleanup, or spec-edit work that should be performed later.

## Retrospective Questions

Analyse these dimensions when evidence exists:

- Goal continuity: did the session keep serving the human's underlying goal, or drift into process, metadata, validation, or cleanup work?
- Spec discipline: were spec conflicts raised early and loudly, or found late through avoidable failures?
- Work classification: did each plan use one correct Primary Work Type, and did capability work avoid closing as docs-only, evidence-only, workaround, or cleanup work?
- Planning quality: were assumptions explicit, testable, and later checked? Which assumptions failed, and should they have been discovered earlier?
- Minimalism: did plans choose the smallest coherent change, or combine separable durable purposes?
- Dependency sequencing: were blockers, prerequisites, and merge order handled before dependent work started?
- Delegation quality: did task packets give enough authority, scope, validation, and off-limits detail for a worker to succeed without guessing?
- Parallelisation quality: were independent investigations or implementation slices run in parallel, while GPU-heavy and overlapping file work stayed serial?
- File ownership: did locks prevent overlap, stale ownership, off-scope edits, and merge conflict risk?
- Validation efficiency: did agents use focused checks first, forecasts before expensive runs, and real runs at closure when required?
- Failure response: did failures produce narrowed diagnosis and repair, or repeated small reactive changes?
- Repair scope control: did fixes stay within the original work packet, or did failures cause broad unplanned edits?
- GPU/resource discipline: were one-GPU constraints, profiler costs, disk gates, and runtime budgets respected?
- Throughput: how many plans reached `MERGED` or `[DONE]`, how much was capability work versus support work, and how long did validation gates take?
- Evidence quality: were result packets complete, with exact commands, pass/fail results, artefact roots, temporary-file status, and spec review where needed?
- Handover quality: could a fresh agent resume without rediscovering state or repeating old mistakes?
- Memory quality: did real lessons enter `AI_LEARNINGS_LOG.md`, and did TODOs stay live-only rather than historical clutter?
- Communication quality: did user-facing updates convey risk, progress, decisions, and blockers without excessive narration?

## Useful Metrics

Report counts and rates only when they can be derived from records:

- sessions reviewed
- plans opened, completed, merged, blocked, rejected, or still running
- plans by Primary Work Type
- worker agents used, and workers per plan
- read-only versus write-capable work packages
- parallel plans versus serial plans
- validation commands per plan
- failed validation attempts before final pass
- GPU-heavy runs and total reported wall time
- forecast/preflight runs before expensive validation
- assumptions contradicted by later evidence
- task packets missing owner, scope, validation, or result schema
- result packets missing changed files, validation, spec review, temporary-file status, or blocker detail
- lock overlaps, stale locks, or scope changes
- TODOs opened, closed, deferred, or left stale
- learnings added for repeated mistakes

## Report Shape

Use this structure unless the user asks for a different output:

1. `[RETRO] Work Classification`
2. `Evidence Reviewed`
3. `Process Summary`
4. `What Worked Well Operationally`
5. `Friction / Inefficiency`
6. `Parallelisation Review`
7. `Validation And Resource Review`
8. `Planning And Delegation Review`
9. `Memory, TODO, And Handover Review`
10. `Actionable Improvements`
11. `Open Questions / Missing Evidence`

Keep each finding evidence-backed. Prefer references to session IDs, plan IDs, commands, result packets, and artefact roots over broad judgements.

## Finding Format

For each material finding, include:

- evidence: exact session, plan, packet, command, status, or artefact root;
- process interpretation: what this says about how the agents worked;
- impact on future work: time, risk, repeated effort, validation cost, user clarity, or parallelisation quality;
- improvement: one concrete behaviour change, rule, template change, metric, or follow-up plan.

## Anti-Patterns To Flag

- "Good outcome" used to excuse weak process evidence.
- Broad taxonomy or discussion when the next action should have been diagnosis or repair.
- Repeated validation failures without narrowing the failure contract.
- Workers claiming `[DONE]` while required validation, result packets, spec review, or cleanup is missing.
- Main-thread serial implementation when independent work packages could have been delegated.
- Parallel GPU/profiler runs that compete for the single local GPU.
- Write-capable agents with vague file scope or overlapping ownership.
- Support work counted as capability progress.
- Handover or TODO text that preserves history but does not make the next action clear.
- Learning-log entries that describe an event but do not change future behaviour.

## Closure

End with the smallest useful set of process improvements. If the retro creates new durable TODOs, learnings, skill changes, or session notes, state exactly what changed and where. If it is read-only, state that no files were changed.
