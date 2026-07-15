"""OpenAI API analysis and CLEAR refactoring."""

from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

from .config import KNOWN_CATEGORIES, MAX_TOKENS, OPENAI_MODEL, ensure_api_key
from .prompts import (
    build_analysis_system_prompt,
    build_analysis_user_prompt,
    build_refactor_system_prompt,
    build_refactor_user_prompt,
)


class AnalyzerError(Exception):
    """Raised when analysis or refactoring fails."""


def _extract_json(text: str) -> dict[str, Any]:
    """Parse JSON from model response, stripping optional markdown fences."""
    cleaned = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    return json.loads(cleaned)


def _call_openai(client: OpenAI, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    if not content:
        raise AnalyzerError("OpenAI API returned an empty response.")
    return content


def _call_with_json_retry(client: OpenAI, system: str, user: str) -> dict[str, Any]:
    raw = _call_openai(client, system, user)
    try:
        return _extract_json(raw)
    except json.JSONDecodeError:
        raw_retry = _call_openai(
            client,
            system + "\n\nYour previous response was not valid JSON. Return ONLY valid JSON.",
            user,
        )
        try:
            return _extract_json(raw_retry)
        except json.JSONDecodeError as exc:
            raise AnalyzerError(
                "OpenAI API returned non-JSON after retry.\n\nRaw response:\n" + raw_retry
            ) from exc


def analyze_prompt(
    raw_prompt: str,
    category: str = "auto",
) -> dict[str, Any]:
    """Call 1: classify prompt and assess CLEAR."""
    client = OpenAI(api_key=ensure_api_key())
    category_hint = None if category == "auto" else category
    system = build_analysis_system_prompt(KNOWN_CATEGORIES)
    user = build_analysis_user_prompt(raw_prompt, category_hint)
    return _call_with_json_retry(client, system, user)


def refactor_prompt(
    raw_prompt: str,
    analysis: dict[str, Any],
    mode: str = "production",
    target_model: str = "gpt-4o",
) -> dict[str, Any]:
    """Call 2: refactor prompt using CLEAR methodology."""
    client = OpenAI(api_key=ensure_api_key())
    system = build_refactor_system_prompt()
    user = build_refactor_user_prompt(raw_prompt, analysis, mode, target_model)
    return _call_with_json_retry(client, system, user)
