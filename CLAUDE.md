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
| `product-planning` | `/product-planning "{PRODUCT_IDEA}" {SITE}` |

## Rules

- Never commit real credentials.
- Never include raw marketplace responses in public examples.
- Always preserve Markdown reports.
- Excel output is optional and additional.
- Excel output must include a `MCP原始数据` worksheet with the raw MCP evidence used by the report, after redacting secrets and local paths.
- Product planning output must separate evidence, assumptions, calculations, and decisions.
- Use environment variables or `.mcp.json` for local MCP configuration.
- Prefer the Python toolchain under `scripts/python/` for package checks, sanitization, installation, and GitHub publishing.

## Skill Paths

Use `.claude/skills/*/SKILL.md` for Claude Code style installs.
Use `skills/*/SKILL.md` for generic/Codex style installs.

## Tooling

Recommended cross-platform checks:

```bash
python scripts/python/sellersprite_skill_tools.py check-package
python scripts/python/sellersprite_skill_tools.py test-open-source-skills
python scripts/python/sellersprite_skill_tools.py scan-sensitive
```

## Output Policy

All skills should save a Markdown report first.

For `/amazon-analyse {ASIN} {SITE}` only:

1. collect data;
2. generate and save Markdown;
3. run data validation;
4. ask whether Excel is needed;
5. if yes, generate Excel while preserving Markdown and include the `MCP原始数据` sheet.

For `/product-planning "{PRODUCT_IDEA}" {SITE}` default V1 Excel:

1. use the sheet order `意向产品` → `市场分析` → `竞品分析与优化策略` → `SWOT分析` → `ABA排名【季度】` → `MCP原始数据` → `数据来源`;
2. do not include `成本试算` or `销售计划` unless the user explicitly asks and provides assumptions.
