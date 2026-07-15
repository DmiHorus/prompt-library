# Библиотека промптов

Командная библиотека промптов, управляемая как код. Промпты хранятся в виде YAML-карточек с метаданными, версионированием и проверкой в CI.

Рабочий каталог проекта — `~/PyCharmMiscProject/M61`.

## Возможности

- **YAML-карточки** — единый формат с полями `id`, `version`, `owner`, `tags`, `system`, `user_template` и др.
- **Валидация** — скрипт проверяет обязательные поля, semver и паттерны секретов.
- **Рефакторинг по CLEAR** — CLI-инструмент превращает личный промпт в командную карточку через OpenAI API.

## Быстрый старт

### 1. Окружение

```bash
cd ~/PyCharmMiscProject/M61
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### 2. API-ключ

Добавьте в `.env` в корне проекта:

```
OPENAI_API_KEY=sk-...
```

Ключ подхватывается автоматически при запуске скриптов.

### 3. Работа с промптами

```bash
# Просмотр и валидация существующих карточек
python scripts/validate_cards.py

# Рефакторинг личного промпта (предпросмотр без записи)
python scripts/refactor_prompt.py \
  --input my_prompt.txt \
  --owner "@you" \
  --dry-run

# Запись карточки в prompts/categories/
python scripts/refactor_prompt.py \
  --input my_prompt.txt \
  --owner "@you"
```

## CLI: refactor_prompt.py

Преобразует свободный текст в YAML-карточку по методике **CLEAR**:

| Принцип | Суть |
|---------|------|
| **C**oncise | Цель в 1–2 предложениях, без воды |
| **L**ogical | Повторяемый порядок шагов |
| **E**xplicit | Точный формат выхода (JSON, Markdown, таблица) |
| **A**daptive | Переменные `{{var}}` для разных сценариев |
| **R**eflective | Тест-кейсы и критерии качества |

### Параметры

| Параметр | Описание |
|----------|----------|
| `--input FILE` | Файл с сырым промптом |
| `--stdin` | Читать промпт из stdin (`cat prompt.txt \| ...`) |
| `--owner @handle` | Владелец карточки (**обязательный**) |
| `--model MODEL` | Целевая модель в карточке (default: `gpt-4o`) |
| `--category NAME` | Категория или `auto` (default: `auto`) |
| `--mode draft\|production` | Режим рефакторинга (default: `production`) |
| `--dry-run` | Показать карточку, не записывая файл |
| `--env-file PATH` | Альтернативный путь к `.env` |
| `--repo-root PATH` | Корень репозитория (default: автоопределение) |

Без `--input` и `--stdin` запускается интерактивный режим: вставьте промпт в терминал, завершите двойным Enter или Ctrl+D.

## Структура проекта

```
M61/
  .env                          # OPENAI_API_KEY и прочие секреты
  requirements.txt              # зависимости Python
  prompts/
    categories/                 # промпты по доменам
      payments/
      rag/
      transcription/
      product_requirements/
      code_review/
      requirements_engineering/
    templates/
      card_template.yaml        # шаблон YAML-карточки
    variants/                   # A/B и экспериментальные версии
  examples/                     # синтетические примеры входа/выхода
  docs/                         # документация и таксономия
  scripts/
    refactor_prompt.py          # CLI: рефакторинг по CLEAR
    validate_cards.py           # валидация YAML-карточек
    refactor_prompt/            # модули CLI-инструмента
  tests/                        # тест-кейсы для промптов
  .github/workflows/            # CI
```

## Категории промптов

| Категория | Описание |
|-----------|----------|
| `payments` | Возвраты, чеки, фискальные документы |
| `rag` | Индексация, переписывание запросов, генерация ответов |
| `transcription` | Заметки со встреч, action items, саммари |
| `product_requirements` | PRD, feature briefs, спецификации |
| `code_review` | Чеклисты ревью, саммари PR, обратная связь |
| `requirements_engineering` | Формальный анализ требований (FR/NFR, допущения, риски) для ТЗ |

Подробнее — в [docs/taxonomy.md](docs/taxonomy.md).

## Документация

- [Таксономия](docs/taxonomy.md) — категории, теги, правила именования
- [Руководство по участию](docs/contribution_guide.md) — чеклист PR, коммиты, ветки
- [README (подробный)](docs/README.md) — полная документация библиотеки

## CI

Каждый PR проверяется автоматически (`.github/workflows/validate.yml`):

- YAML lint
- Проверка обязательных полей карточки
- Поиск паттернов секретов

## Лицензия

MIT — см. [LICENSE](LICENSE).
