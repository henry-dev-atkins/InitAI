---
name: implementation-desk-check
description: Use when the user asks for a "desk check", "desk execution", "hypothetical run", "manual trace", "trace-table run", "dry run", "run it in your head", or when real execution is slow, expensive, destructive, unavailable, or disproportionate as a first check. Manually trace representative execution paths through control flow, data flow, state changes and contracts without running the code. Prefer concrete inputs; use lightweight symbolic reasoning where concrete values are unavailable.
---

# Implementation Desk Check

## Overview

Desk checking, also called desk execution, is the manual execution of code or an algorithm. "Play computer": take representative inputs and follow what the implementation actually does, step by step, without running it.

Use this as a cheap first filter before expensive execution. The goal is not to prove that the code works. The goal is to find evidence that it cannot work, expose assumptions, or reduce the next real execution to the smallest useful test.

A desk check is reasoning, not runtime evidence. Never report a desk-checked result as "ran", "passed", "failed in execution", or otherwise observed.

## Themes and Related Ideas

This skill combines standard ideas from:

- **Desk checking / desk execution** -- manually "play computer" with test inputs before or instead of an immediate run.
- **Program tracing / algorithm tracing / manual tracing** -- execute code by hand and track values, branches and outputs.
- **Trace tables** -- record variable and state changes explicitly rather than keeping the whole execution in working memory.
- **Manual dry runs** -- work through the algorithm step by step without a computer. Do not confuse this with a program's `--dry-run` mode, which is still real execution.
- **Rubber duck debugging** -- explain what each part of the code actually does, line by line, and notice where that differs from what it was intended to do.
- **Symbolic execution** -- where concrete values are unavailable, carry constrained symbolic values through paths and branch conditions. This skill uses lightweight symbolic reasoning, not a solver or formal symbolic-execution engine.
- **Static testing / code walkthroughs** -- inspect behaviour without relying on runtime execution.

The important common idea is explicit execution reasoning. Do not read code impressionistically and conclude that it "looks right".

## When to Use

Use when:

- the user asks for a `hypothetical run`, `desk check`, `desk execution`, `manual trace`, or to "run it in your head";
- a full test, training job, build, simulation, benchmark, integration or pipeline run is slow or expensive;
- execution consumes paid APIs, scarce hardware, large datasets, GPUs, cloud resources or substantial time;
- execution is destructive or has meaningful external side effects;
- required infrastructure, credentials, data or services are unavailable;
- a failed run needs to be reconstructed from code and known inputs;
- a broad execution can probably be narrowed to one cheap confirming test;
- logic, data-shape, state, ordering or branch errors are plausible before runtime behaviour matters.

Do not use desk checking as an excuse to avoid a focused run that is cheap, safe and available. Desk checking filters execution; it does not replace required verification.

## Core Rule

Follow the code, not the intention.

If the comment says one thing and the implementation does another, trace the implementation. If a branch condition is wrong, follow the wrong branch. If a loop never terminates under the chosen input, stop there and report it. If a value becomes unknown, do not silently choose the value needed for the rest of the path to work.

## Process

### Step 1: TARGET -- Define what is being checked

State:

- the behaviour or claim being examined;
- the entry point;
- the expected outcome or invariant;
- why a real run is currently disproportionate, unavailable or intentionally deferred.

Keep the scope narrow. Trace the smallest call/data-flow cone which can affect the target behaviour.

### Step 2: INPUT -- Choose representative scenarios

Prefer concrete values because they make execution unambiguous.

Normally check:

1. one expected path;
2. one boundary or empty-state path;
3. one plausible failure path.

Add another scenario only when it exercises materially different control flow or state.

Where concrete values are unavailable, use constrained symbolic values, for example:

```text
records = []
count > retry_limit
response.status_code != 200
user_id = missing
array.shape = (N, 0)
```

Do not invent external state, API responses, database contents or configuration.

### Step 3: TRACE -- Play computer

Walk through the implementation in execution order.

Track what matters to the target:

- variable values;
- types and nullability;
- array/tensor/dataframe shapes;
- units and scaling;
- branch conditions and the branch actually taken;
- loop counters, bounds and termination;
- function arguments and returned values;
- mutations and shared state;
- file/database/message state changes;
- exceptions and error paths;
- retries and recovery behaviour;
- external calls and side effects;
- resource acquisition/release;
- ordering dependencies.

Use a trace table when state becomes non-trivial:

| Step | Location | State Before | Operation / Condition | State After | Finding |
|---|---|---|---|---|---|
| 1 | `file.py:fn` | `x=...` | `if ...` | `x=...` | none / issue |

Do not trace every line merely because it exists. Trace every step that changes the relevant state, path or contract.

### Step 4: CONTRACT -- Check boundaries and invariants

At each relevant boundary, ask whether the output of one component is valid input to the next.

Check, where relevant:

- caller/callee contracts;
- types and schemas;
- required/optional fields;
- dimensions and shapes;
- units;
- ordering assumptions;
- mutation ordering;
- idempotency;
- retry termination;
- partial side effects after failure;
- exception handling;
- resource cleanup;
- persistence consistency;
- assumptions about environment or configuration.

A large class of bugs is not inside a function. It is the mismatch between two individually reasonable pieces of code.

### Step 5: FALSIFY -- Look for the first concrete contradiction

Prefer a specific failure mechanism over a general concern.

Bad:

> This may have problems with empty data.

Good:

> `select_latest()` calls `max(records)` before the empty-list guard. With `records=[]`, the trace reaches `max([])` first, so the documented empty-result path is unreachable.

Once a concrete bug explains the target symptom, record it. Continue only if another path is needed to understand material impact.

### Step 6: STOP -- Respect runtime boundaries

Desk checking cannot establish everything.

