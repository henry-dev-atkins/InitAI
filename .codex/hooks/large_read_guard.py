#!/usr/bin/env python3
"""Deny oversized, model-visible reads from the main context."""

from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


class UnsafeRead(RuntimeError):
    """The command names a read that cannot be checked safely."""


DEFAULT_PROTECTED_PATTERNS = (
    "AGENTS.md",
    "**/AGENTS.md",
    "AI_SPACE/SPEC.md",
    "AI_SPACE/TODO.md",
    "AI_SPACE/AI_LEARNINGS_LOG.md",
    "AI_SPACE/sessions/**",
    "AI_SPACE/handovers/**",
    ".agents/skills/**",
    ".agents/workflow/**",
    ".codex/**",
)
READ_COMMANDS = {"cat", "gc", "get-content", "head", "less", "more", "tail", "type"}
WRAPPERS = {"bash", "sh", "zsh", "powershell", "powershell.exe", "pwsh", "pwsh.exe", "cmd", "cmd.exe"}
PREFIXES = {"env", "exec", "command", "builtin", "nohup"}
TARGETED = {"grep", "rg", "select-string", "measure-object", "wc"}
TOKEN_RE = re.compile(r'''"(?:\\.|[^"\\])*"|'(?:[^']|'')*'|&&|\|\||\d?(?:>>?|<)|[;|]|[^\s;|<>]+''')


@dataclass(frozen=True)
class Settings:
    line_threshold: int
    byte_threshold: int
    protected_patterns: tuple[str, ...] = DEFAULT_PROTECTED_PATTERNS


@dataclass(frozen=True)
class Finding:
    path: str
    size_bytes: int
    line_count: int | None
    aggregate: bool = False
    operand_count: int = 1


def clean(value: str) -> str:
    value = value.strip().rstrip(",")
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        value = value[1:-1]
    return value


def name(value: str) -> str:
    return Path(clean(value).replace("\\", "/")).name.lower()


def tokens(command: str) -> list[str]:
    return TOKEN_RE.findall(command.replace("\r\n", "\n").replace("\n", ";"))


def statements(values: list[str]) -> list[list[str]]:
    result, current = [], []
    for value in values:
        if value in {";", "&&", "||"}:
            if current:
                result.append(current)
                current = []
        else:
            current.append(value)
    if current:
        result.append(current)
    return result


def stages(values: list[str]) -> list[list[str]]:
    result, current = [], []
    for value in values:
        if value == "|":
            if current:
                result.append(current)
                current = []
        else:
            current.append(value)
    if current:
        result.append(current)
    return result


def command_position(stage: list[str]) -> int:
    for index, value in enumerate(stage):
        value = clean(value)
        if not value or value in {"(", ")", "{", "}", "&"} or value in PREFIXES:
            continue
        if value.startswith("-") or ("=" in value and not value.startswith(("./", ".\\"))):
            continue
        return index
    raise UnsafeRead("read command has no executable")


def stage_command(stage: list[str]) -> tuple[str, list[str]]:
    start = command_position(stage)
    args, index = [], start + 1
    while index < len(stage):
        if stage[index] in {">", ">>", "1>", "1>>", "2>", "2>>", "<", "0<"}:
            if index + 1 >= len(stage):
                raise UnsafeRead("redirection has no static target")
            index += 2
            continue
        args.append(stage[index])
        index += 1
    return name(stage[start]), args


def wrapper_command(stage: list[str]) -> str | None:
    command, args = stage_command(stage)
    if command not in WRAPPERS:
        return None
    for index, arg in enumerate(args):
        option = clean(arg).lower()
        if command in {"bash", "sh", "zsh"} and option.startswith("-") and "c" in option[1:]:
            if index + 1 < len(args):
                return clean(" ".join(args[index + 1 :]))
        if command in {"powershell", "powershell.exe", "pwsh", "pwsh.exe"} and option in {"-c", "-command"}:
            if index + 1 < len(args):
                return clean(" ".join(args[index + 1 :]))
        if command in {"cmd", "cmd.exe"} and option in {"/c", "/k"}:
            if index + 1 < len(args):
                return clean(" ".join(args[index + 1 :]))
    return None


def variants(command: str) -> list[str]:
    result, pending = [], [command]
    while pending:
        current = pending.pop(0)
        if current in result:
            continue
        result.append(current)
        for statement in statements(tokens(current)):
            for stage in stages(statement):
                nested = wrapper_command(stage)
                if nested:
                    pending.append(nested)
    return result


def redirect_is_safe(stage: list[str]) -> bool | None:
    target = None
    for index, value in enumerate(stage):
        if value in {">", ">>", "1>", "1>>"}:
            if index + 1 >= len(stage):
                raise UnsafeRead("stdout redirection has no target")
            target = clean(stage[index + 1]).lower().replace("\\", "/")
    if target is None:
        return None
    visible = {"&1", "&2", "/dev/stdout", "/dev/stderr", "/dev/fd/1", "/dev/fd/2", "/dev/tty", "con", "conout$"}
    if not target or target in visible or any(marker in target for marker in ("$", "`", ">(")):
        return False
    return True


