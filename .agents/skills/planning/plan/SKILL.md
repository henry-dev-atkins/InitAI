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

If there is a more elegant way of doing it, replan with that elegant method and iterate until the plan is as elegant as possible. 

The plan must be clear enough for one implementation agent to execute without inventing requirements or broadening scope.

Use supporting skills when they improve this plan. Examples include `$first-principles`, `$bounded-execution`, `$plan-desk-check`, and domain-specific skills. They are tools inside planning. They do not create more orchestration stages.

Use `$pattern-write` only for one new file copied mechanically from one named reference. State the target, reference, permitted differences, protected invariants, and validation. Do not use it for dependencies, schemas, public interfaces, security, concurrency, migrations, shared state, or adjacent edits.

For a successor plan after rejection, state what the previous plan failed to make clear, complete, or correct. Do not produce a cosmetic rewording of the same plan.

## Planning rules

- Resolve the assigned findings completely and minimally.
- Prefer a coherent end state over the smallest diff.
- Remove orphaned code, tests, configuration and documentation recursively when the change makes them redundant.
- Do not preserve legacy compatibility without concrete evidence or explicit authority.
- Split large work into phases that each leave a clear, testable repository state.
- Keep progress in session artefacts and reports. Do not add a progress appendix to a plan.
- Start with the highest-level behaviour required by the workstream; support software must directly enable or validate it.
- Name exact files to create/modify and all off-limits files.
- Name public interfaces, schemas, configs or generated outputs changed/consumed.
- Include consequence analysis for changed types, interfaces, config ownership and downstream consumers.
- Include exact behavioural validation commands and what each proves.
- Do not plan temporary diagnostics as durable outputs.
- Do not assume a later repair phase. The plan must be complete enough for one controlled implementation attempt, while implementation rejection still returns through the normal finding/workstream loop.
- Do not create legacy compatibility, special cases, wrapper layers or speculative abstractions unless the spec requires them.
- What is the simplest thing that could work?

## Planning philosophy

Keep the plan short and factual. 
State the intended end state, required changes, proof, and protected invariants. 
Omit history and external migration detail unless the authority requires them.

When a change removes a concept, trace its dependants until the active repository has no orphaned path that exists only because of the removed concept.
Use the repository archive rules when a durable file must leave the active tree.

Split work at durable boundaries. 
Front-load discovery when the repository is unclear.
Keep later phases mechanical. End each phase with the cheapest meaningful validation.


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


## Iteration 
A plan should be reviewed by `$plan-elegance`, `$plan-desk-check`, and `$plan-review` before submission. 
If the plan is rejected, the next plan must be a standalone plan that includes the rejection findings, then review again.
Submit a perfect plan, possibly after many iterations of planning.