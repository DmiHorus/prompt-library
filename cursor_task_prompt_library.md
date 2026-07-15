# Задание: создать и запушить репозиторий библиотеки промптов в GitHub

## Контекст

Ты — агент-разработчик. Твоя задача — создать локальный Git-репозиторий `prompt-library`, наполнить его файлами по спецификации ниже, создать удалённый репозиторий на GitHub и запушить туда код. Выполняй шаги строго по порядку. Не пропускай ни одного файла. После пуша верни мне ссылку на репозиторий.

## Предусловия

- macOS, zsh, git, gh CLI установлены и авторизованы.
- Перед началом проверь: `gh auth status`. Если не авторизован — останови работу и сообщи.

---

## Шаг 1. Создай локальный репозиторий и структуру папок

```bash
mkdir -p ~/projects/prompt-library && cd ~/projects/prompt-library
git init

mkdir -p prompts/categories/payments
mkdir -p prompts/categories/rag
mkdir -p prompts/categories/transcription
mkdir -p prompts/categories/product_requirements
mkdir -p prompts/categories/code_review
mkdir -p prompts/templates
mkdir -p prompts/variants
mkdir -p examples/payments
mkdir -p docs
mkdir -p tests
mkdir -p scripts
mkdir -p .github/workflows
```

---

## Шаг 2. Создай файл `.gitignore`

Путь: `.gitignore`

```
# Secrets
.env
.env.*
secrets/
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store

# Python
__pycache__/
*.pyc
.venv/
venv/

# Node
node_modules/

# OS
Thumbs.db
```

---

## Шаг 3. Создай файл `LICENSE`

Путь: `LICENSE`

Используй MIT License. В поле year поставь 2025, в поле name — "Prompt Library Contributors".

---

## Шаг 4. Создай корневой `README.md`

Путь: `README.md`

```markdown
# Prompt Library

A team-grade prompt library managed as code. Prompts are stored as YAML cards with metadata, versioning, and CI validation.

## Quick Start

1. Browse prompts in `prompts/categories/`
2. Use the YAML card template in `prompts/templates/card_template.yaml`
3. Read the [contribution guide](docs/contribution_guide.md) before adding new prompts

## Structure

```
prompts/
  categories/       # prompts grouped by domain
  templates/         # base YAML card template
  variants/          # A/B and experimental versions
examples/            # synthetic input/output samples
docs/                # documentation and taxonomy
tests/               # test cases for prompts
scripts/             # validation and utility scripts
```

## Documentation

- [Taxonomy](docs/taxonomy.md) — categories, tags, naming rules
- [Contribution Guide](docs/contribution_guide.md) — how to add/edit prompts
- [README (detailed)](docs/README.md) — full library documentation

## CI

Every PR is validated automatically:
- YAML lint
- Required card fields check
- Secret pattern detection
```

---

## Шаг 5. Создай `docs/README.md`

Путь: `docs/README.md`

```markdown
# Prompt Library — Documentation

## How to find a prompt

1. Go to `prompts/categories/<domain>/`.
2. Each `.yaml` file is a self-contained prompt card with metadata.
3. Use `tags` field for cross-domain search: `grep -r "tags:.*refund" prompts/`.

## How to add a new prompt

1. Copy `prompts/templates/card_template.yaml` into the appropriate category folder.
2. Fill in ALL required fields (see template comments).
3. Add a synthetic example to `examples/<category>/`.
4. Create a feature branch: `git checkout -b feature/add-<category>-<name>`.
5. Commit with Conventional Commits: `feat(prompts): add <name> for <category>`.
6. Open a PR. The prompt `owner` is a required reviewer.

## How to update an existing prompt

1. Create a branch: `git checkout -b fix/<category>-<name>-<what>`.
2. Edit the YAML card. Bump `version` following semver:
   - **Major** (2.0.0): structural/behavioral change, old version incompatible.
   - **Minor** (1.1.0): new variables, added context, backward compatible.
   - **Patch** (1.0.1): typo fixes, wording tweaks.
3. Update `changelog` inside the card.
4. Include before/after output examples in the PR description.
5. Commit: `fix(prompts): <what changed>` or `feat(prompts): <what added>`.

## Versioning

We use semantic versioning inside each YAML card (`version` field).
Git history tracks all changes. Tags are optional for major releases.

## Onboarding

New team members should:
1. Read this document (5 min).
2. Read `docs/taxonomy.md` for category descriptions (3 min).
3. Read `docs/contribution_guide.md` for the PR checklist (2 min).
4. Open any card in `prompts/categories/` to see a real example.
```

---

## Шаг 6. Создай `docs/taxonomy.md`

Путь: `docs/taxonomy.md`

