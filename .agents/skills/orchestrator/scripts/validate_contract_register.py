#!/usr/bin/env python3
"""Validate the canonical material contract register."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from schema_validation import validate as validate_schema
from workflow_common import load_json


def fail(messages: list[str]) -> int:
    print("FAIL")
    for message in messages:
        print(f"- {message}")
    return 1


def validate_register(register: Path, schema_path: Path | None = None) -> list[str]:
    chosen_schema = schema_path or Path(__file__).resolve().parents[1] / "assets/contract-register.schema.json"
    try:
        data = load_json(register)
        schema = load_json(chosen_schema)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    errors = validate_schema(data, schema)
    if errors:
        return errors
    ids = [item.get("id") for item in data.get("contracts", []) if isinstance(item, dict)]
    names = [item.get("name") for item in data.get("contracts", []) if isinstance(item, dict)]
    for values, label in [(ids, "contract id"), (names, "contract name")]:
        for duplicate in sorted({item for item in values if values.count(item) > 1}):
            errors.append(f"duplicate {label}: {duplicate}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("register", type=Path)
    args = parser.parse_args()
    errors = validate_register(args.register)
    if errors:
        return fail(errors)
    data = load_json(args.register)
    print("PASS")
    print("contracts=" + ",".join(str(item.get("id")) for item in data.get("contracts", [])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
