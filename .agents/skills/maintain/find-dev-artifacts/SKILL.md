---
name: find-dev-artifacts
description: Review a caller-supplied scope for names and nearby text that describe development history instead of the stable capability.
---

# Find Dev Artifacts

Review exactly the scope supplied by the caller. The scope may be one element,
a file, a directory, tests, configuration, or the whole repository. Use wider
repository context only when it is needed to identify the stable capability or
accepted terminology.

Inspect active names and nearby text, including functions, tests, files,
directories, classes, variables, fields, configuration keys, comments,
docstrings, and public APIs. Report one exact element per finding.

Ignore generated, archived, migration, fixture, and session paths by default.
Review one of those paths only when the caller explicitly names it as the
intended scope.

This is a report-only review. Do not edit files, rename elements, create
workstreams, assign work, choose future work, or create workflow phases.

## What to find

Find names that encode development process rather than the durable capability.
Review cues include finding, requirement, workstream, plan, issue, ticket,
session, run, attempt, retry, phase, stage, step, review, approval,
implementation, planner, worker, orchestrator, agent, scratch, debug, probe,
experiment, generated, fix, patch, hotfix, workaround, migration, old, new,
final, final2, clean, fixed, v2, variant, model, author, and tool identity.

Also look for tests named after findings, plans, failures, or implementation
steps, functions named after plans or experiments, files and directories named
after sessions or reviews, generic process residue such as `helper`, `manager`,
`handler`, `processor`, `utils`, or `misc` when it hides the capability, and
comments or docstrings that preserve obsolete process vocabulary.

These are review cues, not an exhaustive taxonomy or automatic rename rule.
Versioned names are not accepted in active artefacts. Domain terms such as
`legacy`, `version`, `migration`, and `experiment` require review evidence.
Use accepted project terminology when it is available.

Flag confirmed and probable process-derived naming. Probable ambiguity is a
valid finding because unclear names harm searchability and maintenance.

Do not prescribe a replacement name. State the stable capability or accepted
term that the element should express.

## Verdicts

Use exactly one verdict:

- `CLEAN`: no development-process naming was found in scope.
- `NEEDS_RENAMING`: a local naming correction is needed.
- `PROCESS_LEAKAGE`: process-derived naming materially harms capability
  clarity, searchability, monitoring, or maintenance.

## Output

Return exactly this structure. Rank findings from highest impact to lowest.

```text
Verdict: CLEAN | NEEDS_RENAMING | PROCESS_LEAKAGE

Findings
- rank: 1
  severity: HIGH | MEDIUM | LOW
  confidence: CONFIRMED | PROBABLE
  element: <one exact file, directory, symbol, test, field, configuration key, or text>
  capability_or_terminology: <stable capability or accepted term>
  evidence: <scope evidence>
  process_artifact: <development-history meaning>
  impact: <concrete quality, searchability, monitoring, or maintenance impact>

Core Capability Impact
- <impact or none>
```

Do not invent findings, evidence, terminology, or impact. A clean result reports
no findings and does not list every element that passed.
