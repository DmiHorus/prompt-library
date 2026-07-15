"""Configuration constants for the prompt refactoring tool."""

from pathlib import Path

DEFAULT_REPO_ROOT = "~/projects/prompt-library"
CATEGORIES_DIR = "prompts/categories"
TEMPLATES_DIR = "prompts/templates"
CARD_TEMPLATE = "prompts/templates/card_template.yaml"
VALIDATOR_SCRIPT = "scripts/validate_cards.py"
DEFAULT_MODEL = "claude"
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096

REQUIRED_FIELDS = [
    "id",
    "version",
    "owner",
    "category",
    "tags",
    "purpose",
    "model",
    "system",
    "user_template",
    "expected_output_format",
    "variables",
    "tests",
    "changelog",
]

CARD_FIELD_ORDER = [
    "id",
    "version",
    "owner",
    "category",
    "tags",
    "model",
    "purpose",
    "system",
    "user_template",
    "expected_output_format",
    "variables",
    "tests",
    "changelog",
]

KNOWN_CATEGORIES = [
    "payments",
    "rag",
    "transcription",
    "product_requirements",
    "code_review",
]


def resolve_repo_root(repo_root: str | None = None) -> Path:
    """Expand and resolve the repository root path."""
    root = Path(repo_root or DEFAULT_REPO_ROOT).expanduser()
    return root.resolve()
