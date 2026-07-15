# Руководство по участию

## Чеклист PR

Перед открытием PR проверьте:

- [ ] YAML-карточка содержит все обязательные поля (id, version, owner, category, tags, purpose, model, system, user_template, expected_output_format).
- [ ] `id` соответствует шаблону `category.action_detail` (например, `payments.partial_refund`).
- [ ] `version` соответствует semver (например, `"1.0.0"`).
- [ ] Нет реальных секретов, токенов, PII или внутренних URL — только плейсхолдеры вроде `{{order_id}}`.
- [ ] Имя файла соответствует шаблону `{category}_{action}_{detail}.yaml`.
- [ ] В описании PR есть пример входа и выхода.
- [ ] В YAML-карточку добавлена запись в `changelog`.

## Сообщения коммитов

Следуйте [Conventional Commits](https://www.conventionalcommits.org/):

- `feat(prompts): add partial refund prompt for payments`
- `fix(prompts): clarify output format in rag query rewrite`
- `docs: update taxonomy with new code_review category`
- `chore(ci): add secret detection step`

## Именование веток

- Новый промпт: `feature/add-{category}-{name}`
- Редактирование промпта: `fix/{category}-{name}-{what}`
- Документация: `docs/{what}`

## Ревью

У каждого промпта есть поле `owner`. Этот человек — обязательный ревьюер изменений своего промпта.
