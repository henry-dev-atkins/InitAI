---
name: implementation-desk-check
description: Desk check an implementation without running the target behaviour. Use when asked for a hypothetical run, desk check, desk execution, manual trace or dry run, or when real execution is slow, expensive, destructive, rate-limited or unavailable. Play computer through representative paths using concrete state and lightweight symbolic reasoning. Return BUG_FOUND, NO_FAILURE_FOUND_IN_TRACED_PATHS or RUNTIME_REQUIRED.
---

# [IMPLEMENTATION.DESK.CHECK]

Desk check an implementation before paying for a real run.

The purpose is not to prove that the implementation works. It is to cheaply find reasons that it cannot work.

Use when asked for a `hypothetical run`, `desk check`, `desk execution`, `manual trace`, `algorithm trace`, `program trace`, `dry run`, or when an expensive execution can first be filtered through structured reasoning.

## Themes

This skill combines ideas from:

- **desk checking / desk execution**: manually work through a program without executing it;
- **program or algorithm tracing**: follow control flow and state changes step-by-step;
- **manual tracing / trace tables**: make intermediate values and state explicit;
- **manual dry runs**: simulate execution without performing the real run;
- **rubber duck debugging**: explain what the code actually does line-by-line until contradictions become visible;
- **lightweight symbolic execution**: carry constrained unknown values through branches when concrete runtime values are unavailable.

This is not formal symbolic execution, abstract interpretation, runtime tracing, or a program's `--dry-run` mode. Those are separate techniques and may execute code or use dedicated analysis machinery.

## Core rule

**Play computer.**

Given representative inputs, follow what the implementation actually says one operation at a time. Do not substitute what the implementation was intended to do.

Do not execute the target behaviour while using this skill. Read-only repository inspection is allowed and expected.

Do not claim that code ran, passed, raised an observed exception, returned an observed value, or produced logs. All results are reasoned results until confirmed by execution.

## Method

1. Define the behaviour being checked and the expected result.
2. Identify the smallest relevant entry point, callers, callees, state and external contracts.
3. Choose the smallest useful scenario set. Normally:
   - one expected path;
   - one boundary or empty-state path;
   - one likely failure path.
4. Prefer concrete values. Where a value is unknown, use a constrained symbolic value such as `records=[]`, `count > retry_limit`, `response.status_code != 200`, or `array.shape == (N, 0)`.
5. State assumptions before depending on them. Keep code-derived facts, user-provided facts, inferences and external assumptions separate.
6. Trace each scenario through:
   - values and types;
   - nullability and collection sizes;
   - array/tensor shapes and units;
   - branch conditions;
   - loop bounds and termination;
   - function calls and returns;
   - mutation and shared state;
   - errors and exception handling;
   - retries;
   - side effects and persistent state;
   - resource acquisition and release;
   - external boundaries.
7. At each boundary, check that the producer's output satisfies the consumer's assumptions.
8. Stop reasoning where the result materially depends on unavailable runtime behaviour. Do not invent the missing result.
9. If a problem is found, identify the first concrete failure mechanism and trace how the scenario reaches it.
10. State the smallest real execution that would confirm the finding or resolve the remaining uncertainty.

A trace table is useful when state changes are non-trivial:

| Step | Location | Input state | Operation / condition | Resulting state |
|---|---|---|---|---|

## Check especially

- wrong or unreachable branches;
- missing branches;
- off-by-one errors;
- empty collections and missing values;
- incorrect defaults;
- type, schema, shape or unit mismatch;
- mutation before validation;
- stale or shared state;
- incorrect ordering;
- swallowed exceptions;
- exceptions after partial side effects;
- retries which cannot terminate or cannot succeed;
- duplicate processing;
- non-idempotent recovery;
- resource leaks;
- assumptions about filesystem, database, network, API or environment behaviour;
- caller/callee contract mismatch.

## Runtime boundaries

Return `RUNTIME_REQUIRED` when the answer materially depends on something that static desk execution cannot establish, including:

- actual database or filesystem contents;
- permissions or environment variables not available to inspect;
- external service responses;
- timing, races, scheduling or concurrency;
- memory or performance behaviour;
- stochastic output;
- hardware behaviour;
- numerical stability or precision that cannot be bounded from the code;
- third-party implementation details not available to inspect.

Do not reason past a runtime boundary as though it were known.

## Findings

A finding must include:

- exact location;
- triggering input/state;
- traced path to the problem;
- expected behaviour;
- hypothetical behaviour;
- why they differ;
- confidence;
- smallest confirming execution.

Bad:

> This function may have an issue with empty lists.

Good:

> `select_latest()` calls `max(records)` before checking whether `records` is empty. With `records=[]`, execution reaches `max([])` before the documented empty-result branch, so that branch is unreachable for the empty case.

## Verdict

Return exactly one:

- `BUG_FOUND`: a concrete logic, data-flow, state or contract failure is established by the traced path;
- `NO_FAILURE_FOUND_IN_TRACED_PATHS`: selected paths remain internally consistent;
- `RUNTIME_REQUIRED`: the relevant result cannot be determined without focused execution.

`NO_FAILURE_FOUND_IN_TRACED_PATHS` does not mean the implementation passed, works, or is correct. It means only that this desk check did not falsify the traced paths.

## Output

```text
[IMPLEMENTATION.DESK.CHECK]

Target:
...

Reason for desk check:
...

Scenarios:
1. ...

Assumptions:
- ...

Trace:
...

Findings:
- ...

Runtime-dependent unknowns:
- ...

Minimum confirming execution:
...

Verdict:
BUG_FOUND | NO_FAILURE_FOUND_IN_TRACED_PATHS | RUNTIME_REQUIRED
```

## Do not

- Do not execute the target behaviour and then describe it as a desk check.
- Do not manufacture logs, timings, exceptions or outputs.
- Do not infer success from the absence of a discovered bug.
- Do not use desk checking as a replacement for required real validation.
- Do not silently assume external systems behave as intended.
- Do not trace every possible branch at once; use separate scenarios.
- Do not continue through an unknown value by inventing a convenient result.
- Do not recommend a full expensive run when one small confirming run answers the question.
