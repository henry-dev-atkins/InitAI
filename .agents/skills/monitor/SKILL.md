---
name: monitor
description: Use when the prompt contains [MONITOR], or when a running script needs log/progress/result monitoring, evaluation, and possible intervention.
---

# [MONITOR]

A script is running and will output logs/progress/results which you need to await -> evaluate -> maybe intervene -> await -> ...
- Spec alignment is first priority, do not drift away through iterations.
- Generally this is needed when the script is 'right' but just needs debugging/diagnosing etc.
