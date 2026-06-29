plan_id: PXXX
agent: {agent-name}
status: DONE | BLOCKED | NEEDS_REVIEW
primary_work_type: {WORK_TYPE}
branch: codex/PXXX-{short-name}
worktree: {path-or-none}
commits:
  - {hash-or-none}
changed_files:
  - {path}
files_outside_scope:
  - {path-or-none}
validation:
  - command: {exact command}
    result: PASS | FAIL | NOT_RUN
    evidence_path: {path-or-none}
spec_review:
  status: PASS | NON_BLOCKING_FINDINGS | BLOCKING_FINDINGS | NOT_APPLICABLE
  blocking_findings:
    - {finding-or-none}
temporary_work:
  created:
    - {path-or-none}
  removed_or_archived:
    - {path-or-none}
learnings:
  - {learning-or-none}
todos:
  - {todo-or-none}
merge_risk: LOW | MEDIUM | HIGH
merge_notes: {notes}
next_action: {merge | repair | human_decision | none}
