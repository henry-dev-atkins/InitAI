---
name: diagnose
description: Use when the prompt contains [DIAGNOSE], or when the user asks for the underlying cause of a symptom, failed run, failed test, regression, repeated repair failure, unexpected GPU/CPU/device behaviour, or spec misalignment.
---

# [DIAGNOSE]

No permanent changes yet unless the human explicitly authorises a fix.

Find the underlying cause of the symptom.

Rules:

- No band-aid, hacky or workaround fixes.
- You may use agents for diagnostic experiments.
- Use temporary diagnostics under `temp/` and archive/remove them before closure.
- We are experimentally driven, not speculative.
- Consider high level, medium level and low level causes.
- Output may be diagnosis-only, but must not be reported as a fix or closure.
- If diagnosis identifies durable work, classify it with `[WORK_TYPE]` before implementation.

Output a report card with hypotheses, methodologies, possible missed factors, detailed causes and evidence.

You may call `[DIAGNOSE]` at any point in terminal-condition loops.


## Role boundary

  Diagnostic agents are factual investigators, not process managers.

  - Report hypotheses, methods, evidence, causes and uncertainty.
  - Do not suggest next steps, assign future work, repair, or tell the orchestrator what to do after the diagnosis.
  - If durable work is implied by the diagnosis, state the work type and evidence boundary only. The orchestrator decides whether to plan, commit, split, defer or block.
  - Do not include fields such as `next_step`, `recommended_next_action`, `recommended_plan`, or similar process-direction text.