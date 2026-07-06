---
name: plan
description: Use when the prompt contains [PLAN], or when work needs a written, classified plan before editing, testing, validation, orchestration or implementation.
---

# [PLAN]

Planning should be done considering all layers of the project. Get as much relevant documentation and code into context as possible to minimise errors.

Every plan must start with a `[WORK_TYPE]` classification block.

## Required plan sections

1. `Work Classification`
2. `Mission`
3. `Authority`
4. `Scope`
5. `Assumptions`
6. `Implementation Order Rationale`
7. `Implementation Steps`
8. `Validation Gate`
9. `Cleanup Before [DONE]`
10. `Risks / Tradeoffs`
11. `Review Requirements`
12. `Executive Summary`

## Work Classification block

Use `$work-type` and include:

- Primary Work Type
- Authority
- Counts as capability progress
- Commit policy
- Expected commit prefix
- Allowed durable outputs
- Forbidden durable outputs
- Supporting work allowed
- Cleanup before `[DONE]`
- Done gate

## Consequence review

Every plan must consider consequences, for example:

- If a variable changes type, where is it used?
- Do we still assume the old type anywhere?
- Which config keys own this behaviour?
- Which tests or real runs prove behaviour?
- Which files are in scope and off-limits?
- Does this need a subplan?
- Does this create an orchestration or merge conflict?

## Implementation order rationale

Explain why the first implementation steps are the right starting point.

Use the Work Type classification as the main signal. When a core `CAPABILITY.*` or `FIX.ALIGNMENT` target is still missing, plans should normally bias towards that target before surrounding support work. Support work can come first only when the plan explains how it directly enables the next behaviour step.

Examples of support work that needs an ordering rationale when it appears early include runners, config frameworks, logging, reporting, orchestration, cleanup, dependency setup, and validation scaffolding. These examples are warning signs, not fixed bans; the spec and local implementation context decide what is genuinely required. The goal is to avoid spaghettification, tech debt, and code explosions while keeping work focused on core spec capabilities.

## Agentic plan review

All plans require explicit review for:

- overengineering
- minimalism
- technical debt
- redundant iterations
- more elegant implementation missed
- true implementation of the intended framework
- regression to non-correct implementation
- gaps, ambiguity or contradictions
- work type correctness
- file ownership/parallelisation safety

Plans guide execution; plans are not deliverables unless the human explicitly requested plan-only output.
