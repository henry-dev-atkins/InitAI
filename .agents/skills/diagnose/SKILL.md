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
