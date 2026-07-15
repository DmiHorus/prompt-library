"""Place prompt cards in the repository and run validation."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from .card_builder import card_to_yaml
from .config import CATEGORIES_DIR, VALIDATOR_SCRIPT, resolve_repo_root


def _load_validator(repo_root: Path):
    """Dynamically import validate_card from validate_cards.py."""
    validator_path = repo_root / VALIDATOR_SCRIPT
    spec = importlib.util.spec_from_file_location("validate_cards", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load validator: {validator_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_card


def resolve_target_path(repo_root: Path, category: str, filename: str) -> Path:
    """Return the full path for a new card file."""
    return repo_root / CATEGORIES_DIR / category / filename


def check_existing(path: Path) -> str | None:
    """Return a warning message if the target file already exists."""
    if path.exists():
        return (
            f"File already exists: {path}\n"
            "Consider bumping version or using a different action_detail suffix."
        )
    return None


def save_card(
    repo_root: Path,
    category: str,
    filename: str,
    card: dict[str, Any],
    dry_run: bool = False,
) -> Path:
    """Write card to disk or print in dry-run mode."""
    target_dir = repo_root / CATEGORIES_DIR / category
    target_path = target_dir / filename
    yaml_text = card_to_yaml(card)

    if dry_run:
        print("\n--- YAML Card Preview ---")
        print(yaml_text)
        print(f"👀 Dry run — would save to: {target_path.relative_to(repo_root)}")
        return target_path

    target_dir.mkdir(parents=True, exist_ok=True)
    warning = check_existing(target_path)
    if warning:
        print(f"⚠️  {warning}")

    target_path.write_text(yaml_text, encoding="utf-8")
    print(f"✅ Card created: {target_path.relative_to(repo_root)}")
    return target_path


def run_validation(repo_root: Path, card_path: Path, dry_run: bool = False) -> list[str]:
    """Validate a single card file using validate_cards.py logic."""
    if dry_run:
        return []

    validate_card = _load_validator(repo_root)
    errors = validate_card(card_path)
    if errors:
        print("\n⚠️  Validator reported issues (file saved anyway):")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"✓ Validation passed: {card_path.relative_to(repo_root)}")
    return errors


def place_card(
    card: dict[str, Any],
    filename: str,
    repo_root: str | None = None,
    dry_run: bool = False,
) -> tuple[Path, list[str]]:
    """Save card and run validation."""
    root = resolve_repo_root(repo_root)
    category = card["category"]
    path = save_card(root, category, filename, card, dry_run=dry_run)
    errors = run_validation(root, path, dry_run=dry_run)
    return path, errors
