# InitAI workflow correction

This variant fixes four coordination failures in the original template.

## Runtime requirement

Start the parent Codex chat with the repository trusted. Project config uses `sandbox_mode = "workspace-write"` with `approval_policy = "never"`; read-only custom agents override the inherited sandbox default. Child agents still inherit live parent-turn overrides, so do not launch the parent with a conflicting runtime mode.

## Chosen concurrency model

One top-level chat owns one checkout. Subagents share that checkout and receive disjoint file scopes. The workflow does not create per-agent branches or nested worktrees. For isolated branches, start separate top-level chats in Worktree mode.

## Main-thread rule

The main orchestrator may coordinate, inspect, validate and write `AI_SPACE/` artefacts. It never implements project code. A write-agent permission failure is `[BLOCKED]`, not permission for the main thread to take over.

## Coordination corrections

- Retained allow rules for `tools/write_ai_space_artifact.ps1/.cmd` because they provide a useful narrow write path for `AI_SPACE/`. The wrapper scripts must exist before those commands are invoked.
- Replaced unsupported/obsolete config keys with current Codex keys.
- Removed ambiguous branch/worktree assignment from task packets.
- Added a permission preflight and shared-checkout integration contract.