```markdown
# Taxonomy

## Categories

| Category                | Folder                    | Description                                      |
|-------------------------|---------------------------|--------------------------------------------------|
| payments                | `categories/payments/`    | Refunds, holds, receipts, fiscal documents       |
| rag                     | `categories/rag/`         | Ingestion, query rewriting, answer generation     |
| transcription           | `categories/transcription/`| Meeting notes, action items, summaries           |
| product_requirements    | `categories/product_requirements/` | PRDs, feature briefs, specs              |
| code_review             | `categories/code_review/` | Review checklists, PR summaries, feedback         |

## Naming Rules

- **Files:** `{category}_{action}_{detail}.yaml` — all snake_case, ASCII only.
- **Version:** stored inside the YAML card, NOT in the filename.
- **Examples:** `payments_partial_refund.yaml`, `rag_query_rewrite.yaml`.

## Tags

Tags are freeform but should follow existing conventions. Check current tags:

```bash
grep -rh "tags:" prompts/categories/ | sort -u
```

Common tags: `refund`, `fiscal`, `e-invoice`, `summarization`, `extraction`,
`rewrite`, `meeting`, `action-items`, `prd`, `feature`, `review`, `feedback`.
```

---

## Шаг 7. Создай `docs/contribution_guide.md`

Путь: `docs/contribution_guide.md`

```markdown
# Contribution Guide

## PR Checklist

Before opening a PR, verify:

- [ ] YAML card has all required fields (id, version, owner, category, tags, purpose, model, system, user_template, expected_output_format).
- [ ] `id` follows the pattern `category.action_detail` (e.g., `payments.partial_refund`).
- [ ] `version` follows semver (e.g., `"1.0.0"`).
- [ ] No real secrets, tokens, PII, or internal URLs — only placeholders like `{{order_id}}`.
- [ ] Filename matches the pattern `{category}_{action}_{detail}.yaml`.
- [ ] PR description includes example input and output.
- [ ] Changelog entry added inside the YAML card.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(prompts): add partial refund prompt for payments`
- `fix(prompts): clarify output format in rag query rewrite`
- `docs: update taxonomy with new code_review category`
- `chore(ci): add secret detection step`

## Branch Naming

- New prompt: `feature/add-{category}-{name}`
- Edit prompt: `fix/{category}-{name}-{what}`
- Docs: `docs/{what}`

## Reviews

Every prompt has an `owner` field. That person is a required reviewer for changes to their prompt.
```

---

## Шаг 8. Создай шаблон карточки промпта

Путь: `prompts/templates/card_template.yaml`

```yaml
# =============================================================================
# Prompt Card Template
# Copy this file to prompts/categories/<category>/<category>_<action>_<detail>.yaml
# Fill in ALL fields. Remove comments when done.
# =============================================================================

# --- Metadata ---
id: "category.action_detail"           # unique ID, format: category.snake_case_name
version: "1.0.0"                       # semver: major.minor.patch
owner: "@your-github-handle"           # responsible person, required PR reviewer
category: "category_name"              # must match folder name in categories/
tags: [tag1, tag2]                     # freeform, see docs/taxonomy.md
model: "claude"                        # target model: claude, gpt-4o, gigachat, etc.
purpose: "One sentence: what this prompt does and for whom."

# --- Prompt ---
system: |
  System message. Define the role, tone, constraints.
  Be concise. Remove filler words.

user_template: |
  Task: ...
  Input:
    - {{variable_1}}: description
    - {{variable_2}}: description
  Output: ...

# --- Contract ---
expected_output_format: |
  Describe the expected shape: Markdown, JSON, table, N paragraphs, etc.

variables:
  - name: "variable_1"
    description: "What this variable contains"
    example: "example value"
  - name: "variable_2"
    description: "What this variable contains"
    example: "example value"

# --- Quality ---
tests:
  - "Output matches expected format"
  - "No hallucinated data"
  - "Length within bounds"

changelog: |
  v1.0.0 — Initial version.
```

---

## Шаг 9. Создай пример промпта (payments)

Путь: `prompts/categories/payments/payments_partial_refund.yaml`

```yaml
id: "payments.partial_refund"
version: "1.0.0"
owner: "@pm-lead"
category: "payments"
tags: [refund, partial, e-invoice, fiscal, customer-support]
model: "claude"
purpose: "Generate a customer-facing message for a partial refund with e-receipt link."

system: |
  You are a customer support agent for an online store.
  Respond in a polite, concise tone. No bureaucratic language.
  Always include the refund amount, product name, and receipt link.

user_template: |
  A customer is receiving a partial refund. Write a short notification message.

  Product: {{product}}
  Refund amount: {{amount}} {{currency}}
  Reason: {{reason}}
  Receipt: {{receipt_url}}

expected_output_format: |
  A single paragraph, 30-60 words. Includes product name, refund amount, and a clickable receipt link.

