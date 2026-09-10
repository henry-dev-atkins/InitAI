---
name: bulk-read
description: Summarise a large, non-authority repository read into cited evidence when the exact question and allowed paths are known.
---

# Bulk read

Use this optional read-only route when a large file read would add raw context cost.

Before reading, record the exact question, allowed paths, known terms, evidence needed, and stop condition.

Read at most 200 lines per chunk. Search known terms first. Preserve file paths and line references.

Return the `BULK_READ` handoff with `status`, `answer`, `evidence`, `uncertainty`, and `follow_up` fields.

Do not make judgements for the parent task. Do not decide authority. Do not edit files. Do not spawn agents. Do not create a workflow stage.
