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
6. `Implementation Steps`
7. `Validation Gate`
8. `Cleanup Before [DONE]`
9. `Risks / Tradeoffs`
10. `Review Requirements`
11. `Executive Summary`

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
