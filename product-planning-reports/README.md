# Product Planning Reports

Runtime output directory for `/product-planning "{ASIN1;ASIN2;ASIN3}" {SITE}`.

Do not commit real generated planning reports, raw MCP exports, supplier quotes, private cost assumptions, or launch plans to public repositories.

Recommended runtime structure:

```text
product-planning-reports/{ASIN1}_{ASIN2}_{ASIN3}_{SITE}_{YYYYMMDD}/
├── report.md
├── planning.xlsx
├── assumptions.md
└── raw/
```
