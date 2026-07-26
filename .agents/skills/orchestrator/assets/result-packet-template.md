# Result Packet

plan_id: PXXX
agent: {agent-name}
checkout: shared-parent-session-checkout
status: DONE | BLOCKED | PERMISSION_BLOCKED
changed_files:
  - {path-or-none}
commands_run:
  - {command-or-none}
validation:
  status: PASS | FAIL | NOT_RUN
  evidence: {summary-or-path}
permission_failure: {exact failed operation or none}
unresolved_issues:
  - {issue-or-none}
temporary_files:
  - {created-and-archived-or-none}
summary: {concise result}
