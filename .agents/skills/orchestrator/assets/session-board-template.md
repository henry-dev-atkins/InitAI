# Session Board: session__YYYYMMDD_HHMMSS

## Mission

{one-paragraph spec implementation mission}

## Authority and frozen state

- Spec source: `AI_SPACE/SPEC.md`
- Campaign baseline: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/campaign_baseline.json`
- Requirement register: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/requirement_register.json`
- Current checkout:
- Starting canonical active-tree hash:
- Campaign status: ACTIVE | TERMINAL_REVIEW | DONE | BLOCKED
- Active workstream states: {mixed per-workstream states or none}
- Commit policy: one final orchestrator commit unless explicitly overridden

## Capacity

- Maximum concurrent agents: 6
- Active agents:
- GPU-heavy slots: 1
- Active mutable-resource locks:

## Register summary

- Open findings:
- Deferred findings without requirement waiver:
- Resolved findings:
- Active workstreams:
- Accepted workstreams:
- Blocked workstreams:

## Current-state capsule

- Session capsule path: `AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/current_state_capsule.md`
- Global pointer path: `AI_SPACE/current_state.md`
- Capsule tree hash:
- Missing or stale sources:

## Compaction state

- Active session size:
- Versioned plan directories:
- Last compaction manifest:
- Compaction required: yes | no

## Plan portfolio collation

- Latest collation report:
- Safe batches:
- Blocked or conflicting plans:

## Current mixed-stage assignments

| Agent | Role | Workstream/Review | Write Scope | Stable Read Scope | Mutable Resources | State |
|---|---|---|---|---|---|---|
| {agent} | {role} | {WS/review ID} | {paths-or-read-only} | {paths-or-none} | {resource IDs-or-none} | {state} |

## Global gate

- Finding register has no open findings or unwaived deferred requirements.
- No workstream is active, awaiting review, rejected or blocked.
- Requirement register validates with implementation and validation evidence for every unwaived requirement.
- Global validation manifest passes through the trusted runner.
- Evidence ledgers validate for accepted implementation workstreams.
- Every active-tree mutation since the campaign baseline belongs to a current accepted workstream state.
- Six terminal reviewers cover all requirement IDs on the same canonical active-tree hash.
- Repository active-tree hash is unchanged during terminal review.
