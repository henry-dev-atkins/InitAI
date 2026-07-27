---
name: final-report
description: Use before [DONE] or [BLOCKED] reports, especially for orchestrated spec implementation.
---

# [DONE] / [BLOCKED]

## `[DONE]` requires

- requested behaviour exists in repository state, not only plans/reports;
- relevant validation passed and exact commands/results are reported;
- spec alignment is evidenced;
- no in-scope finding remains open;
- no workstream is active, awaiting review, rejected or blocked;
- temporary diagnostics, fluff and unapproved workarounds are absent;
- Work Type and commit policies were followed.

For orchestrated spec implementation, `[DONE]` additionally requires `$terminal-condition`: six independent spec reviewers pass the same frozen repository revision and the tree remains unchanged during review.

Worker `[DONE]` means only that the worker task packet completed.

## `[BLOCKED]` requires

Use `[BLOCKED]` only after a concrete path fails for a reason outside current authority, available tooling/data or safe operating limits.

Report:

- exact unavailable command/check/capability;
- exact blocker evidence;
- concrete attempts already made;
- files changed;
- affected workstream/finding states;
- smallest human decision or external action required.

Do not report `[DONE]` when validation failed, was skipped by choice, findings remain, or required behaviour is absent.
