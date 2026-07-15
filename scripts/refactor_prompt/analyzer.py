"""Claude API analysis and CLEAR refactoring."""

from __future__ import annotations

import json
import os
import re
from typing import Any

import anthropic

from .config import ANTHROPIC_MODEL, KNOWN_CATEGORIES, MAX_TOKENS
from .prompts import (
    build_analysis_system_prompt,
    build_analysis_user_prompt,
    build_refactor_system_prompt,
    build_refactor_user_prompt,
)


class AnalyzerError(Exception):
    """Raised when analysis or refactoring fails."""


def ensure_api_key() -> str:
    """Return API key or raise AnalyzerError with setup instructions."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise AnalyzerError(
            "ANTHROPIC_API_KEY is not set.\n"
            "Export your key: export ANTHROPIC_API_KEY='sk-ant-...'"
        )
    return api_key


def _ensure_api_key() -> str:
    return ensure_api_key()


def _extract_json(text: str) -> dict[str, Any]:
    """Parse JSON from model response, stripping optional markdown fences."""
    cleaned = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    return json.loads(cleaned)


def _call_claude(client: anthropic.Anthropic, system: str, user: str) -> str:
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    parts = [block.text for block in message.content if block.type == "text"]
    return "".join(parts)


def _call_with_json_retry(client: anthropic.Anthropic, system: str, user: str) -> dict[str, Any]:
    raw = _call_claude(client, system, user)
    try:
        return _extract_json(raw)
    except json.JSONDecodeError:
        raw_retry = _call_claude(
            client,
            system + "\n\nYour previous response was not valid JSON. Return ONLY valid JSON.",
            user,
        )
        try:
            return _extract_json(raw_retry)
        except json.JSONDecodeError as exc:
            raise AnalyzerError(
                "Claude API returned non-JSON after retry.\n\nRaw response:\n" + raw_retry
            ) from exc


def analyze_prompt(
    raw_prompt: str,
    category: str = "auto",
) -> dict[str, Any]:
    """Call 1: classify prompt and assess CLEAR."""
    client = anthropic.Anthropic(api_key=_ensure_api_key())
    category_hint = None if category == "auto" else category
    system = build_analysis_system_prompt(KNOWN_CATEGORIES)
    user = build_analysis_user_prompt(raw_prompt, category_hint)
    return _call_with_json_retry(client, system, user)


def refactor_prompt(
    raw_prompt: str,
    analysis: dict[str, Any],
    mode: str = "production",
    target_model: str = "claude",
) -> dict[str, Any]:
    """Call 2: refactor prompt using CLEAR methodology."""
    client = anthropic.Anthropic(api_key=_ensure_api_key())
    system = build_refactor_system_prompt()
    user = build_refactor_user_prompt(raw_prompt, analysis, mode, target_model)
    return _call_with_json_retry(client, system, user)
