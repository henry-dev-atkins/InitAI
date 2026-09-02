---
name: outcome-decomposition
description: Split independent durable outcomes, not files or incidental implementation steps. Collate the current conformance findings into coherent independent durable workstreams. Output the workstream list only; do not plan implementation details.
---

# [PLAN.PORTFOLIO] / outcome-decomposition

Input: the current misalignment list from `$conformance`.

Output: a list of workstreams.

Split only genuinely independent durable outcomes. Required tests, config changes and behaviour documentation may remain supporting changes within the capability workstream.

Each workstream contains:

- `Workstream ID`;
- `Title`;
- `Outcome`;
- `Finding IDs`;
- `Spec authority`;
- `Rough affected area`;
- `Dependencies`, only when real;
- `Status`: `OPEN`, `BLOCKED`, or `ACCEPTED`.

Rules:

- Every current misalignment belongs to one active workstream unless a real dependency requires otherwise.
- Do not split by file when one durable outcome spans several files.
- Do not create support-only workstreams when the support change is required by the same outcome.
- Do not plan code here.
- Do not create a second requirements system around the spec.
