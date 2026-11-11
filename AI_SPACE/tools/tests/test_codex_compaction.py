"""Tests for deterministic compaction profile and dispatcher generation."""

from pathlib import Path
import importlib.util
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "AI_SPACE/tools/configure_codex_compaction.py"
SPEC = importlib.util.spec_from_file_location("configure_codex_compaction", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CompactionTests(unittest.TestCase):
    def test_repository_profiles_have_unique_metadata(self) -> None:
        profiles = MODULE.load_profiles(ROOT / ".codex/compaction/profiles")
        self.assertEqual(len(profiles), 8)
        self.assertEqual(len({meta["id"] for meta, _, _ in profiles}), 8)

    def test_dispatcher_contains_shared_contract_and_gap_signal(self) -> None:
        profiles = MODULE.load_profiles(ROOT / ".codex/compaction/profiles")
        prompt = MODULE.dispatcher(profiles)
        for field in ("PROFILE:", "STRUCTURE:", "PREVIOUSLY:", "PARKED TASKS:",
                      "CURRENT TASK:", "NEXT ACTION:", "STOP CONDITION:",
                      "DO NOT REPEAT:", "PROFILE_GAP"):
            self.assertIn(field, prompt)
        self.assertIn("Choose exactly one profile", prompt)
        self.assertIn("Never invent a profile", prompt)

    def test_dry_run_does_not_create_external_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            self.assertFalse((home / "config.toml").exists())
            self.assertFalse((home / "initai").exists())


if __name__ == "__main__":
    unittest.main()
