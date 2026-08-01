# Result Packet

```yaml
workstream_id: WSXXX
plan_id: PXXX
agent: {agent-name}
status: DONE | INCOMPLETE | BLOCKED | PERMISSION_BLOCKED
changed_files:
  - {path-or-none}
scope_deviations:
  - {path-and-reason-or-none}
command_manifest_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/plan_command_manifest.json
evidence_ledger_path: AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream__WSXXX__short-name/evidence_ledger.json
commands_run:
  - command_id: CMD001
    argv: [python, -m, pytest, tests/example.py, --basetemp, temp/pytest/WSXXX]
    exit_code: 0
    status: PASS | FAIL | NOT_RUN
    result: {concise result}
validation:
  status: PASS | FAIL | NOT_RUN
  evidence:
    - {requirement -> command_id/result/path}
first_failed_gate: {command_id-or-none}
artefacts:
  - path: {path-or-none}
    sha256: {hash-or-none}
unexpected_discoveries:
  - {fact-or-none}
permission_failure: {exact failed operation or none}
temporary_files:
  - {created-and-removed/archived-or-none}
summary: {concise factual result}
```

Packet status is not a workflow decision. The orchestrator sends every implementation result to read-only implementation review.
