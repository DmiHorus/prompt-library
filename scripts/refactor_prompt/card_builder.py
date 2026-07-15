"""Build YAML prompt cards from analyzer output."""

from __future__ import annotations

import re
from typing import Any

import yaml

from .config import CARD_FIELD_ORDER, DEFAULT_MODEL


def _slugify_action_detail(action_detail: str) -> str:
    slug = action_detail.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "refactored_prompt"


def build_card(
    analysis: dict[str, Any],
    refactor: dict[str, Any],
    owner: str,
    model: str = DEFAULT_MODEL,
    category_override: str | None = None,
) -> tuple[dict[str, Any], str]:
    """
    Merge analysis and refactor JSON into a card dict.

    Returns (card_dict, filename).
    """
    category = category_override or analysis.get("category", "general")
    category = re.sub(r"[^a-z0-9_]", "_", str(category).lower()).strip("_")

    action_detail = _slugify_action_detail(
        str(refactor.get("action_detail", "refactored_prompt"))
    )

    card_id = f"{category}.{action_detail}"
    filename = f"{category}_{action_detail}.yaml"

    purpose = refactor.get("purpose") or analysis.get("purpose", "")
    tags = refactor.get("tags") or analysis.get("tags", [])
    variables = refactor.get("variables") or analysis.get("variables", [])

    card: dict[str, Any] = {
        "id": card_id,
        "version": "1.0.0",
        "owner": owner,
        "category": category,
        "tags": tags,
        "model": model,
        "purpose": purpose,
        "system": refactor.get("system", "").strip(),
        "user_template": refactor.get("user_template", "").strip(),
        "expected_output_format": refactor.get("expected_output_format", "").strip(),
        "variables": variables,
        "tests": refactor.get("tests", []),
        "changelog": "v1.0.0 — Initial version (refactored with CLEAR tool).",
    }

    ordered = {key: card[key] for key in CARD_FIELD_ORDER}
    return ordered, filename


def card_to_yaml(card: dict[str, Any]) -> str:
    """Serialize card dict to YAML with stable field order."""
    return yaml.dump(
        card,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )
