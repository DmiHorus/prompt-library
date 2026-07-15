# Библиотека промптов

Командная библиотека промптов, управляемая как код. Промпты хранятся в виде YAML-карточек с метаданными, версионированием и проверкой в CI.

**Репозиторий:** https://github.com/DmiHorus/prompt-library  
**Рабочий каталог:** `~/PyCharmMiscProject/M61`

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
# Валидация всех карточек
python scripts/validate_cards.py

# Рефакторинг личного промпта (предпросмотр)
python scripts/refactor_prompt.py \
  --input RAW_prompt/my_prompt.md \
  --owner "@you" \
  --category requirements_engineering \
  --dry-run

# Запись карточки в prompts/categories/
python scripts/refactor_prompt.py \
  --input RAW_prompt/my_prompt.md \
  --owner "@you"
```

## Каталог промптов

| ID | Категория | Назначение |
|----|-----------|------------|
| `payments.partial_refund` | payments | Сообщение клиенту о частичном возврате с ссылкой на чек |
| `rag.query_rewrite` | rag | Переписывание запроса пользователя для векторного поиска |
| `requirements_engineering.user_input_to_fr` | requirements_engineering | Преобразование интервью/стенограммы в FR/NFR и артефакты для ТЗ |

Примеры входа/выхода — в `examples/<category>/`.

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
| `--stdin` | Читать промпт из stdin |
| `--owner @handle` | Владелец карточки (**обязательный**) |
| `--model MODEL` | Целевая модель в карточке (default: `gpt-4o`) |
| `--category NAME` | Категория или `auto` (default: `auto`) |
| `--mode draft\|production` | Режим рефакторинга (default: `production`) |
| `--dry-run` | Показать карточку, не записывая файл |
| `--env-file PATH` | Альтернативный путь к `.env` |
| `--repo-root PATH` | Корень репозитория (default: автоопределение) |

Без `--input` и `--stdin` — интерактивный режим (двойной Enter или Ctrl+D для завершения).

## Структура проекта

```
M61/
  .env                          # OPENAI_API_KEY (не коммитится)
  requirements.txt              # зависимости Python
  RAW_prompt/                   # исходные черновики промптов
  prompts/
    categories/                 # YAML-карточки по доменам
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
  tests/
  .github/workflows/            # CI
```

## Категории

| Категория | Описание |
|-----------|----------|
| `payments` | Возвраты, чеки, фискальные документы |
| `rag` | Индексация, переписывание запросов, генерация ответов |
| `transcription` | Заметки со встреч, action items, саммари |
| `product_requirements` | PRD, feature briefs, спецификации |
| `code_review` | Чеклисты ревью, саммари PR, обратная связь |
| `requirements_engineering` | Формальный анализ требований (FR/NFR, допущения, риски) для ТЗ по ISO 29148, BABOK, ГОСТ 34.602 |

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
