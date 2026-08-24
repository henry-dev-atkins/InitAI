---
name: done
description: Indicates when the requested work has been completed and validated.
--- 

# You are done when:
- The requested change exists in the repo state, not only in docs/plans/reports.
- The code change is complete, coherent and aligned with the spec or explicit human instruction.
- Relevant checks or real runs have been completed at the right stage.
- Exact validation commands/checks and pass results are reported.
- Config, docs and outputs have been updated where behaviour changed.
- Obsolete assumptions and replaced logic in touched areas have been cleaned up.
- Learnings, TODOs and handovers have been updated when relevant.
- Required spec alignment passes a `[SPEC.REVIEW]`, although the review may fail on sections not covered by the plan.
- A plan's implementation is complete, with no gaps, no surprises, no laziness and no workarounds.
- There are no known in-scope gaps, placeholders, workarounds, cosmetic completions or silently deferred items.
- Remaining limitations or next steps are allowed only when:
    - they are outside the requested scope, or
    - they are explicitly approved human deferrals, or
    - the task is reported as `[BLOCKED]`, not `[DONE]`.
- If validation fails or cannot be run, `[DONE]` Means is not satisfied unless the human explicitly requested no validation.
- The deliverable is the completed repo change plus validation evidence, not a plan, diagnosis, classification, note or documented gap.
- Do not stop after naming, documenting or categorising a shortfall. If the requested work is not complete, continue the work loop or report `[BLOCKED]`.
- `[DONE]` is allowed only when the requested work exists in the repo and the relevant validation has passed, or when the human explicitly requested analysis, diagnosis, planning or documentation only.
- `[Done]` during goal mode is normally a sub-task completion, not a real exit.
- `[BLOCKED]` is not completion. Use it only after a concrete implementation/validation attempt fails for a reason outside current authority, available tools or safe operating limits.
- Blocker reports must include:
    - exact command/check that failed or could not be run
    - exact error or missing authority/tooling
    - files changed
    - concrete attempts made
    - smallest next action needed from a human
- Forbidden completion substitutes:
    - "I have documented that ..."
    - "classified as ..."
    - "proof consolidation gap"
    - "the remaining work is ..."
    - "X helped only a little, but Y is still the real blocker"
    - TODO-only, note-only or documentation-only changes unless explicitly requested
- If a gap is found, close it. Do not preserve it as a named category.

# Report
- For implementation, proof, debugging, refactoring and spec-alignment tasks, the final response must begin with either `[DONE]` or `[BLOCKED]`.
- `[DONE]` reports:
    - files changed
    - validation commands/checks run
    - pass result
    - behaviour/spec outcome
- `[BLOCKED]` reports:
    - exact failed/unavailable command or check
    - exact remaining error/blocker
    - concrete repair attempts already made
    - files changed
    - smallest next human decision/action needed
- Do not report `[DONE]` if validation failed, validation was skipped by choice, or the requested behaviour is still absent.