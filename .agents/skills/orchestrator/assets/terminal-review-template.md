# Terminal Review Record

The JSON block is the machine-checked terminal record. The table below is only a compact view.

```json
{
  "schema": "terminal-review.v1",
  "terminal_review_id": "TR001",
  "tree_hash": "{canonical-active-tree-hash}",
  "campaign_baseline_path": "AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/campaign_baseline.json",
  "requirement_register_path": "AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/requirement_register.json",
  "finding_register_path": "AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/finding_register.json",
  "workstream_register_path": "AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/workstream_register.md",
  "global_validation_ledger_path": "AI_SPACE/sessions/session__YYYYMMDD_HHMMSS/reports/global-validation/GV001/evidence_ledger.json",
  "reviewers": [
    {
      "review_id": "TRR001",
      "lens": "requirement_coverage",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    },
    {
      "review_id": "TRR002",
      "lens": "behavioural_correctness",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    },
    {
      "review_id": "TRR003",
      "lens": "files_config_outputs",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    },
    {
      "review_id": "TRR004",
      "lens": "extra_prohibited_logic",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    },
    {
      "review_id": "TRR005",
      "lens": "validation_edge_cases",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    },
    {
      "review_id": "TRR006",
      "lens": "holistic_integration_minimality",
      "tree_hash": "{same-hash}",
      "assigned_requirement_ids": ["REQ001"],
      "verdict": "PASS",
      "findings": [],
      "finding_verification_ids": []
    }
  ],
  "status": "PASS"
}
```

| Reviewer | Lens | Tree Hash | Assigned Requirements | Verdict | Findings |
|---|---|---|---|---|---|
| TRR001 | requirement coverage | `{hash}` | `{REQ IDs/range}` | PASS | none |
| TRR002 | behavioural correctness | `{hash}` | `{REQ IDs/range}` | PASS | none |
| TRR003 | files/config/outputs | `{hash}` | `{REQ IDs/range}` | PASS | none |
| TRR004 | extra/prohibited logic | `{hash}` | `{REQ IDs/range}` | PASS | none |
| TRR005 | validation/edge cases | `{hash}` | `{REQ IDs/range}` | PASS | none |
| TRR006 | holistic integration/minimality | `{hash}` | `{REQ IDs/range}` | PASS | none |

Terminal status is `PASS` only when `validate_terminal_coverage.py` passes on the unchanged canonical active tree.
