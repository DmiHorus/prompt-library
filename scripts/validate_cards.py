#!/usr/bin/env python3
"""Validate prompt YAML cards: required fields, naming, no secrets."""

import sys
import re
from pathlib import Path

import yaml

REQUIRED_FIELDS = [
    "id", "version", "owner", "category", "tags",
    "purpose", "model", "system", "user_template",
    "expected_output_format",
]

SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",
    r"ghp_[a-zA-Z0-9]{36,}",
    r"Bearer\s+[a-zA-Z0-9\-_.]+",
    r"AKIA[0-9A-Z]{16}",
    r"-----BEGIN\s+(RSA\s+)?PRIVATE\sKEY-----",
]

FILENAME_RE = re.compile(r"^[a-z][a-z0-9_]*\.yaml$")


def validate_card(path: Path) -> list[str]:
    errors: list[str] = []

    # Filename check
    if not FILENAME_RE.match(path.name):
        errors.append(f"Filename '{path.name}' violates naming convention (expected snake_case.yaml)")

    # YAML parse
    try:
        with open(path) as f:
            raw = f.read()
            card = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return errors

    if not isinstance(card, dict):
        errors.append("Card root must be a YAML mapping")
        return errors

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in card or not card[field]:
            errors.append(f"Missing or empty required field: '{field}'")

    # Version format
    version = card.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+$", str(version)):
        errors.append(f"Version '{version}' is not valid semver (expected X.Y.Z)")

    # Secret detection
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, raw):
            errors.append(f"Potential secret detected (pattern: {pattern[:20]}...)")

    return errors


def main() -> int:
    cards_dir = Path("prompts/categories")
    if not cards_dir.exists():
        print(f"ERROR: {cards_dir} not found. Run from repo root.")
        return 1

    yaml_files = list(cards_dir.rglob("*.yaml"))
    if not yaml_files:
        print("No YAML cards found.")
        return 0

    total_errors = 0
    for path in sorted(yaml_files):
        errors = validate_card(path)
        if errors:
            print(f"\n✗ {path}")
            for e in errors:
                print(f"  - {e}")
            total_errors += len(errors)
        else:
            print(f"✓ {path}")

    print(f"\n{'='*40}")
    print(f"Files checked: {len(yaml_files)}, Errors: {total_errors}")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
