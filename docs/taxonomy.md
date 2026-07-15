# Таксономия

## Категории

| Категория                  | Папка                                  | Описание |
|----------------------------|----------------------------------------|----------|
| payments                   | `categories/payments/`                 | Возвраты, холды, чеки, фискальные документы |
| rag                        | `categories/rag/`                      | Индексация, переписывание запросов, генерация ответов |
| transcription              | `categories/transcription/`            | Заметки со встреч, action items, саммари |
| product_requirements       | `categories/product_requirements/`     | PRD, feature briefs, спецификации |
| code_review                | `categories/code_review/`              | Чеклисты ревью, саммари PR, обратная связь |
| requirements_engineering   | `categories/requirements_engineering/` | Преобразование сырого ввода от стейкхолдеров (интервью, стенограммы) в структурированные бизнес-/системные требования (BR/UR/FR/NFR), реестры допущений, рисков и открытых вопросов для разделов ТЗ |

`requirements_engineering` отличается от `product_requirements`: последняя категория — для лёгких PRD и feature briefs продуктовых команд, а `requirements_engineering` — для формального анализа требований по стандартам (ISO/IEC/IEEE 29148, BABOK v3, ГОСТ 34.602) с полной трассируемостью, реестрами рисков/допущений и приоритизацией MoSCoW — для детальных технических спецификаций, а не продуктовых брифов.

## Правила именования

- **Файлы:** `{category}_{action}_{detail}.yaml` — только snake_case, ASCII.
- **Версия:** хранится внутри YAML-карточки, НЕ в имени файла.
- **Примеры:** `payments_partial_refund.yaml`, `rag_query_rewrite.yaml`, `requirements_engineering_user_input_to_fr.yaml`.

## Теги

Теги задаются произвольно, но должны следовать существующим соглашениям. Текущие теги:

```bash
grep -rh "tags:" prompts/categories/ | sort -u
```

Распространённые теги: `refund`, `fiscal`, `e-invoice`, `summarization`, `extraction`,
`rewrite`, `meeting`, `action-items`, `prd`, `feature`, `review`, `feedback`,
`requirements`, `functional-requirements`, `non-functional-requirements`,
`business-analysis`, `stakeholder-interview`, `traceability`, `assumptions`,
`hypotheses`, `risk-register`, `open-questions`, `scope`, `moscow`,
`iso-29148`, `babok`, `gost-34602`, `tech-spec`.

## Заметки по категории `requirements_engineering`

Промпты в этой категории обычно длинные многоэтапные system prompts, а не короткие task-шаблоны. При добавлении карточки:

- `purpose` должен называть производимый артефакт (например, «структурированный набор FR/NFR для раздела требований к системе в ТЗ»), а не просто «анализ требований».
- `variables` обычно содержит один большой свободный текстовый вход (сырое интервью/стенограмма/переписка), а не несколько мелких полей — документируйте его как одну переменную `{{source_text}}`.
- `expected_output_format` должен ссылаться на фиксированную структуру разделов, которую задаёт промпт (например, 13 нумерованных Markdown-секций: резюме, границы, бизнес-цели, акторы, FR, NFR, ограничения, допущения, гипотезы, риски, неявные ожидания, открытые вопросы, глоссарий), а не на общее описание формата.
- `tests` должны проверять структурную полноту (все обязательные секции на месте, соблюдена схема ID, каждое допущение/гипотеза/риск связано с требованием или границей scope) в дополнение к качеству содержания.
