---
name: learn
description: Use when the prompt contains [LEARN], or when work has produced lessons, mistakes, debugging discoveries, orchestration lessons, failed plans, validation discoveries or course corrections that should update AI_SPACE/AI_LEARNINGS_LOG.md and AI_SPACE/TODO.md.
---

# [LEARN]

`AI_SPACE/AI_LEARNINGS_LOG.md` stores lessons, mistakes and vital information discovered through work. Keep it clean.

- Update learnings after failures, debugging discoveries, architecture/course corrections and mistakes.
- Propose stale learnings for removal, but remove only with explicit human approval if removal changes project memory materially.
- Make surgical doc/spec updates only with the required authority.
- Update `AI_SPACE/TODO.md` only with concrete unresolved work.
- Use the required `Blocking`, `Ready` and `Deferred` sections.
- Write each item as a checkbox bullet with its action and current reason, dependency or evidence.
- Include the linked finding or workstream identifier when one exists.
- Do not append historical session prose.
- Do not use TODO/learnings updates as a substitute for completing requested implementation, proof, validation or spec-alignment work.
- For orchestrated work, record agent/team process lessons only when they change future behaviour.
- If work has turned into process churn or repeated setup migration, run `retro`, assess throughput against the user's actual goal, and pivot to the smallest packet that produces or protects the target outcome.
- Use `maintain-review` when a learning is about repo work drifting into avoidable surrounding software, wrapper code, or non-capability work.
- Use `maintain-techdebt` when a learning exposes durable repo/codebase maintenance debt.
- Use `maintain-despaghettify` when a learning shows tangled code ownership, duplicated implementation paths, or unclear module boundaries.

## Approval friction lessons

When repeated approval prompts interrupt routine work:

- Diagnose whether `.codex/rules/` is missing narrow allow rules or whether the command style prevents prefix matching.
- Prefer durable, repo-local allow rules for read-only inspection commands that the human repeatedly authorises.
- Keep mutating commands guarded even when they are repeatedly approved.
- Record command-style lessons in `AI_SPACE/AI_LEARNINGS_LOG.md` when they change future behaviour.
- Prefer stable command names over aliases: use `Get-Content` instead of `cat`, `rg` instead of `grep`, and `Get-ChildItem` instead of `ls`.
- Avoid PowerShell pipelines and complex inline shell syntax for routine inspection; use separate simple commands or direct `rg -e ... -- path` searches.
