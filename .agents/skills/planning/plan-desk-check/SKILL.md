---
name: plan-desk-check
description: Desk check one implementation plan before source edits. Simulate the ordered plan against current repository state, contracts, dependencies, write scope, and validation to find missing steps, bad ordering, or assumptions that would make implementation fail.
---

# [PLAN.DESK.CHECK]

Desk check a plan before implementation begins.

The purpose is to cheaply find reasons the plan cannot succeed as written. This is a planning review lens. It does not implement the plan and does not replace `$plan-review`.

## Core rule

**Play the plan forward.**

Start from the current repository state. Walk through the plan in order. After each planned step, state the repository or contract state that the next step would receive. Follow what the plan actually authorises, not what an implementer might guess or repair later.

Read-only repository inspection is allowed and expected. Do not edit files or execute the target implementation while using this skill.

## Method

1. Identify the plan, source findings, exact spec authority, intended durable outcome, write scope, dependencies, and validation.
2. Confirm the current repository state needed by the first step.
3. Simulate each implementation step in order.
4. After each step, track the expected changes to files, interfaces, schemas, config, generated outputs, state, and downstream assumptions.
5. Check that the next step can start from that simulated state without inventing missing work.
6. Check that every required contract consequence and affected consumer is covered by an authorised step.
7. Check that planned validation is reachable and would actually prove the source findings are resolved.
8. Stop at any point where success depends on an unstated requirement, unavailable evidence, out-of-scope edit, contradictory ordering, or implementation choice that the plan must decide first.
9. Record the first concrete failure mechanism and any later consequences it causes.
10. If no defect is found, state which steps and assumptions were traced. Do not claim the plan is proven correct.

A trace table is useful:

| Step | Planned action | State before | State after | Dependency / contract check | Finding |
|---|---|---|---|---|---|

## Check especially

- a prerequisite created after it is consumed;
- a required file or contract change outside the authorised write scope;
- a consumer still assuming the old interface, schema, type, or config;
- a validation command that cannot run from the planned state;
- validation that can pass without proving the required behaviour;
- steps that depend on unspecified product or architecture decisions;
- hidden implementation work between two written steps;
- duplicate or contradictory steps;
- ordering that creates a broken intermediate state;
- a plan that requires an ad hoc repair pass to become complete;
- parallel assumptions that conflict with another accepted plan or shared resource.

Use `$change-impact-analysis` when shared-contract consequences need a focused consumer scan. Use `$parallel-safety` when the question is collision risk between accepted plans.

## Verdict

Return exactly one:

- `PLAN_DEFECT_FOUND`: the traced plan contains a concrete missing step, contradiction, scope error, ordering error, or proof gap;
- `NO_DEFECT_FOUND_IN_TRACED_STEPS`: the selected plan path is internally coherent on the inspected repository state;
- `EVIDENCE_REQUIRED`: a material planning decision cannot be checked without named evidence that is not currently available.

`NO_DEFECT_FOUND_IN_TRACED_STEPS` is not plan acceptance. `$plan-review` remains the acceptance authority.

## Output

```text
[PLAN.DESK.CHECK]

Plan:
...

Starting repository state:
...

Trace:
...

Findings:
- ...

Missing evidence:
- ...

Verdict:
PLAN_DEFECT_FOUND | NO_DEFECT_FOUND_IN_TRACED_STEPS | EVIDENCE_REQUIRED
```
