#!/usr/bin/env python3
"""Install and verify a human-maintained Codex compaction profile dispatcher."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Iterable


MANAGED_KEY = "experimental_compact_prompt_file"
MARKER = "# initai-compaction-managed"
INSTALLER_VERSION = "1"
FRONTMATTER = re.compile(r"\A---\n(?P<meta>.*?)\n---\n(?P<body>.*)\Z", re.DOTALL)
REQUIRED = ("id", "name", "summary", "version")


class ConfigurationError(RuntimeError):
    """Report an invalid profile or unsafe configuration operation."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def codex_home(value: str | None) -> Path:
    return Path(value or os.environ.get("CODEX_HOME") or (Path.home() / ".codex")).expanduser().resolve()


def profile_root(value: str | None) -> Path:
    return (repo_root() / (value or ".codex/compaction/profiles")).resolve()


def parse_profile(path: Path) -> tuple[dict[str, str], str]:
    match = FRONTMATTER.fullmatch(path.read_text(encoding="utf-8"))
    if not match:
        raise ConfigurationError(f"Profile has invalid frontmatter: {path}")
    metadata: dict[str, str] = {}
    for line in match.group("meta").splitlines():
        if ":" not in line:
            raise ConfigurationError(f"Profile metadata line is invalid: {path}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    missing = [key for key in REQUIRED if not metadata.get(key)]
    if missing:
        raise ConfigurationError(f"Profile missing metadata {missing}: {path}")
    body = match.group("body").strip()
    if not body:
        raise ConfigurationError(f"Profile body is empty: {path}")
    return metadata, body


def load_profiles(root: Path) -> list[tuple[dict[str, str], str, Path]]:
    if not root.is_dir():
        raise ConfigurationError(f"Profile directory does not exist: {root}")
    profiles = []
    seen: set[str] = set()
    for path in sorted(root.glob("*.md")):
        metadata, body = parse_profile(path)
        identifier = metadata["id"]
        if identifier in seen:
            raise ConfigurationError(f"Duplicate profile ID: {identifier}")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", identifier):
            raise ConfigurationError(f"Profile ID is not portable: {identifier}")
        seen.add(identifier)
        profiles.append((metadata, body, path))
    if not profiles:
        raise ConfigurationError(f"No profiles found: {root}")
    return profiles


def digest(paths: Iterable[Path]) -> str:
    hasher = hashlib.sha256()
    for path in paths:
        hasher.update(path.name.encode())
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def dispatcher(profiles: list[tuple[dict[str, str], str, Path]]) -> str:
    catalogue = "\n\n".join(
        f"PROFILE ID: {meta['id']}\nPROFILE NAME: {meta['name']}\nPROFILE SUMMARY: {meta['summary']}\nPROFILE RULES:\n{body}"
        for meta, body, _ in profiles
    )
    return f"""# InitAI Codex compaction dispatcher

You are compacting context for the next model. Choose exactly one profile from the catalogue below for this compaction.
Choose even when confidence is low. Never invent a profile and never use a generic fallback.
If no profile is a strong fit, choose the closest profile and set PROFILE_GAP to the missing capability.

{catalogue}

Return only this checkpoint. Preserve exact paths, commands, errors, decisions, pending agents, approvals, and validation state when present.

PROFILE:
PROFILE_CONFIDENCE:
PROFILE_GAP:

STRUCTURE:
Describe how the conversation was organised and which phases are complete.

PREVIOUSLY:
Preserve the timeline, completed work, evidence, decisions, and stable facts.

PARKED TASKS:
Preserve deferred threads, blockers, and context-only notes.

CURRENT TASK:
State the active objective, phase, exact state, files, plans, agents, and pending work.

NEXT ACTION:
State the immediate continuation action.

STOP CONDITION:
State what proves the current task is complete or blocked.

DO NOT REPEAT:
List rejected paths, completed exploration, and known mistakes.
"""


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def config_path(home: Path) -> Path:
    return home / "config.toml"


def codex_version() -> str:
    result = subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise ConfigurationError("Unable to run codex --version")
    return result.stdout.strip()


def validate_codex_setting(generated: Path) -> None:
    value = f"{MANAGED_KEY}={str(generated)!r}"
    result = subprocess.run(
        ["codex", "--strict-config", "-c", value, "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise ConfigurationError(
            f"Codex does not accept {MANAGED_KEY}: {(result.stderr or result.stdout).strip()}"
        )


def managed_config(home: Path, generated: Path, apply: bool) -> None:
    path = config_path(home)
    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines(keepends=True)
    replacement = f'{MANAGED_KEY} = {str(generated)!r} {MARKER}\n'
    matching = [index for index, line in enumerate(lines) if line.startswith(f"{MANAGED_KEY} =")]
    if len(matching) > 1:
        raise ConfigurationError(f"Multiple {MANAGED_KEY} settings found: {path}")
    if matching and MARKER not in lines[matching[0]]:
        raise ConfigurationError(f"Existing {MANAGED_KEY} is not owned by InitAI: {path}")
    updated = list(lines)
    if matching:
        updated[matching[0]] = replacement
    else:
        if updated and not updated[-1].endswith("\n"):
            updated.append("\n")
        updated.append(replacement)
    if apply:
        backup = path.with_suffix(path.suffix + ".initai-backup")
        if not backup.exists() and path.exists():
            shutil.copy2(path, backup)
        atomic_write(path, "".join(updated))
    else:
        print(f"DRY RUN: would update {path}")


def install(args: argparse.Namespace) -> None:
    profiles = load_profiles(profile_root(args.profile_dir))
    home = codex_home(args.codex_home)
    version = codex_version()
    generated = home / "initai" / "compaction" / "dispatcher.md"
    validate_codex_setting(generated)
    bundle = dispatcher(profiles)
    if args.apply:
        atomic_write(generated, bundle)
    else:
        print(f"DRY RUN: would write {generated}")
    managed_config(home, generated, args.apply)
    print(f"codex={version}\nprofiles={','.join(meta['id'] for meta, _, _ in profiles)}\ndigest={digest([path for _, _, path in profiles])}")


def verify(args: argparse.Namespace) -> None:
    profiles = load_profiles(profile_root(args.profile_dir))
    home = codex_home(args.codex_home)
    generated = home / "initai" / "compaction" / "dispatcher.md"
    config = config_path(home)
    if not config.is_file() or not generated.is_file():
        raise ConfigurationError("InitAI compaction dispatcher is not installed")
    if str(generated) not in config.read_text(encoding="utf-8"):
        raise ConfigurationError("Codex config does not point to the InitAI dispatcher")
    expected = dispatcher(profiles)
    if generated.read_text(encoding="utf-8") != expected:
        raise ConfigurationError("Generated dispatcher is stale")
    print(f"verified codex={codex_version()} profiles={','.join(meta['id'] for meta, _, _ in profiles)}")


def uninstall(args: argparse.Namespace) -> None:
    home = codex_home(args.codex_home)
    path = config_path(home)
    if not path.is_file():
        raise ConfigurationError(f"Codex config does not exist: {path}")
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    matching = [(index, line) for index, line in enumerate(lines)
                if line.startswith(f"{MANAGED_KEY} =")]
    if len(matching) != 1 or MARKER not in matching[0][1]:
        raise ConfigurationError("Managed InitAI compaction setting is absent or not owned by InitAI")
    updated = "".join(line for index, line in enumerate(lines) if index != matching[0][0])
    generated = home / "initai" / "compaction" / "dispatcher.md"
    if not args.apply:
        print(f"DRY RUN: would update {path}")
        print(f"DRY RUN: would move {generated} to the InitAI compaction archive")
        return
    atomic_write(path, updated)
    if generated.is_file():
        archive = generated.parent / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        shutil.move(str(generated), str(archive / "dispatcher.md"))
    print(f"uninstalled={path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("install", "verify", "status", "uninstall"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--codex-home")
    parser.add_argument("--profile-dir")
    args = parser.parse_args()
    try:
        if args.command == "install":
            install(args)
        elif args.command == "verify":
            verify(args)
        elif args.command == "status":
            print(f"codex={codex_version()}\ncodex_home={codex_home(args.codex_home)}")
        else:
            uninstall(args)
    except ConfigurationError as error:
        print(f"ERROR: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