Mark behaviour as runtime-dependent when the answer materially depends on:

- actual external-service responses;
- real database/file contents not supplied;
- permissions;
- environment variables or deployment configuration;
- race conditions or scheduling;
- timing;
- memory pressure;
- numerical stability/precision that cannot be bounded from the code;
- hardware behaviour;
- performance;
- stochastic output;
- undocumented third-party behaviour.

Do not reason past an unknown by assuming the convenient result.

### Step 7: MINIMUM RUN -- Reduce the real verification

If execution is still required, identify the smallest real run which distinguishes the remaining possibilities.

Prefer, in order:

1. one pure-function/unit test;
2. one small fixture or reduced dataset;
3. one focused integration test;
4. one controlled external call;
5. only then the expensive full run.

The desk check has done useful work if it either finds a bug before execution or makes the required execution smaller.

## Common Failure Modes to Check

Pay particular attention to:

- wrong or inverted branch conditions;
- off-by-one errors;
- empty collections;
- missing/null values;
- wrong defaults;
- stale state;
- mutation before validation;
- unexpected shared mutation;
- shape/schema mismatches;
- units or scaling errors;
- ordering mistakes;
- swallowed exceptions;
- failure after partial side effects;
- ineffective or infinite retries;
- loops which cannot terminate;
- duplicate processing;
- non-idempotent recovery;
- caller/callee disagreement;
- environment assumptions;
- code which does something different from its comment, name or surrounding contract.

## Verdicts

Return exactly one primary verdict:

- `BUG_FOUND` -- the trace identifies a concrete logic, data-flow, state or contract failure.
- `NO_FAILURE_FOUND_IN_TRACED_PATHS` -- the selected paths remain internally consistent. This is not a pass and is not proof of correctness.
- `RUNTIME_REQUIRED` -- the answer depends materially on runtime behaviour which cannot be established from the available code and inputs.

If the requested scope is one disputed claim, make the verdict about that claim rather than the whole codebase.

## Output

Use a compact report:

```text
DESK CHECK

Target
- behaviour/claim
- expected result/invariant
- why desk execution is being used

Scenarios
1. scenario
2. scenario

Assumptions
- assumption + basis

Trace
- trace table or concise step-by-step execution

Findings
- concrete failure mechanism(s), or none in traced paths

Runtime-dependent unknowns
- unknown-or-none

Minimum confirming execution
- smallest useful real test/run, or none needed to establish the bug

Verdict
BUG_FOUND | NO_FAILURE_FOUND_IN_TRACED_PATHS | RUNTIME_REQUIRED
```

Do not pad the report with every correct line of code. Preserve the causal chain needed to reproduce the conclusion.

## Interaction with Other Skills

- **`test-driven-development`** -- a desk check may find the likely bug or narrow the reproduction case, but the failing/passing test remains the behavioural proof when execution is available.
- **`comprehensive-testing`** -- use desk checking to decide which expensive test is actually necessary; do not replace the testing strategy with manual reasoning.
- **`diagnose`** -- desk checking is a diagnostic methodology when code and known inputs can explain the symptom. Diagnosis may still need experimental evidence where runtime state matters.
- **`adversarial-review`** -- desk checking follows execution logic; doubt-driven development provides independent adversarial review. They address different failure modes and can be combined.

## Do

- Use concrete representative inputs first.
- Make assumptions explicit.
- Track state, types, shapes and branch conditions.
- Follow actual code, including incorrect code.
- Use trace tables when state becomes difficult to hold mentally.
- Use lightweight symbolic values when exact inputs are unavailable.
- Stop at runtime-dependent boundaries.
- Prefer falsification over reassurance.
- Reduce expensive verification to the smallest useful real run.

## Do Not

- Do not claim that anything was executed.
- Do not manufacture logs, exceptions, timings, outputs or observations.
- Do not say the implementation "passes" because no bug was found.
- Do not use desk checking as a replacement for required tests.
- Do not silently assume external systems behave as intended.
- Do not invent values to get past an unknown branch.
- Do not trace all possible paths at once; use separate scenarios.
- Do not drift into a general code review when one execution claim is being checked.
- Do not recommend a full expensive run when a smaller confirming experiment answers the question.

## Verification

Before completing a desk check:

- [ ] The target behaviour and expected result are explicit.
- [ ] Representative scenarios were chosen deliberately.
- [ ] Every assumption is separated from code-derived fact.
- [ ] Relevant state and branch conditions were traced in execution order.
- [ ] Caller/callee and data-shape contracts were checked where relevant.
- [ ] Runtime-dependent behaviour was marked rather than invented.
- [ ] Any finding names the exact triggering state and failure mechanism.
- [ ] `NO_FAILURE_FOUND_IN_TRACED_PATHS` was not presented as proof of correctness.
- [ ] The smallest useful real verification was identified where runtime evidence remains necessary.

## Terminology References

The terminology in this skill follows established programming and program-analysis ideas:

- **Steven J. Zeil, Old Dominion University -- Desk-Checking:** uses *desk checking* / *desk execution* for taking test inputs and manually "playing computer" through an algorithm.
- **ETH Zurich -- Program Tracing:** defines program tracing as executing program code by hand with concrete inputs.
- **Trace-table teaching material:** uses trace tables to record variable/output changes during a manual dry run.
- **Hunt and Thomas / Rubber Duck Debugging:** the debugging method of explaining code line by line until the difference between intended and actual behaviour becomes visible.
- **Symbolic-execution literature:** executes paths using symbolic values and path constraints. `implementation-desk-check` borrows the idea of carrying constrained unknowns through code, but does not claim formal symbolic execution or solver-backed proof.

These are related methods, not synonyms in every context. `implementation-desk-check` is the repository term for the combined practical behaviour defined above.
