# Таксономия

## Категории

| Категория               | Папка                             | Описание                                              |
|-------------------------|-----------------------------------|-------------------------------------------------------|
| payments                | `categories/payments/`            | Возвраты, холды, чеки, фискальные документы           |
| rag                     | `categories/rag/`                 | Индексация, переписывание запросов, генерация ответов |
| transcription           | `categories/transcription/`       | Заметки со встреч, action items, саммари              |
| product_requirements    | `categories/product_requirements/`| PRD, feature briefs, спецификации                     |
| code_review             | `categories/code_review/`         | Чеклисты ревью, саммари PR, обратная связь            |

## Правила именования

- **Файлы:** `{category}_{action}_{detail}.yaml` — только snake_case, ASCII.
- **Версия:** хранится внутри YAML-карточки, НЕ в имени файла.
- **Примеры:** `payments_partial_refund.yaml`, `rag_query_rewrite.yaml`.

## Теги

Теги задаются произвольно, но должны следовать существующим соглашениям. Текущие теги:

```bash
grep -rh "tags:" prompts/categories/ | sort -u
```

Распространённые теги: `refund`, `fiscal`, `e-invoice`, `summarization`, `extraction`,
`rewrite`, `meeting`, `action-items`, `prd`, `feature`, `review`, `feedback`.
