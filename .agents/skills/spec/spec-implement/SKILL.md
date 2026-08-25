---
name: spec-implement
description: Convenience entry point for implementing the current spec. For substantial work, delegate to the simplified $orchestrator loop; for one already-bounded change, use normal plan -> review -> implementation.
---

# [SPEC.IMPLEMENT]

If the repository may contain several spec misalignments, use `$orchestrator`.

If the user supplied one bounded implementation outcome, create one `$plan`, obtain plan review, implement it, review the result, then run `$spec-review` over the affected spec scope.

Do not invent a separate implementation workflow.
