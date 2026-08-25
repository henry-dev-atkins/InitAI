---
name: plan
description: Create one implementation-ready plan for one selected workstream. The plan fixes WHAT is authorised while leaving the implementation agent freedom over HOW to execute it safely.
---

# [PLAN]

Plan one workstream only.

## Required plan sections

- `Plan ID`;
- `Workstream ID`;
- source finding IDs;
- exact spec authority;
- intended durable outcome;
- exact or bounded write scope;
- important read/dependency assumptions;
- ordered implementation steps;
- meaningful validation;
- protected invariants;
- prohibited shortcuts, compatibility layers, fallbacks, or workarounds;


1. `Identity and Traceability`
2. `Work Classification`
3. `Mission`
4. `Scope and Contracts`
5. `Protected Invariants / Must Not`
7. `Implementation Steps`
8. `Validation and Resolution Evidence`
9. `Risks and Assumptions`
11. `Executive Summary`
12. `Am I going in Circles?`
13. `Is there a more elegant way of doing this?`

The plan must be clear enough for one implementation agent to execute without inventing requirements or broadening scope.

Use supporting skills when they improve this plan. Examples include `$planning-and-task-breakdown`, `$first-principles`, `$flowguard`, `$prototype`, and domain-specific skills. They are tools inside planning. They do not create more orchestration stages.

For a successor plan after rejection, state what the previous plan failed to make clear, complete, or correct. Do not produce a cosmetic rewording of the same plan.

## Planning rules

- Resolve the assigned findings completely and minimally.
- Start with the highest-level behaviour required by the workstream; support software must directly enable or validate it.
- Name exact files to create/modify and all off-limits files.
- Name public interfaces, schemas, configs or generated outputs changed/consumed.
- Include consequence analysis for changed types, interfaces, config ownership and downstream consumers.
- Include exact behavioural validation commands and what each proves.
- Do not plan temporary diagnostics as durable outputs.
- Do not assume a later repair phase. The plan must be complete enough for one controlled implementation attempt, while implementation rejection still returns through the normal finding/workstream loop.
- Do not create legacy compatibility, special cases, wrapper layers or speculative abstractions unless the spec requires them.


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

- overengineering;
- minimalism;
- technical debt;
- redundant iterations;
- more elegant implementation missed;
- true implementation of the intended framework;
- regression to non-correct implementation;
- gaps, ambiguity or contradictions;
- work type correctness;
- file ownership/parallelisation safety.
