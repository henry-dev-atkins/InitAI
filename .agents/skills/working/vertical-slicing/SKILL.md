---
name: vertical-slicing
description: Delivers changes incrementally during implementation or planning. Use when planning or implementing any work that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step. 
---

# Vertical Slicing
Incremental implementation is a synonym.
May be invoked as a planner, which applies these to a read only planner.

## Overview

Build in thin vertical slices -- implement one piece, test it, verify it, then expand. Avoid implementing an entire feature in one pass. Each increment should leave the system in a working, testable state. This is the execution discipline that makes large features manageable.

Support three modes within it:

1) walking skeleton -> first minimal end-to-end path
2) risk-first slice -> attack uncertainty
3) vertical slice -> normal implementation unit

## When to Use

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

**When NOT to use:** Single-file, single-function changes where the scope is already minimal.

## The Increment Cycle

```
┌──────────────────────────────────────┐
│                                      │
│ Implement ──-> Test ──-> Verify ──┐  │
│       ▲                           │  │
│       └── Checkpoint ◄────────────┘  │
│              │                       │
│              ▼                       │
│          Next slice                  │
│                                      │
└──────────────────────────────────────┘
```

For each slice:

1. **Implement** the smallest complete piece of functionality
2. **Test** -- run the test suite (or write a test if none exists)
3. **Verify** -- confirm the slice works as expected (tests pass, build succeeds, manual check)
4. **Checkpoint** -- record changed files, verification evidence, and the next slice. Commit only when the accepted plan authorises it.
5. **Move to the next slice** -- carry forward, do not restart

## Slicing Strategies

1. Vertical Slices (Preferred). Each slice delivers working end-to-end functionality.

2.  Contract-First Slicing. When backend and frontend need to develop in parallel.

3.  Risk-First Slicing. Tackle the riskiest or most uncertain piece first.



## Verification

After completing all increments for a task:

- [ ] Each increment was individually tested and checkpointted
- [ ] The full test suite passes
- [ ] The build is clean
- [ ] The feature works end-to-end as specified
- [ ] No uncheckpointted changes remain
