# InitAI workflow correction

This variant fixes four coordination failures in the original template.

## Runtime requirement

Start the parent Codex chat with the repository trusted and a writable workspace permission mode. In the desktop app, choose `Approve for me` or `Ask for approval` with workspace write before invoking `[ORCHESTRATOR]`. Child agents inherit the parent turn's live mode.

## Chosen concurrency model

One top-level chat owns one checkout. Subagents share that checkout and receive disjoint file scopes. The workflow does not create per-agent branches or nested worktrees. For isolated branches, start separate top-level chats in Worktree mode.

## Main-thread rule

The main orchestrator may coordinate, inspect, validate and write `AI_SPACE/` artefacts. It never implements project code. A write-agent permission failure is `[BLOCKED]`, not permission for the main thread to take over.

## Removed defects

- Removed rules for `tools/write_ai_space_artifact.ps1/.cmd`; those scripts did not exist.
- Replaced unsupported/obsolete config keys with current Codex keys.
- Removed ambiguous branch/worktree assignment from task packets.
- Added a permission preflight and shared-checkout integration contract.
