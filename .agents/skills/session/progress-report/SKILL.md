---
name: progress-report
description: Create an evidence-based quantitative report for one orchestration session, including workstream progress, finding convergence, rates, ETAs, and a factual retro.
---

# Progress report

Create a report only when the human or orchestrator requests one. 
Require an explicit session path. Do not add a new stage to the orchestrator loop.

## Evidence

Read the current session registers first. Read linked plans, plan reviews, implementation reviews, result packets, handovers, and earlier progress reports.
Ignore `AI_SPACE/archive/` and repository-root `archive/`.

Use explicit ISO-8601 timestamps with timezone before session names and file times.
Use file times only as weak evidence. Use chat timestamps only when the caller supplies them as explicit `LABEL=ISO-8601` inputs. 
Show the source and quality of each time measure.

Missing evidence does not block a useful report. 
Mark the affected metric unavailable. 
Never invent a count, rate, ETA, or conformance result.

## Metrics

Run `scripts/calculate_progress.py` with the explicit session path and report time.
Use its JSON output as the arithmetic source. 
The report author must not recalculate the values by hand.

Use elapsed session time from the session folder timestamp to the report timestamp.
Calculate completed workstream and resolved finding rates per elapsed hour.
Calculate known-backlog ETAs only when a positive observed rate exists.

Known convergence is resolved findings divided by all registered findings. 
Mark it not applicable when no findings exist. 
Perfect convergence requires a fresh clean conformance review. 
A closure percentage alone does not prove it.

Yet-to-find findings are unknown. 
A single conformance review may support a separate low-confidence next-review scenario. 
Project the latest observed finding count and keep it outside the actual convergence measure.

## Report structure

Write Markdown to:

`AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/progress_reports/report_YYYYMMDD_HHMMSS.md`

Use these sections:

1. Report basis and evidence quality.
2. Quantitative progress story.
3. Known convergence and the fresh conformance gate.
4. Completed workstreams.
5. In-progress workstreams.
6. Waiting workstreams.
7. Finding status and the unknown yet-to-find scope.
8. Low-confidence next-review scenario.
9. Retro on process quality.
10. Missing evidence and unavailable metrics.
11. The current capabilities vs the desired capabilities. 'what can we do?' vs 'what do we want to do?'

Summarise each workstream from its register and linked artefacts. 
Include its outcome, state, validation evidence, duration when supported, and blocker when one exists. 
Keep cancelled and superseded workstreams separate from progress totals.

Use the same evidence-led process questions as `$retro`. 
Report process findings and lessons. 
Do not choose future work or write recommendations into workflow registers.

Create the report with `AI_SPACE/tools/write_ai_space_artifact.cmd` in `create` mode. 
Never overwrite an existing timestamped report. 
Return the report path and evidence status in chat. 
Do not paste the full report into chat.
