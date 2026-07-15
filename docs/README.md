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