def integer(value: str) -> int | None:
    value = clean(value)
    return int(value) if re.fullmatch(r"\d+", value) else None


def option_value(args: list[str], names: set[str]) -> int | None:
    for index, raw in enumerate(args):
        value = clean(raw).lower()
        for option in names:
            if value == option and index + 1 < len(args):
                return integer(args[index + 1])
            if value.startswith(option + ":") or value.startswith(option + "="):
                return integer(value.split(":", 1)[-1].split("=", 1)[-1])
    for raw in args:
        value = clean(raw)
        if re.fullmatch(r"-\d+", value) and ("-n" in names or "-last" in names):
            return int(value[1:])
    return None


def has_option(args: list[str], names: set[str]) -> bool:
    return any(
        clean(arg).lower() in names
        or any(clean(arg).lower().startswith(n + ":") or clean(arg).lower().startswith(n + "=") for n in names)
        for arg in args
    )


def paths_for(command: str, args: list[str]) -> list[tuple[str, bool]]:
    result: list[tuple[str, bool]] = []
    positional = True
    path_flags = {"-path": False, "-literalpath": True}
    value_flags = {"-n", "--lines", "-first", "-head", "-last", "-tail", "-totalcount", "-raw", "-wait", "-delimiter", "-encoding", "-readcount", "-asbytestream", "-force"}
    index = 0
    while index < len(args):
        raw, value = args[index], clean(args[index])
        lower = value.lower()
        if re.fullmatch(r"-\d+", value):
            index += 1
            continue
        if lower == "--":
            positional = True
            index += 1
            continue
        matched = next((flag for flag in path_flags if lower == flag or lower.startswith(flag + ":") or lower.startswith(flag + "=")), None)
        if matched:
            if lower == matched:
                if index + 1 >= len(args):
                    raise UnsafeRead(f"{command} path option has no value")
                result.append((clean(args[index + 1]), path_flags[matched]))
                index += 2
            else:
                result.append((value.split(":", 1)[-1].split("=", 1)[-1], path_flags[matched]))
                index += 1
            continue
        if lower in value_flags or any(lower.startswith(flag + ":") or lower.startswith(flag + "=") for flag in value_flags):
            if lower in value_flags and lower not in {"-raw", "-wait", "-force", "-asbytestream"}:
                index += 2
            else:
                index += 1
            continue
        if positional and not value.startswith("-"):
            result.append((value, False))
        index += 1
    return result


def selection(command: str, args: list[str], settings: Settings) -> int | None:
    if command in {"cat", "gc", "get-content", "less", "more", "type"}:
        if command in {"gc", "get-content"}:
            if has_option(args, {"-wait", "-raw", "-asbytestream", "-delimiter", "-readcount"}) or has_option(args, {"-encoding:byte", "-encoding=byte"}):
                return None
            return option_value(args, {"-first", "-head", "-totalcount", "-last", "-tail"})
        return None
    if command in {"head", "tail"}:
        if command == "tail" and (has_option(args, {"-f", "-F", "--follow"}) or any(clean(a).lower().startswith("--follow=") for a in args)):
            return None
        if has_option(args, {"-z", "--zero-terminated"}):
            return None
        return option_value(args, {"-n", "--lines", "-first", "-last"})
    if command == "sed":
        if has_option(args, {"-z", "-zn", "--null-data"}):
            return None
        scripts = [clean(a) for a in args if re.search(r"\d", clean(a)) and ("p" in clean(a) or "," in clean(a))]
        if not scripts or any(re.search(r"(?:^|,)\s*(?:[1-9]\d*)?\s*\$", script) for script in scripts):
            return None
        ranges = re.findall(r"(\d+)(?:,(\d+))?p", " ".join(scripts))
        return max([int(end or start) for start, end in ranges], default=None)
    return None


def protected(relative: str, settings: Settings) -> bool:
    relative = relative.replace("\\", "/")
    while relative.startswith("./"):
        relative = relative[2:]
    return any(fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(relative, pattern.replace("**/", "")) for pattern in settings.protected_patterns)


def resolve(raw: str, literal: bool, root: Path) -> list[Path]:
    raw = clean(raw)
    if not raw or raw in {"-", ".", ".."} or any(marker in raw for marker in ("$", "`", "$(", "%")):
        raise UnsafeRead(f"read path is dynamic or missing: {raw!r}")
    candidate = Path(raw) if Path(raw).is_absolute() else root / raw
    matches = [candidate] if literal else [Path(value) for value in glob.glob(str(candidate), recursive=True)]
    if not matches:
        raise UnsafeRead(f"read path does not exist: {raw}")
    checked = []
    for path in matches:
        resolved = path.resolve(strict=False)
        if root.resolve() not in resolved.parents and resolved != root.resolve():
            raise UnsafeRead(f"read path is outside the repository: {raw}")
        if path.is_symlink() and (path.resolve() != resolved or not resolved.exists()):
            raise UnsafeRead(f"read path is an unsafe symlink: {raw}")
        if not path.is_file():
            raise UnsafeRead(f"read path is not a file: {raw}")
        checked.append(path)
    return checked


