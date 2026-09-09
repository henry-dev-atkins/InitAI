---
name: comprehensive-testing
description: Complete testing strategy covering TDD workflow, test pyramid, unit/integration/E2E/property testing, framework best practices (pytest), mock strategies, and CI integration. Use when writing tests, reviewing test quality, or establishing testing standards.
---

## Core Philosophy

> "Codex performs best when it has a clear target to iterate against--a test case provides concrete success criteria."

Testing is not about proving code works; it's about **designing code that is testable** and **documenting expected behaviour**.

---

## Test Pyramid

```
        /\
       /  \        E2E Tests (10%)
      /----\       - Full user flows
     /      \      - Slowest, most brittle
    /--------\
   /          \    Integration Tests (20%)
  /------------\   - Component interaction
 /              \  - Real dependencies
/----------------\
       Unit Tests (70%)
       - Single function/method
       - Fast, isolated, many
```

| Level | Speed | Scope | When to Use |
|-------|-------|-------|-------------|
| Unit | <10ms | Single function | All logic |
| Integration | <1s | Multiple components | APIs, DB |
| E2E | <30s | Full flow | Critical paths |

---

## TDD Workflow

### Step 1: Write Tests First

```markdown
Be EXPLICIT about TDD to avoid mock implementations:

"I want to implement [feature] using TDD.
First, write tests for [expected behaviour] with these input/output pairs:
- Input: X -> Expected: Y
- Input: A -> Expected: B
Do NOT create any implementation yet."
```

### Step 2: Verify Tests Fail

```bash
# Run tests and confirm they fail for the RIGHT reason
# Run the repository's focused test command, for example pytest, go test, or the project-specific JavaScript test command.

# Expected: "function not found" or "undefined"
# NOT: syntax error, wrong import
```

### Step 3: Checkpoint Test Suite

Record the failing-test evidence with the current implementation result. Commit only when the accepted plan authorises it.

### Step 4: Implement Incrementally

```markdown
"Now implement the code to make these tests pass.
Do NOT modify the tests.
Run tests after each change until all pass."
```

Codex will enter an autonomous loop:
```
Write code -> Run tests -> Analyze failures -> Adjust -> Repeat
```

### Step 5: Verify with Subagent

```markdown
"Use a subagent to independently verify the implementation:
- Is it overfitting to tests?
- Are edge cases handled?
- Is the code maintainable?"
```

### Step 6: Checkpoint Implementation

Record the passing-test evidence and changed files with the implementation result. Commit only when the accepted plan authorises it.

---

## Test Structure Patterns

1. AAA Pattern (Arrange-Act-Assert)
2. Given-When-Then Pattern
3. User Journey Pattern
4. Property-Based Testing Pattern
5. Mocking and Stubbing Pattern
6. Test Fixtures Pattern
7. Parameterized Tests Pattern

---


## Mock

| Scenario | Mock? | Reason |
|----------|-------|--------|
| External APIs | Yes | Slow, unreliable, costs money |
| Time/Date | Yes | Non-deterministic |
| Random | Yes | Non-deterministic |
| Database (unit) | Yes | Slow, complex setup |
| Database (integration) | No | Test real behaviour |
| Your own code | Rarely | Prefer real implementations |
| File system | Depends | Use temp dirs when possible |

Prefer Test Doubles Over Mocks
