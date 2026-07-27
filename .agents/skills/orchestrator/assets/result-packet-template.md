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
commands_run:
  - command: {command}
    exit_code: {code}
    result: {concise result}
validation:
  status: PASS | FAIL | NOT_RUN
  evidence:
    - {requirement -> command/result/path}
unexpected_discoveries:
  - {fact-or-none}
permission_failure: {exact failed operation or none}
temporary_files:
  - {created-and-removed/archived-or-none}
summary: {concise factual result}
```

Packet status is not a workflow decision. The orchestrator sends every implementation result to read-only implementation review.
