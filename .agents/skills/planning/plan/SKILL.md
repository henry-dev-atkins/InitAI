---
name: plan
description: Use when the prompt contains [PLAN], or when one assigned workstream needs an implementation plan before editing.
---

# [PLAN]

Create one implementation plan for one assigned workstream. Do not broaden the workstream, create portfolio priorities or absorb unrelated findings.

Apply `$workflow-ontology` and declare one Primary Work Type. Required tests, configuration and behaviour documentation may be supporting changes inside the same coherent workstream.

## Required inputs

- workstream ID;
- source finding IDs;
- exact spec authority;
- dependencies;
- allowed write scope;
- contracts changed and consumed;
- acceptance evidence.

If these are materially missing, return a factual planning blocker to the orchestrator rather than inventing scope.

## Required plan sections

1. `Identity and Traceability`
2. `Work Classification`
3. `Mission`
4. `Scope and Contracts`
5. `Protected Invariants / Must Not`
6. `Command Manifest`
7. `Implementation Steps`
8. `Validation and Resolution Evidence`
9. `Risks and Assumptions`
10. `Result Packet Contract`
11. `Executive Summary`
12. `Am I going in Circles?`
13. `Is there a more elegant way of doing this?`

## Command Manifest

Every plan must include a structured command manifest. Each command entry must declare:

- stable command ID;
- command `argv` or exact shell command;
- working directory;
- purpose;
- expected status;
- evidence target;
- whether it is pre-edit, implementation validation, final validation or diagnostic;
- output artefact paths, if any;
- temp/cache root, if the command writes temporary files.

Pytest commands must use a repo-local `temp/` basetemp. Inline Python snippets must be syntactically valid. Commands must fail loudly and must not rely on silent fallback behaviour.

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

## Supporting review lenses

`[PLAN.REVIEW]` may invoke `plan-elegance`, `maintain-review`, `maintain-elegance`, `maintain-techdebt`, `maintain-despaghettify`, `maintain-declutter` and `peer-review`. These are review criteria, not extra planning stages.

Plans guide implementation; they are not completion deliverables unless plan-only output was explicitly requested.

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
