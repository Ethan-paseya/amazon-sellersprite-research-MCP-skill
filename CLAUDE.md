# Agent Instructions

This repository contains sanitized Amazon research skills and templates for SellerSprite MCP.

## Skills

| Skill | Command |
|---|---|
| `amazon-analyse` | `/amazon-analyse {ASIN} {SITE}` |
| `category-selection` | `/category-select "{CATEGORY}" {SITE}` |
| `keyword-research` | `/keyword-research {ASIN} {SITE}` |
| `review-analysis` | `/review-analysis {ASIN} {SITE}` |
| `product-research` | `/product-research "{PRODUCT_KEYWORD}" {SITE}` |

## Rules

- Never commit real credentials.
- Never include raw marketplace responses in public examples.
- Always preserve Markdown reports.
- Excel output is optional and additional.
- Use environment variables or `.mcp.json` for local MCP configuration.

## Skill Paths

Use `.claude/skills/*/SKILL.md` for Claude Code style installs.
Use `skills/*/SKILL.md` for generic/Codex style installs.

## Output Policy

All skills should save a Markdown report first.

For `/amazon-analyse {ASIN} {SITE}` only:

1. collect data;
2. generate and save Markdown;
3. run data validation;
4. ask whether Excel is needed;
5. if yes, generate Excel while preserving Markdown.
