---
name: workflow-ontology
description: All work is classified into a work type. Use this skill to classify work type and enforce the work type ontology.
---

Classify the work before planning or reviewing implementation.

## Required output

Every plan must declare:

- Primary Work Type
- Authority
- Counts as capability progress
- Commit policy
- Expected commit prefix, if any
- Allowed durable outputs
- Forbidden durable outputs
- Supporting work allowed
- Cleanup before `[DONE]`
- Done gate

## Classification rules

A plan has exactly one Primary Work Type.

If a task mixes durable purposes, split it into separate plans or create `[SUBPLAN]` work.

Do not let temporary diagnostics, local environment adaptations, docs, cleanup, or validation evidence masquerade as capability progress.

## Work Type Ontology

### `CAPABILITY.RESEARCH`

Durable research capability described by `AI_SPACE/SPEC.md`.

Examples:
- experiment framework behaviour
- model/training/evaluation behaviour
- analysis logic needed for real research runs
- config-driven experiment capability
- correctness checks for research behaviour

Commit policy: commit required when complete.  
Counts as capability progress: yes.  
Typical commit prefixes: `FEAT:`, `CONFIG:`, `TEST:`, `FIX:`.  
Required closure: real behavioural validation where practical, plus `[SPEC_REVIEW]`.

### `CAPABILITY.PRODUCT`

Durable product/user-facing capability described by `AI_SPACE/SPEC.md`.

Examples:
- app behaviour
- CLI/user workflow
- report/export behaviour
- user-visible analysis outputs
- experimental tooling

Commit policy: commit required when complete.  
Counts as capability progress: yes.  
Typical commit prefixes: `FEAT:`, `CONFIG:`, `TEST:`, `FIX:`.  
Required closure: user-path validation, behaviour check, docs/config update where behaviour changed, plus `[SPEC_REVIEW]`.

### `EVIDENCE.VALIDATION`

Durable validation evidence for a capability.

Examples:
- tests that prove expected behaviour
- reproducible experiment configs
- lightweight result summaries
- validation scripts intended to be reused
- benchmark/report generation code

Commit policy: commit reusable validation code/configs/reports; do not casually commit large raw outputs, datasets or checkpoints.  
Counts as capability progress: supports capability progress, but is not itself a capability unless the spec says so.  
Typical commit prefixes: `TEST:`, `CONFIG:`, `DOCS:`.  
Required closure: exact command/check reported, result captured, output location intentional.

### `FIX.ALIGNMENT`

Durable correction of code, config, tests, or docs so current implementation matches the spec or explicit human instruction.

Examples:
- root-cause bug fix
- removing stale behaviour
- correcting config ownership
- fixing an implementation/spec mismatch
- deleting legacy-path assumptions by replacing them with current-state logic

Commit policy: commit required when complete.  
Counts as capability progress: only if it restores or unlocks a spec capability.  
Typical commit prefixes: `FIX:`, `CONFIG:`, `TEST:`.  
Required closure: failing behaviour reproduced or evidenced, fix implemented, relevant validation passes.

### `DEPENDENCY.LOCAL`

Portable local dependency or repo infrastructure needed to make durable work possible.

Examples:
- setup scripts
- runner scripts
- `.codex/` config
- repo-local tool configuration
- dependency updates
- environment checks
- platform setup that is reusable by other agents/humans

Commit policy: commit only if portable, reusable, and justified.  
Counts as capability progress: no; it only enables capability work.  
Typical commit prefixes: `CONFIG:`, `FIX:`, `AI:`.  
Required closure: dependency is justified, documented, reproducible, and does not silently change research/product behaviour.

### `TEMPORARY.DIAGNOSTIC`

Temporary work used to understand a failure or inspect behaviour.

Examples:
- debug logging
- scratch scripts
- one-off probes
- temporary assertions
- intermediate experiment snippets
- diagnostic notebooks/scripts

Commit policy: do not commit by default. Keep under `temp/` or archive/remove before `[DONE]`.  
Counts as capability progress: no.  
Typical commit prefixes: none.  
Required closure: diagnostic result is either converted into durable work, recorded in learnings/TODO where relevant, or removed/archived.

### `ENVIRONMENT.ADAPTATION`

Quarantined adaptation for a local/sandbox/platform constraint that is not a real product/research fix.

Examples:
- Windows-only sandbox helper
- local path shim
- temporary launcher needed by Codex/local execution
- machine-specific setup workaround

Commit policy: do not commit unless explicitly approved or clearly portable and isolated.  
Counts as capability progress: no.  
Typical commit prefixes: `CONFIG:` or `AI:` only when approved.  
Required closure: must be isolated from core behaviour, documented as environment-only, and must not be used to claim capability closure.

### `FLUFF.DISPOSABLE`

One-off material with no durable spec, validation, documentation, or workflow value.

Examples:
- throwaway plots
- ad hoc screenshots
- exploratory output dumps
- duplicated reports
- unneeded progress notes
- one-off notebooks not used for validation

Commit policy: never commit. Move to `archive/` or keep under `temp/` if still useful during the active session.  
Counts as capability progress: no.  
Required closure: removed, archived, or converted into `EVIDENCE.VALIDATION` if it becomes real evidence.

### `DOCS.MEMORY`

Durable documentation, handover, TODO, learning, or instruction update.

Examples:
- `AI_SPACE/AI_LEARNINGS_LOG.md`
- `AI_SPACE/TODO.md`
- handovers
- AGENTS/skill updates
- docs that explain changed behaviour

Commit policy: commit when requested, when part of `[SESSION.END]`, or when required to preserve learning.  
Counts as capability progress: no, unless paired with actual implementation.  
Typical commit prefixes: `DOCS:`, `AI:`.  
Required closure: documentation must describe real repo state, not substitute for unfinished implementation.

### `CLEANUP.HYGIENE`

Durable repo organisation that improves navigability without changing behaviour.

Examples:
- moving clutter to `archive/`
- consolidating duplicate notes
- organising outputs
- removing stale temporary files by archiving
- renaming files for clarity

Commit policy: commit if durable and useful.  
Counts as capability progress: no.  
Typical commit prefix: `CLEANUP:`.  
Required closure: no behaviour change unless explicitly stated; no deletion, only archive/move according to repo rules.

### `SPEC.EDIT`

A change to `AI_SPACE/SPEC.md`.

Examples:
- changing project goals
- updating capability definitions
- adding/removing milestones
- clarifying expected behaviour

Commit policy: commit required if applied.  
Counts as capability progress: no; it changes the target.  
Typical commit prefix: `SPEC_EDIT:`.  
Required closure: allowed only when `[SPEC EDIT REQUIRED]` is present; must run the spec-edit workflow and downstream consequence review.
