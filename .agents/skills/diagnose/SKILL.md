---
name: diagnose
description: Use when the prompt contains [DIAGNOSE], or when the user asks for the underlying cause of a symptom, failed run, failed test, regression, unexpected GPU/CPU/device behaviour, or spec misalignment.
---

# [DIAGNOSE]
No permanent changes yet.
What is the underlying cause of this symptom?
    - No band-aid, hacky or workaround fixes
    - You may use agents for diagnostic experiments
    - We are experimentally driven, not speculative
    - Agentically consider high level (philosophy, underlying math, etc), medium level (integration, usage, etc) and low level (bugs, syntax, etc).
    - Output may be diagnosis-only, but must not be reported as a fix or closure.

Output a report card with hypotheses, methodologies, possible missed factors, detailed causes, and evidence.
You may call on [DIAGNOSE] at any point.
