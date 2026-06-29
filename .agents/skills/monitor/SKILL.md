---
name: monitor
description: Use when the prompt contains [MONITOR], or when a running script, worker agent, validation job or GPU-heavy run needs progress/log/result monitoring, evaluation and possible intervention.
---

# [MONITOR]

A script, worker or validation job is running and will output logs/progress/results which you need to await -> evaluate -> maybe intervene -> await.

Rules:

- Spec alignment is first priority; do not drift away through iterations.
- Monitor validation gates and GPU-heavy jobs serially unless authorised otherwise.
- Intervene when the process is clearly failing, looping, drifting or producing invalid evidence.
- Record exact commands, outputs, run IDs and evidence paths.
- If repeated small failures occur, stop reactive patching and call `[DIAGNOSE]`.
