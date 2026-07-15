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
