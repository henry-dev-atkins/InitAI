---
name: test-driven-development
description: Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behaviour. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality.
---

# Test-Driven Development

## Overview

Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix. Tests are proof -- "seems right" is not done. A codebase with good tests is an AI agent's superpower; a codebase without tests is a liability.

## When to Use

- Implementing any new logic or behaviour
- Fixing any bug (the Prove-It Pattern)
- Modifying existing functionality
- Adding edge case handling
- Any change that could break existing behaviour

**When NOT to use:** Pure configuration changes, documentation updates, or static content changes that have no behavioural impact.

## Discover the Stack First

The TDD cycle is universal; the commands are not. Before writing the first test, discover how *this* repository tests, and use its commands for verification:
1. Language and build system
2. Checked-in wrappers
3. Test framework and configuration
4. Existing conventions
5. Documented commands

## The TDD Cycle

```
 Write a test    Write minimal code    Clean up the
 that fails  ──->  to make it pass  ──->  implementation  ──->  (repeat)
      │                  │                    │
      ▼                  ▼                    ▼
   Test FAILS        Test PASSES         Tests still PASS
```

1. Write a Failing Test. Write the test first. It must fail. A test that passes immediately proves nothing.
2. Make It Pass. Write the minimum code to make the test pass. Don't over-engineer.
3. Refactor and Clean Up. Run tests after every refactor step to confirm nothing broke. 


## The Prove-It Pattern (Bug Fixes)

When a bug is reported, **do not start by trying to fix it.** Start by writing a test that reproduces it.

```
Bug report arrives
       │
       ▼
  Write a test that demonstrates the bug
       │
       ▼
  Test FAILS (confirming the bug exists)
       │
       ▼
  Implement the fix
       │
       ▼
  Test PASSES (proving the fix works)
       │
       ▼
  Run full test suite (no regressions)
```

## The Test Pyramid

Invest testing effort according to the pyramid -- most tests should be small and fast, with progressively fewer tests at higher levels:

```
          ╱╲
         ╱  ╲         E2E Tests (~5%)
        ╱    ╲        Full user flows, real browser
       ╱──────╲
      ╱        ╲      Integration Tests (~15%)
     ╱          ╲     Component interactions, API boundaries
    ╱────────────╲
   ╱              ╲   Unit Tests (~80%)
  ╱                ╲  Pure logic, isolated, milliseconds each
 ╱──────────────────╲
```

**The Beyonce Rule:** If you liked it, you should have put a test on it. Infrastructure changes, refactoring, and migrations are not responsible for catching your bugs -- your tests are. If a change breaks your code and you didn't have a test for it, that's on you.

### Test Sizes (Resource Model)

Beyond the pyramid levels, classify tests by what resources they consume:

| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network, no database | Milliseconds | Pure function tests, data transforms |
| **Medium** | Multi-process OK, localhost only, no external services | Seconds | API tests with test DB, component tests |
| **Large** | Multi-machine OK, external services allowed | Minutes | E2E tests, performance benchmarks, staging integration |

Small tests should make up the vast majority of your suite. They're fast, reliable, and easy to debug when they fail.

### Decision Guide

```
Is it pure logic with no side effects?
  -> Unit test (small)

Does it cross a boundary (API, database, file system)?
  -> Integration test (medium)

Is it a critical user flow that must work end-to-end?
  -> E2E test (large) -- limit these to critical paths
```

## Writing Good Tests

### Test State, Not Interactions

Assert on the *outcome* of an operation, not on which methods were called internally. Tests that verify method call sequences break when you refactor, even if the behaviour is unchanged.


### DAMP Over DRY in Tests

In production code, DRY (Don't Repeat Yourself) is usually right. In tests, **DAMP (Descriptive And Meaningful Phrases)** is better. A test should read like a specification -- each test should tell a complete story without requiring the reader to trace through shared helpers.


Duplication in tests is acceptable when it makes each test independently understandable.

### Prefer Real Implementations Over Mocks

Use the simplest test double that gets the job done. The more your tests use real code, the more confidence they provide.

```
Preference order (most to least preferred):
1. Real implementation  -> Highest confidence, catches real bugs
2. Fake                 -> In-memory version of a dependency (e.g., fake DB)
3. Stub                 -> Returns canned data, no behaviour
4. Mock (interaction)   -> Verifies method calls -- use sparingly
```

**Use mocks only when:** the real implementation is too slow, non-deterministic, or has side effects you can't control (external APIs, email sending). Over-mocking creates tests that pass while production breaks.

### One Assertion Per Concept

Each test should focus on a single concept or behaviour. This makes it clear what is being tested and why a test might fail.


### Name Tests Descriptively

A good test name clearly communicates the scenario being tested and the expected outcome. Use descriptive names that convey intent, not implementation details.


## Test Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Tests break when refactoring even if behaviour is unchanged | Test inputs and outputs, not internal structure |
| Flaky tests (timing, order-dependent) | Erode trust in the test suite | Use deterministic assertions, isolate test state |
| Testing framework code | Wastes time testing third-party behaviour | Only test YOUR code |
| Snapshot abuse | Large snapshots nobody reviews, break on any change | Use snapshots sparingly and review every change |
| No test isolation | Tests pass individually but fail together | Each test sets up and tears down its own state |
| Mocking everything | Tests pass but production breaks | Prefer real implementations > fakes > stubs > mocks. Mock only at boundaries where real deps are slow or non-deterministic |

## When to Use Subagents for Testing

For complex bug fixes, spawn a subagent to write the reproduction test:

```
Main agent: "Spawn a subagent to write a test that reproduces this bug:
[bug description]. The test should fail with the current code."

Subagent: Writes the reproduction test

Main agent: Verifies the test fails, then implements the fix,
then verifies the test passes.
```

This separation ensures the test is written without knowledge of the fix, making it more robust.

## See Also

For broader testing strategy, use `$comprehensive-testing`. 

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write tests after the code works" | You won't. And tests written after the fact test implementation, not behaviour. |
| "This is too simple to test" | Simple code gets complicated. The test documents the expected behaviour. |
| "Tests slow me down" | Tests slow you down now. They speed you up every time you change the code later. |
| "I tested it manually" | Manual testing doesn't persist. Tomorrow's change might break it with no way to know. |
| "The code is self-explanatory" | Tests ARE the specification. They document what the code should do, not what it does. |
| "It's just a prototype" | Prototypes become production code. Tests from day one prevent the "test debt" crisis. |
| "Let me run the tests again just to be extra sure" | After a clean test run, repeating the same command adds nothing unless the code has changed since. Run again after subsequent edits, not as reassurance. |

## Red Flags

- Writing code without any corresponding tests
- Reaching for a default test command without checking what this repository actually uses
- Tests that pass on the first run (they may not be testing what you think)
- "All tests pass" but no tests were actually run
- Bug fixes without reproduction tests
- Tests that test framework behaviour instead of application behaviour
- Test names that don't describe the expected behaviour
- Skipping tests to make the suite pass
- Running the same test command twice in a row without any intervening code change

## Verification

After completing any implementation:

- [ ] Every new behaviour has a corresponding test
- [ ] The full suite passes, run with the repository's own test command (`npm test`, `./gradlew test`, `pytest`, `go test ./...`, ...)
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe the behaviour being verified
- [ ] No tests were skipped or disabled
- [ ] Coverage hasn't decreased (if tracked)

**Note:** Run each test command after a change that could affect the result. After a clean run, don't repeat the same command unless the code has changed since -- re-running on unchanged code adds no confidence.
