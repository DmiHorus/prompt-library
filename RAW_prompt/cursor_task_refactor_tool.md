# Задание: спроектировать и написать Python CLI-скрипт для рефакторинга персональных промптов в командные по методике CLEAR

## Контекст

У меня есть Git-репозиторий `~/projects/prompt-library` с командной библиотекой промптов. Структура:

```
prompt-library/
  prompts/
    categories/
      payments/
      rag/
      transcription/
      product_requirements/
      code_review/
    templates/
      card_template.yaml      # шаблон YAML-карточки
    variants/
  examples/
  docs/
    taxonomy.md               # список категорий и тегов
  scripts/
    validate_cards.py          # валидатор карточек (уже есть)
```

Формат карточки промпта — YAML с обязательными полями:
`id`, `version`, `owner`, `category`, `tags`, `purpose`, `model`, `system`, `user_template`, `expected_output_format`, `variables`, `tests`, `changelog`.

Мне нужен CLI-инструмент, который принимает сырой персональный промпт (свободный текст), прогоняет его через Claude API по методике CLEAR, и на выходе создаёт готовую YAML-карточку в нужной папке репозитория.

## Что такое CLEAR (обязательно учесть в логике рефакторинга)

- **Concise** — цель фиксируется в 1–2 предложениях, убирается размытость и вода.
- **Logical** — задаётся повторяемый порядок шагов, уменьшается фактор случайности.
- **Explicit** — указывается точный формат выхода (JSON, Markdown, таблица), даётся схема и примеры.
- **Adaptive** — один шаблон работает для разных режимов (draft/production) через переменные.
- **Reflective** — встроенный контроль качества: самопроверка, чек-лист, критерии успеха.

Скрипт должен превращать расплывчатый личный промпт в структурированный командный артефакт, пригодный для повторного использования другими людьми.

## Требования к скрипту

### Архитектура

Скрипт должен быть модульным. Раздели на файлы:

```
scripts/
  refactor_prompt/
    __init__.py
    cli.py            # точка входа, argparse
    analyzer.py       # вызов Claude API для анализа и рефакторинга
    card_builder.py   # сборка YAML-карточки из ответа LLM
    repo_placer.py    # определение папки, запись файла, вызов валидатора
    prompts.py        # системные и пользовательские промпты для Claude API
    config.py         # настройки: пути, модель, обязательные поля
```

Дополнительно создай `scripts/refactor_prompt.py` — однофайловый entry point:

```python
#!/usr/bin/env python3
"""Entry point: python scripts/refactor_prompt.py ..."""
from refactor_prompt.cli import main
main()
```

### CLI интерфейс (`cli.py`)

```
python scripts/refactor_prompt.py \
  --input "raw_prompt.txt"       # файл с сырым промптом (или --stdin)
  --owner "@vadim"               # владелец (обязательный)
  --model "claude"               # целевая модель промпта (default: claude)
  --category "auto"              # категория: auto = LLM определит, или явно задать
  --mode "production"            # режим: draft | production (default: production)
  --dry-run                      # показать карточку, но не записывать в файл
  --repo-root "~/projects/prompt-library"  # корень репозитория (default)
```

Также поддержи `--stdin` для пайпа: `cat my_prompt.txt | python scripts/refactor_prompt.py --stdin --owner "@vadim"`.

Также поддержи интерактивный режим: если `--input` и `--stdin` не указаны, попроси пользователя вставить промпт в терминал (мультистрочный ввод, завершение по Ctrl+D или пустой строке дважды).

### Модуль анализа (`analyzer.py`)

Используй Anthropic Python SDK (`anthropic`). Ключ API берётся из переменной окружения `ANTHROPIC_API_KEY`.

Рефакторинг выполняется в **два вызова Claude API**:

**Вызов 1 — Анализ и классификация:**
- Вход: сырой промпт.
- Задача: определить категорию (из существующих в `taxonomy.md` или предложить новую), предложить теги, сформулировать `purpose` в одно предложение, выделить переменные части промпта.
- Выход: JSON с полями `category`, `tags`, `purpose`, `variables`, `clear_assessment` (оценка по каждой букве CLEAR: что уже хорошо, что нужно исправить).

**Вызов 2 — Рефакторинг по CLEAR:**
- Вход: сырой промпт + результат анализа из вызова 1.
- Задача: переписать промпт в командный формат по CLEAR. Разделить на `system` и `user_template`. Вынести переменные в плейсхолдеры `{{var}}`. Добавить `expected_output_format`. Сгенерировать тест-кейсы.
- Выход: JSON со всеми полями YAML-карточки.

Для обоих вызовов: `model="claude-sonnet-4-20250514"`, `max_tokens=4096`, ответ строго JSON (попроси в system prompt отвечать ТОЛЬКО валидным JSON без маркдауна и преамбул).

### Модуль промптов для Claude API (`prompts.py`)

Вынеси все системные и пользовательские промпты в отдельный файл как константы. Это позволит итерировать над ними отдельно. Промпты должны быть на английском (это промпты для LLM, не для пользователя).

Системный промпт для вызова 1 должен содержать:
- Роль: "You are a prompt engineering analyst."
- Задачу: классифицировать промпт, оценить по CLEAR.
- Список существующих категорий (передаётся динамически из `taxonomy.md` или `config.py`).
- Формат выхода: строгий JSON-schema.

