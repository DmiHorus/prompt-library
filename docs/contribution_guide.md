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
