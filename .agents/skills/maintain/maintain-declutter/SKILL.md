---
name: maintain-declutter
description: Report-only repo declutter and commit-worthiness audit. Use when Codex is asked to review repo files for clutter, permanence, archive recommendations, move recommendations, commit candidates, untracked files, "should this be committed?", "what should be archived?", or file cleanup decisions without changing files.
---

# Maintain Declutter

Perform a non-mutating repo declutter audit. Inspect tracked and untracked files, classify relevant files, and report what should be committed, kept uncommitted, archived, moved, ignored as temporary, or decided by a human.

Do not move, delete, stage, commit, format, rewrite, or generate cleanup artefacts unless the user separately asks for that action after the report.

## Use inside the simple loop

When a plan or implementation reviewer invokes this skill, return only the bounded review findings and evidence. The parent reviewer owns `ACCEPT` / `REJECT` or the implementation verdict. Do not create workstreams, workflow stages, or future-work decisions.
- the parent `plan-review` or implementation reviewer owns the final verdict and the orchestrator owns all subsequent action.

## Scope

- Work from inside the current repo.
- Check `AI_SPACE/SPEC.md` if present. If absent, do not infer project intent; limit conclusions to repo hygiene and explicit repo-maintenance evidence.
- Inspect `git status --short`, tracked files, untracked files, and relevant directories.
- Exclude `.git/`.
- Avoid dependency folders, cache churn, virtual environments, generated build trees, large datasets, checkpoints, and machine-local state unless the user explicitly asks to include them.
- Preserve current uncommitted user work. Call it out separately when it appears related to active work.
- Do not expose secrets. If a file may contain secrets, say that it needs human review without quoting secret-like content.

## Output

Use exactly these labels for file decisions:

- `COMMIT`: Durable repo change that appears intentional, scoped, and worth staging.
- `KEEP_UNCOMMITTED`: Valid local or active work that should remain outside a commit for now.
- `ARCHIVE_RECOMMENDED`: Old, noisy, superseded, or completed material that should be moved under `archive/` or an existing repo archive location if present.
- `MOVE_RECOMMENDED`: Useful file in the wrong repo location; propose a specific repo location.
- `IGNORE_OR_TEMP`: Cache, generated output, local-only state, or temporary diagnostic material that should not be committed.
- `NEEDS_HUMAN_DECISION`: Ambiguous, risky, secret-adjacent, large, ownership-sensitive, or intent-unclear material.

For every relevant file or coherent file group, include the reason and confidence: `high`, `medium`, or `low`.

```text
Declutter Verdict: CLEAN | ACTIONS_RECOMMENDED | BLOCKED

Commit Candidates
- path: reason; confidence: high|medium|low

Archive Recommended
- path: reason; confidence: high|medium|low

Keep Uncommitted
- path: reason; confidence: high|medium|low

Move Recommended
- path: current location -> proposed location, reason; confidence: high|medium|low

Needs Human Decision
- path: question; confidence: high|medium|low

Risks
- item

Evidence Gaps
- missing-evidence-or-none
```

Use `Declutter Verdict: CLEAN` only when no commit, archive, move, or human-decision action is recommended. Use `ACTIONS_RECOMMENDED` when the repo is workable but has proposed actions. Use `BLOCKED` when evidence is insufficient or safety rules prevent a useful report.

## Safety Rules

- Never delete files.
- Treat archive as a proposed move, not a completed action.
- Do not recommend archiving secrets, large datasets, checkpoints, dependency folders, virtual environments, or machine-local state without explicit human instruction.
- Do not silently ignore untracked files. Either classify them or explain why they are out of scope.
- Do not use archive recommendations as a substitute for preserving useful project memory; recommend consolidation first when a file contains active TODOs, lessons, or handover value.
- Do not classify files by filename alone when nearby context is cheap to inspect.
- Do not run mutating commands. Report missing evidence rather than prescribing commands unless the user separately requests an execution plan.
