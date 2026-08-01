# Session Compaction Manifest

```yaml
session_compaction_id: SCXXX
session: session__YYYYMMDD_HHMMSS
status: DONE | BLOCKED
trigger:
  reason: plan_dirs_over_100 | session_over_10mb | post_spec_review_checkpoint | context_pressure
  measured_plan_dirs: 0
  measured_session_size_bytes: 0
capsule_path: AI_SPACE/current_state.md
authoritative_sources:
  - AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/session_board.md
  - AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/finding_register.md
  - AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream_register.md
  - AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/locks.md
archived_paths:
  - {path-or-none}
omitted_or_unread:
  - {path-or-none}
```
