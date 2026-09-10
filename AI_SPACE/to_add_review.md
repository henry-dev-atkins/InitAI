# Review of `temp/to_add`

Reviewed on `20260910_125720`.

## Scope decision

Do not copy `ai_workflow_context_routing` as a folder. The current repository has moved beyond that snapshot.

Review the context-routing hooks separately. Review only `bulk-read` and `pattern-write` as possible new skills. Keep the current workflow files, agent roster, rules, config, and AI_SPACE tools authoritative.

The bundle contains 44 exact skill copies. They add no behaviour and are omitted from the tables below.

## Context-routing skills

| Candidate | What it does | Goal and philosophy | Current overlap | Subsumption | One-line idea | Contradictions and risks | Repo language |
|---|---|---|---|---|---|---|---|
| `ai_workflow_context_routing/.agents/skills/working/bulk-read/SKILL.md` | Routes large factual reads to a read-only evidence reader. | Reduce caller context cost. Keep judgement and decisive verification with the caller. | Fits current `bounded-execution`, `orchestrator`, `conformance`, and `implementation-desk-check`. | Keep as a small optional skill. Add only a short route in the current orchestrator after the hook is proven. | Delegate raw reading. Verify decisive evidence directly. | Depends on a new agent. Authority-file exemptions must remain exact. The hook may misclassify shell commands. | `bulk-read` → bounded large-file inspection; `evidence index` → cited evidence; `caller` → owning agent. |
| `ai_workflow_context_routing/.agents/skills/working/pattern-write/SKILL.md` | Allows one writer to create one predictable file from one named reference. | Reduce cost for mechanical work. Keep exact scope and independent review. | Fits current accepted plans, write scopes, result packets, and implementation review. | Keep as a narrow orchestrator assignment rule. A separate skill is justified only after repeated use. | Use a low-cost writer only for one exact, low-risk file. | Candidate model and role are absent from the current roster. Validation and eligibility checks need a tested contract. | `pattern-writer` → mechanical implementation agent; `target contract` → accepted plan contract; `protected invariants` → must-preserve behaviour. |

## Context-routing hooks

| Candidate file | What it does | Current overlap | Keep or reject | Main concern |
|---|---|---|---|---|
| `.codex/hooks.json` | Registers a pre-tool hook for oversized reads. | Current repo has no installed hook contract for this event. | Keep as design input only. | Bash matcher, Windows command, event payload, and tool field names need proof against the actual runtime. |
| `.codex/hooks/large_read_guard.py` | Parses selected POSIX and PowerShell read commands and reports large or unbounded output. | Current read rules are allow-list policy. This adds a large parser and a second enforcement path. | Review separately. Do not copy yet. | It is explicitly not a security boundary. Static shell parsing has false-positive and false-negative risk. |
| `.codex/hooks/tests/test_large_read_guard.py` | Tests parser thresholds, exemptions, command forms, and hook output. | Current tests prove the workflow runner. They do not prove hook integration. | Reuse tests only after the runtime contract is fixed. | Unit coverage cannot prove the actual hook receives or returns the expected payload. |
| `.codex/agents/bulk-reader.toml` | Defines a read-only low-cost reader. | Current roster has no `bulk-reader`. | Add only with an accepted plan. | Model, capacity cost, instance identity, and result contract must fit the current runner. |
| `.codex/agents/pattern-writer.toml` | Defines a narrow workspace writer. | Current implementation uses existing role assignments and independent review. | Add only with an accepted plan. | It creates a new write-capable role and must never bypass plan acceptance or review. |

## Context-bundle files to exclude

| Area | Reason |
|---|---|
| 44 exact skill copies | Duplicate current files. Adding them creates no capability. |
| Candidate `orchestrator`, `plan`, `plan-review`, and `conformance` skills | Older variants. The current repo has a checked runner, typed handoffs, conditional manifests and ledgers, invalidation rules, and newer failure handling. Replacement would regress those contracts. |
| Candidate `.codex/TEAM.md` and `AGENTS.md` | Duplicate authority. They would compete with current workflow and repository instructions. |
| Candidate `.codex/config.toml` | Current config already has workspace-write mode, approval disabled, and blocked network. The candidate adds unverified hook and agent settings. Do not replace the current config. |
| `AI_SPACE/tools/write_ai_space_artifact.py` | The candidate writer resolves the `AI_SPACE` directory as its root, then appears to append `AI_SPACE` again during allowed-path checks. Treat it as untrusted copied code. |
| Candidate read-inspection rules | Some allow-list ideas are useful. Current `.codex/rules` already owns this policy. Merge only a proven gap. |

## Other candidates in `temp/to_add`

| Candidate | What it does | Overlap and best home | Decision |
|---|---|---|---|
| `SKILL (3).md` | Removes common AI writing patterns. | Strong overlap with `code-style`, `simplified-technical-english`, `henrys-voice`, and AGENTS rules. | Subsumed. Do not add. |
| `SKILL (4).md` | Investigates the reason behind code or requests. | Partial overlap with `first-principles` and `diagnose`. Requires absent skills, references, external systems, and unavailable model names. | Reject as copied. Revisit only as a small local intent-review skill. |
| `SKILL (5).md` | Combines technical-writing standards and unslop rules. | Strong overlap with current writing skills and AGENTS rules. | Subsumed. Do not add. |
| `SKILL (6).md` | Explains what, how, and why with optional diagrams. | Overlaps `implementation-desk-check`, `first-principles`, and `code-style`. Requires absent `how` and `why` skills. | Subsumed. Do not add. |
| `SKILL (7).md` | Requires decision logs, transcript evidence, and cross-model review. | Overlaps current AI_SPACE evidence, result packets, and adversarial review. Adds output sprawl and absent files. | Reject. |
| `SKILL (8).md` | Unfinished glossary copy of current action routing. | Duplicates `AGENTS.md`. Has no frontmatter or usable skill identity. | Reject. |
| `code-tour/SKILL.md` | Creates verified CodeTour JSON files. | No current consumer or `.tours` convention. Partial overlap with execution tracing. | Optional only if a real CodeTour consumer appears. |
| `scientific-literature-review/SKILL.md` | Runs structured literature searches and synthesis. | Partial overlap with `peer-review`. No current literature workflow. | Optional research skill. Keep outside the coding core. |
| `write-concisely/SKILL.md` | Writes short technical prose. | Strong overlap with current writing guidance. | Subsumed. Do not add. |
| `writing-guide/SKILL.md` | Gives general plain-writing advice. | Strong overlap with current writing guidance. | Subsumed. Do not add. |
| `anti-verbosity-gate-main` | Adds a style engine and hooks. | Current AGENTS rules already set communication limits. Its hook names, payloads, transcript format, and fail-open behaviour are unverified. | Exclude from this review path. |

## Final recommendation

Preserve the current workflow implementation unchanged.

Treat `bulk-read` and `pattern-write` as two independent skill candidates.

Treat `large_read_guard.py` and its hook registration as a separate feature requiring runtime-contract tests.

Do not import the surrounding snapshot, copied skills, altered workflow skills, candidate config, candidate TEAM file, candidate AGENTS file, or candidate AI_SPACE writer.
