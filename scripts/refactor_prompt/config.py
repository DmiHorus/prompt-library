"""Configuration constants for the prompt refactoring tool."""

import os
from pathlib import Path

CATEGORIES_DIR = "prompts/categories"
TEMPLATES_DIR = "prompts/templates"
CARD_TEMPLATE = "prompts/templates/card_template.yaml"
VALIDATOR_SCRIPT = "scripts/validate_cards.py"
DEFAULT_MODEL = "gpt-4o"
OPENAI_MODEL = "gpt-4o"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
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


def detect_repo_root() -> Path:
    """Detect repository root from module location or current working directory."""
    module_root = Path(__file__).resolve().parents[2]
    if (module_root / CATEGORIES_DIR).is_dir():
        return module_root

    cwd = Path.cwd().resolve()
    if (cwd / CATEGORIES_DIR).is_dir():
        return cwd

    return module_root


DEFAULT_REPO_ROOT = detect_repo_root()


def load_env_file(path: Path | str | None) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ if not already set."""
    if path is None:
        return

    env_path = Path(path).expanduser()
    if not env_path.is_file():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        os.environ.setdefault(key, value)


def ensure_api_key() -> str:
    """Return OpenAI API key or raise with setup instructions."""
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"{OPENAI_API_KEY_ENV} is not set.\n"
            f"Add it to {DEFAULT_REPO_ROOT / '.env'} or export {OPENAI_API_KEY_ENV}='sk-...'"
        )
    return api_key


def resolve_repo_root(repo_root: str | None = None) -> Path:
    """Expand and resolve the repository root path."""
    if repo_root:
        return Path(repo_root).expanduser().resolve()
    return detect_repo_root()
