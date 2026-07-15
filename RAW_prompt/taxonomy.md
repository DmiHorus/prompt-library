# Taxonomy

## Categories

| Category                 | Folder                              | Description                                                                 |
|---------------------------|--------------------------------------|-------------------------------------------------------------------------------|
| payments                  | `categories/payments/`               | Refunds, holds, receipts, fiscal documents                                    |
| rag                       | `categories/rag/`                    | Ingestion, query rewriting, answer generation                                 |
| transcription             | `categories/transcription/`          | Meeting notes, action items, summaries                                        |
| product_requirements      | `categories/product_requirements/`   | PRDs, feature briefs, specs                                                    |
| code_review               | `categories/code_review/`            | Review checklists, PR summaries, feedback                                     |
| requirements_engineering  | `categories/requirements_engineering/` | Turning raw stakeholder input (interviews, transcripts) into structured system/business requirements (BR/UR/FR/NFR), assumptions, risks, and open-question registers for ТЗ-style specs |

`requirements_engineering` is distinct from `product_requirements`: the latter covers lightweight PRDs/feature briefs for product teams, while `requirements_engineering` covers formal, standards-aligned requirements analysis (ISO/IEC/IEEE 29148, BABOK v3, ГОСТ 34.602) with full traceability, risk/assumption registers, and MoSCoW prioritization — used for detailed technical specifications rather than product briefs.

## Naming Rules

- **Files:** `{category}_{action}_{detail}.yaml` — all snake_case, ASCII only.
- **Version:** stored inside the YAML card, NOT in the filename.
- **Examples:** `payments_partial_refund.yaml`, `rag_query_rewrite.yaml`, `requirements_engineering_user_input_to_fr.yaml`.

## Tags

Tags are freeform but should follow existing conventions. Check current tags:

```bash
grep -rh "tags:" prompts/categories/ | sort -u
```

Common tags: `refund`, `fiscal`, `e-invoice`, `summarization`, `extraction`,
`rewrite`, `meeting`, `action-items`, `prd`, `feature`, `review`, `feedback`,
`requirements`, `functional-requirements`, `non-functional-requirements`,
`business-analysis`, `stakeholder-interview`, `traceability`, `assumptions`,
`hypotheses`, `risk-register`, `open-questions`, `scope`, `moscow`,
`iso-29148`, `babok`, `gost-34602`, `tech-spec`.

## Category Notes: `requirements_engineering`

Prompts in this category tend to be long, multi-stage system prompts rather than short task templates. When adding a card here:

- `purpose` should name the artifact produced (e.g., "structured FR/NFR set for a ТЗ system requirements section"), not just "analyze requirements".
- `variables` typically includes one large free-text input (raw interview/transcript/correspondence) rather than several small fields — document it as a single `{{source_text}}` variable in the card.
- `expected_output_format` should reference the fixed section structure the prompt defines (e.g., 13 numbered Markdown sections: summary, scope, business goals, actors, FR, NFR, constraints, assumptions, hypotheses, risks, implicit expectations, open questions, glossary) rather than a generic format description.
- `tests` should check structural completeness (all required sections present, every ID scheme followed, every assumption/hypothesis/risk cross-linked to a requirement or scope item) in addition to content quality.