variables:
  - name: "product"
    description: "Name of the refunded product"
    example: "Wireless Headphones Pro"
  - name: "amount"
    description: "Refund amount (number)"
    example: "2500"
  - name: "currency"
    description: "Currency code or symbol"
    example: "RUB"
  - name: "reason"
    description: "Reason for the partial refund"
    example: "Damaged packaging"
  - name: "receipt_url"
    description: "URL of the electronic receipt"
    example: "https://store.example.com/receipts/{{receipt_id}}"

tests:
  - "Output is a single paragraph"
  - "Length is 30-60 words"
  - "Contains product name, amount, and receipt link"
  - "Tone is polite, no bureaucratic language"
  - "No PII or real data in output"

changelog: |
  v1.0.0 — Initial version.
```

---

## Шаг 10. Создай пример промпта (rag)

Путь: `prompts/categories/rag/rag_query_rewrite.yaml`

```yaml
id: "rag.query_rewrite"
version: "1.0.0"
owner: "@ml-engineer"
category: "rag"
tags: [query, rewrite, search, retrieval]
model: "claude"
purpose: "Rewrite a vague user query into an optimized search query for vector retrieval."

system: |
  You are a search query optimizer. Your job is to rewrite a user's natural language
  question into a concise, specific query that maximizes relevant document retrieval.
  Remove filler words. Expand abbreviations. Add implicit context when obvious.

user_template: |
  Rewrite the following user question into an optimized search query.

  Original question: {{user_question}}
  Domain context: {{domain}}

  Return ONLY the rewritten query, nothing else.

expected_output_format: |
  A single line: the rewritten search query (5-20 words).

variables:
  - name: "user_question"
    description: "The raw user question"
    example: "how do I do a refund?"
  - name: "domain"
    description: "The knowledge domain for context"
    example: "e-commerce payment processing"

tests:
  - "Output is a single line"
  - "Length is 5-20 words"
  - "No filler words (please, can you, I want to)"
  - "More specific than the original query"

changelog: |
  v1.0.0 — Initial version.
```

---

## Шаг 11. Создай пример входа/выхода

Путь: `examples/payments/partial_refund_example.md`

```markdown
# Example: payments.partial_refund

## Input

```yaml
product: "Wireless Headphones Pro"
amount: 2500
currency: "RUB"
reason: "Damaged packaging"
receipt_url: "https://store.example.com/receipts/R-20250601-0042"
```

## Expected Output

> We've processed a partial refund of 2,500 RUB for your Wireless Headphones Pro
> due to damaged packaging. You can view your updated receipt here:
> https://store.example.com/receipts/R-20250601-0042. Feel free to reach out
> if you have any questions.
```

---

## Шаг 12. Создай скрипт валидации карточек

Путь: `scripts/validate_cards.py`

```python
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
```

Сделай файл исполняемым: `chmod +x scripts/validate_cards.py`

---

## Шаг 13. Создай GitHub Actions workflow

Путь: `.github/workflows/validate.yml`

```yaml
name: Validate Prompt Cards

on:
  pull_request:
    paths:
      - "prompts/**"
      - "examples/**"
  push:
    branches: [main]
    paths:
      - "prompts/**"

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pyyaml yamllint

      - name: YAML lint
        run: |
          find prompts/ -name "*.yaml" -exec yamllint -d relaxed {} +

      - name: Validate prompt cards
        run: python scripts/validate_cards.py

      - name: Check for secrets
        run: |
          PATTERNS='sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36,}|AKIA[0-9A-Z]{16}|BEGIN.PRIVATE.KEY'
          if grep -rEn "$PATTERNS" prompts/ examples/ docs/; then
            echo "::error::Potential secrets found in repository files!"
            exit 1
          fi
          echo "No secrets detected."
```

---

## Шаг 14. Создай remote-репозиторий на GitHub и запуши

```bash
cd ~/projects/prompt-library

git add -A
git commit -m "feat: initial prompt library scaffold

- YAML card template with required fields
- Example prompts: payments_partial_refund, rag_query_rewrite
- CI: yamllint, card validation, secret detection
- Docs: README, taxonomy, contribution guide"

gh repo create prompt-library --private --source=. --remote=origin --push
```

Если `gh repo create` завершился успешно — выведи ссылку на репозиторий в формате:

```
✅ Репозиторий создан: https://github.com/<username>/prompt-library
```

Если произошла ошибка — покажи вывод ошибки и предложи варианты решения.

---

## Шаг 15. Финальная проверка

После пуша выполни:

```bash
python scripts/validate_cards.py
```

Убедись, что оба промпта проходят валидацию без ошибок. Если есть ошибки — исправь, закоммить и запуши.

---

## Итог

После выполнения всех шагов у меня должен быть:

1. Приватный GitHub-репозиторий `prompt-library` со всеми файлами.
2. Ссылка на него.
3. Подтверждение, что `validate_cards.py` прошёл без ошибок.
