---
name: finding-verification
description: Verify one disputed, ambiguous or weakly evidenced conformance finding against the spec and repository. Return VERIFIED, REJECTED or BLOCKED.
---

# [VERIFY.FINDING]

Input: one proposed misalignment.

Check exact spec authority and exact repository evidence.

Return exactly:

- `VERIFIED`: the misalignment is real;
- `REJECTED`: the claim is not supported;
- `BLOCKED`: required evidence cannot be obtained safely.

Do not plan a fix, create a workstream, or choose future work.
