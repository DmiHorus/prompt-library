"""System and user prompts for the LLM API calls."""

from __future__ import annotations

ANALYSIS_JSON_SCHEMA = """{
  "category": "string — one of known categories or a proposed new snake_case category",
  "tags": ["string"],
  "purpose": "string — one sentence describing what the prompt does and for whom",
  "variables": [
    {
      "name": "string — snake_case placeholder name without braces",
      "description": "string",
      "example": "string"
    }
  ],
  "clear_assessment": {
    "concise": {"status": "ok|warning|missing", "note": "string"},
    "logical": {"status": "ok|warning|missing", "note": "string"},
    "explicit": {"status": "ok|warning|missing", "note": "string"},
    "adaptive": {"status": "ok|warning|missing", "note": "string"},
    "reflective": {"status": "ok|warning|missing", "note": "string"}
  }
}"""

REFACTOR_JSON_SCHEMA = """{
  "action_detail": "string — snake_case action detail for id/file naming, e.g. jira_bug_summary",
  "purpose": "string — refined one-sentence purpose",
  "tags": ["string"],
  "system": "string — system message for the team prompt",
  "user_template": "string — user template with {{variable}} placeholders",
  "expected_output_format": "string — exact output shape, length, structure",
  "variables": [
    {
      "name": "string",
      "description": "string",
      "example": "string"
    }
  ],
  "tests": ["string — acceptance criteria / self-check items"],
  "clear_report": {
    "concise": "string — one-line result after refactoring",
    "logical": "string",
    "explicit": "string",
    "adaptive": "string",
    "reflective": "string"
  }
}"""


def build_analysis_system_prompt(categories: list[str]) -> str:
    """Build the system prompt for call 1 (analysis and classification)."""
    category_list = ", ".join(categories)
    return f"""You are a prompt engineering analyst.

Your task is to analyze a raw personal prompt and classify it for a team prompt library.

Known categories: {category_list}

If the prompt does not fit any known category, propose a new snake_case category name
that would fit docs/taxonomy.md conventions.

Evaluate the raw prompt against CLEAR:
- Concise: Is the goal stated in 1-2 sentences without filler?
- Logical: Is there a repeatable step order?
- Explicit: Is the output format specified with schema/examples?
- Adaptive: Can the prompt work across modes via variables?
- Reflective: Are there quality checks, self-review, or success criteria?

Respond with ONLY valid JSON matching this schema (no markdown, no preamble):
{ANALYSIS_JSON_SCHEMA}"""


def build_analysis_user_prompt(raw_prompt: str, category_hint: str | None) -> str:
    """Build the user prompt for call 1."""
    hint = (
        f"\nPreferred category (override auto-detection): {category_hint}"
        if category_hint
        else ""
    )
    return f"""Analyze this raw personal prompt:{hint}

<raw_prompt>
{raw_prompt}
</raw_prompt>"""


def build_refactor_system_prompt() -> str:
    """Build the system prompt for call 2 (CLEAR refactoring)."""
    return f"""You are a prompt refactoring engineer.

Refactor a raw personal prompt into a reusable team-grade prompt card using CLEAR:

1. Concise — Fix purpose to one clear sentence. Remove vagueness and filler.
2. Logical — Define a repeatable sequence of steps in user_template.
3. Explicit — Specify exact output format (Markdown, JSON, table, word count, sections).
4. Adaptive — Use {{{{variable}}}} placeholders for inputs and modes so others can reuse the prompt.
5. Reflective — Add concrete test cases / acceptance criteria for output quality.

Split the refactored prompt into:
- system: role, tone, hard constraints (concise)
- user_template: task, inputs as {{{{var}}}}, step order, output instruction

Extract all dynamic parts into variables with name, description, and example.
Generate 3-5 practical test cases.

Respond with ONLY valid JSON matching this schema (no markdown, no preamble):
{REFACTOR_JSON_SCHEMA}"""


def build_refactor_user_prompt(
    raw_prompt: str,
    analysis: dict,
    mode: str,
    target_model: str,
) -> str:
    """Build the user prompt for call 2."""
    import json

    return f"""Refactor this raw prompt into a team YAML card.

Target prompt model field value: {target_model}
Refactoring mode: {mode}
- production: strict format, full tests, no draft markers
- draft: include {{{{mode}}}} or similar if useful, slightly lighter tests OK

Analysis from prior step:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

<raw_prompt>
{raw_prompt}
</raw_prompt>"""
