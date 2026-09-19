# Result Packet

```yaml
workstream_id: WSXXX
plan_id: PXXX
agent: {agent-name}
status: DONE | INCOMPLETE | BLOCKED | PERMISSION_BLOCKED
requirement_ids:
  - REQXXX
changed_files_reported:
  - {path-or-none}
scope_deviations_reported:
  - {path-and-reason-or-none}
command_manifest_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/plan_command_manifest.json
validation_ledger: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/evidence/evidence_ledger__WSXXX__PXXX.json
scope_diff_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plans/PXXX/scope_diff.json
command_ids_run:
  - CMD001
unexpected_discoveries:
  - {fact-or-none}
permission_failure: {exact failed operation or none}
temporary_files:
  - {created-and-removed/archived-or-none}
summary: {concise factual result}
```

The manifest and evidence ledger are the command/result authorities. Do not duplicate argv, exit codes or artefact hashes here. Packet status is not a workflow decision. The orchestrator sends every implementation result to read-only implementation review.
