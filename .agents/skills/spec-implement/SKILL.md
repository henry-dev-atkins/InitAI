---
name: spec-implement
description: Use when the prompt contains [SPEC.IMPLEMENT] or [SPEC_IMPLEMENT], or when goal mode requires implementation of AI_SPACE/SPEC.md through the orchestrator loop.
---

# [SPEC.IMPLEMENT] / [SPEC_IMPLEMENT]

Implement the spec through `$orchestrator`.

This skill does not define a second workflow. The authoritative loop is `.agents/skills/orchestrator/SKILL.md`:

1. agentic whole-repository `[SPEC.REVIEW]`;
2. finding collation;
3. independent workstreams;
4. one plan per workstream;
5. agentic plan review and replan until accepted;
6. agentic implementation of accepted independent workstreams;
7. agentic implementation review;
8. update registers and repeat;
9. terminal review on a frozen repository revision.

Use up to six agents per phase when that many ready independent tasks exist. 
Do not invent, duplicate or split work merely to fill capacity, but most spec review results will generate at least 6 workstreams while the repo is not perfectly aligned.

Worker `[DONE]` and `[BLOCKED]` are packet-local. Only the orchestrator may declare the spec implementation complete.

Do not exit as `[DONE]` until `$terminal-condition` passes. A genuine unavailable authority/tooling/data/safety path may produce `[BLOCKED]`.