def measure(path: Path, root: Path, settings: Settings, limit: int | None) -> tuple[int, int | None]:
    relative = path.relative_to(root).as_posix()
    if protected(relative, settings):
        return 0, 0
    try:
        data = path.read_bytes()
    except OSError as error:
        raise UnsafeRead(f"cannot measure read path {relative}: {error}") from error
    if limit is None:
        return len(data), data.count(b"\n")
    lines = data.splitlines(keepends=True)
    chosen = lines[:limit]
    return sum(map(len, chosen)), len(chosen)


def visible_bound(stage_list: list[list[str]], index: int, settings: Settings) -> int | None:
    if redirect_is_safe(stage_list[-1]) is True:
        return 0
    if index == len(stage_list) - 1:
        return None
    tail = stage_list[-1]
    command, args = stage_command(tail)
    if command in {"head", "tail"}:
        return option_value(args, {"-n", "--lines", "-first", "-last"})
    if command == "select-object":
        return option_value(args, {"-first", "-last"})
    if command in {"measure-object", "wc"}:
        return 0
    return None


def find_large_reads(command: str, cwd: Path, root: Path, settings: Settings) -> list[Finding]:
    findings: list[Finding] = []
    for variant in variants(command):
        for statement in statements(tokens(variant)):
            stage_list = stages(statement)
            for index, stage in enumerate(stage_list):
                command_name, args = stage_command(stage)
                if command_name not in READ_COMMANDS and command_name != "sed":
                    continue
                operands = paths_for(command_name, args)
                if not operands:
                    if index > 0:
                        continue
                    raise UnsafeRead(f"{command_name} has no static file operand")
                limit = selection(command_name, args, settings)
                streaming = (command_name == "tail" and has_option(args, {"-f", "-F", "--follow"})) or (command_name in {"gc", "get-content"} and has_option(args, {"-wait"}))
                downstream = visible_bound(stage_list, index, settings)
                if downstream == 0:
                    continue
                if downstream is not None and limit is None:
                    limit = downstream
                resolved = [path for raw, literal in operands for path in resolve(raw, literal, root)]
                total_bytes = total_lines = 0
                reported: list[tuple[Path, int, int | None]] = []
                for path in resolved:
                    size, lines = measure(path, root, settings, limit)
                    if size == 0 and lines == 0 and protected(path.relative_to(root).as_posix(), settings):
                        continue
                    total_bytes += size
                    total_lines = None if total_lines is None or lines is None else total_lines + lines
                    reported.append((path, size, lines))
                aggregate = len(resolved) > 1
                if aggregate and (total_bytes > settings.byte_threshold or (total_lines is not None and total_lines > settings.line_threshold)):
                    findings.append(Finding(resolved[0].relative_to(root).as_posix(), total_bytes, total_lines, True, len(resolved)))
                elif streaming and reported:
                    findings.append(Finding(reported[0][0].relative_to(root).as_posix(), reported[0][1], reported[0][2]))
                elif limit is None:
                    findings.extend(Finding(path.relative_to(root).as_posix(), size, lines) for path, size, lines in reported if size > settings.byte_threshold or (lines is not None and lines > settings.line_threshold))
                elif any(size > settings.byte_threshold or (lines is not None and lines > settings.line_threshold) for _, size, lines in reported):
                    findings.extend(Finding(path.relative_to(root).as_posix(), size, lines) for path, size, lines in reported if size > settings.byte_threshold or (lines is not None and lines > settings.line_threshold))
    unique: dict[tuple[str, int, int | None, bool], Finding] = {}
    for finding in findings:
        unique[(finding.path, finding.size_bytes, finding.line_count, finding.aggregate)] = finding
    return list(unique.values())


def hook_output(findings: list[Finding]) -> dict[str, object]:
    paths = ", ".join(f"{item.path} ({item.size_bytes} bytes)" for item in findings[:8])
    reason = f"Large read blocked. Route it through bulk-reader or inspect bounded ranges. Files: {paths}"
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--line-threshold", type=int, required=True)
    parser.add_argument("--byte-threshold", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict) or event.get("hook_event_name") != "PreToolUse" or event.get("tool_name") != "Bash":
            raise UnsafeRead("hook input is missing the required PreToolUse Bash fields")
        tool_input = event.get("tool_input")
        command = tool_input.get("command") if isinstance(tool_input, dict) else None
        if not isinstance(command, str):
            raise UnsafeRead("hook input requires canonical tool_input.command")
        cwd = Path(event.get("cwd", ".")).resolve()
        findings = find_large_reads(command, cwd, cwd, Settings(args.line_threshold, args.byte_threshold))
        if findings:
            print(json.dumps(hook_output(findings), separators=(",", ":")))
        return 0
    except (json.JSONDecodeError, OSError, UnsafeRead, ValueError) as error:
        print(f"large_read_guard: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
