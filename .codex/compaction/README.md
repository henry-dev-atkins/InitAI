# Codex compaction profiles

InitAI installs one global Codex dispatcher from these human-maintained profiles.
The compaction model chooses one profile for each compaction.

Install from the repository root with an explicit external-edit flag:

```text
python -B AI_SPACE/tools/configure_codex_compaction.py install --apply
python -B AI_SPACE/tools/configure_codex_compaction.py verify
python -B AI_SPACE/tools/configure_codex_compaction.py status
python -B AI_SPACE/tools/configure_codex_compaction.py uninstall --apply
```

The installer changes the Codex user configuration and stores a recoverable backup.
It requires Codex support for `experimental_compact_prompt_file`.

Each profile has frontmatter with `id`, `name`, `summary`, and `version`.
Keep profile IDs stable. Add a new profile when the dispatcher reports `PROFILE_GAP`.
