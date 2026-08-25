---
name: terminal-condition
description: Optional explicit completion check. In the simplified orchestrator this is equivalent to a fresh exhaustive spec review that returns no material misalignments.
---

# [TERMINAL_CONDITION]

The normal orchestrator loop does not need a separate terminal machinery phase.

Run a fresh `$spec-review` against the current repository.

Return:

- `PASS` only when the misalignment list is empty;
- `FAIL` with the returned misalignments otherwise.

The spec is the completion authority. Old workstream status does not prove completion.