Системный промпт для вызова 2 должен содержать:
- Роль: "You are a prompt refactoring engineer."
- Полное описание CLEAR (все 5 принципов с критериями).
- Инструкцию: разделить на system/user_template, вынести переменные, задать формат выхода, написать тесты.
- Формат выхода: строгий JSON-schema, совпадающий с полями YAML-карточки.

### Модуль сборки карточки (`card_builder.py`)

- Принимает JSON из analyzer, собирает полную YAML-карточку.
- Генерирует `id` по паттерну `{category}.{action_detail}` из purpose.
- Ставит `version: "1.0.0"`.
- Генерирует имя файла по паттерну `{category}_{action_detail}.yaml`.
- Сериализует в YAML через `yaml.dump` с `default_flow_style=False`, `allow_unicode=True`, `sort_keys=False` (порядок полей должен совпадать с шаблоном).

### Модуль размещения (`repo_placer.py`)

- Определяет целевую папку: `prompts/categories/{category}/`.
- Если папки нет — создаёт её.
- Проверяет, нет ли файла с таким же именем (если есть — предупреди и предложи bump версии или суффикс).
- Записывает файл.
- Запускает `validate_cards.py` на новом файле и показывает результат.
- Если `--dry-run` — только печатает YAML в stdout и путь, куда бы записал.

### Модуль конфигурации (`config.py`)

```python
DEFAULT_REPO_ROOT = "~/projects/prompt-library"
CATEGORIES_DIR = "prompts/categories"
TEMPLATES_DIR = "prompts/templates"
CARD_TEMPLATE = "prompts/templates/card_template.yaml"
VALIDATOR_SCRIPT = "scripts/validate_cards.py"
DEFAULT_MODEL = "claude"
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
REQUIRED_FIELDS = [
    "id", "version", "owner", "category", "tags",
    "purpose", "model", "system", "user_template",
    "expected_output_format", "variables", "tests", "changelog",
]
KNOWN_CATEGORIES = [
    "payments", "rag", "transcription",
    "product_requirements", "code_review",
]
```

### Обработка ошибок

- Если `ANTHROPIC_API_KEY` не задан — понятное сообщение с инструкцией.
- Если Claude API вернул не-JSON — retry один раз. Если повторно не-JSON — показать сырой ответ и завершить с ошибкой.
- Если валидатор нашёл ошибки — показать их, но файл всё равно сохранить (с предупреждением).

### Зависимости

Добавь файл `scripts/refactor_prompt/requirements.txt`:

```
anthropic>=0.42.0
pyyaml>=6.0
```

### UX в терминале

- Показывай прогресс: `⏳ Analyzing prompt...`, `⏳ Refactoring with CLEAR...`, `✅ Card created: prompts/categories/payments/payments_partial_refund.yaml`.
- После создания карточки выведи краткий отчёт:

```
📋 CLEAR Assessment:
  Concise:    ✅ Purpose condensed to 1 sentence
  Logical:    ✅ 4 sequential steps defined
  Explicit:   ✅ Output format: Markdown, 30-60 words
  Adaptive:   ⚠️  No mode variable added (single use case)
  Reflective: ✅ 3 test cases generated

📁 Saved: prompts/categories/payments/payments_partial_refund.yaml
🏷  Tags: refund, partial, customer-support
🔖 Version: 1.0.0
```

- В `--dry-run` режиме вместо `📁 Saved` покажи `👀 Dry run — would save to: ...`.

---

## Ограничения

- Python 3.11+.
- Никаких фреймворков типа click, typer, rich — только stdlib (`argparse`, `pathlib`, `json`, `textwrap`) + `anthropic` + `pyyaml`.
- Никаких реальных API-ключей и токенов в коде. Только `os.environ["ANTHROPIC_API_KEY"]`.
- Все строки и комментарии в коде — на английском. CLI-вывод для пользователя — на английском.

## Результат

После выполнения у меня должны быть:
1. Все файлы модуля `scripts/refactor_prompt/` в репозитории `~/projects/prompt-library`.
2. Entry point `scripts/refactor_prompt.py`.
3. `requirements.txt` внутри модуля.
4. Файлы должны быть рабочими: `python scripts/refactor_prompt.py --help` должен показать справку.
5. Закоммить с сообщением: `feat(scripts): add CLEAR-based prompt refactoring CLI tool`.
6. Запушить в remote.

---

## Тест (выполни после написания кода)

Создай файл `test_prompt.txt` в корне репозитория с содержимым:

```
Ты — ассистент. Когда я даю тебе текст баг-репорта, ты должен написать краткое описание бага для Jira. Напиши заголовок, описание, шаги воспроизведения и ожидаемое поведение. Если баг критичный — пометь это.
```

Запусти: `python scripts/refactor_prompt.py --input test_prompt.txt --owner "@vadim" --dry-run`

Убедись, что:
- Скрипт отработал без ошибок.
- Вывел YAML-карточку с заполненными полями.
- Определил категорию (ожидаемо: `code_review` или предложил новую, напр. `bug_reports`).
- CLEAR assessment показал оценку по каждому пункту.

После теста удали `test_prompt.txt` и закоммить, если были правки.
