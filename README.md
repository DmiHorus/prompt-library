# Prompt Library

A team-grade prompt library managed as code. Prompts are stored as YAML cards with metadata, versioning, and CI validation.

## Quick Start

1. Browse prompts in `prompts/categories/`
2. Use the YAML card template in `prompts/templates/card_template.yaml`
3. Read the [contribution guide](docs/contribution_guide.md) before adding new prompts

## Structure

```
prompts/
  categories/       # prompts grouped by domain
  templates/         # base YAML card template
  variants/          # A/B and experimental versions
examples/            # synthetic input/output samples
docs/                # documentation and taxonomy
tests/               # test cases for prompts
scripts/             # validation and utility scripts
```

## Documentation

- [Taxonomy](docs/taxonomy.md) — categories, tags, naming rules
- [Contribution Guide](docs/contribution_guide.md) — how to add/edit prompts
- [README (detailed)](docs/README.md) — full library documentation

## CI

Every PR is validated automatically:
- YAML lint
- Required card fields check
- Secret pattern detection
