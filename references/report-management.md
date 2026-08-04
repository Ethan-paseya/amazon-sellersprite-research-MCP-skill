# Report Management

## Output Directories

Recommended:

```text
reports/{ASIN}_{SITE}_{YYYYMMDD}/
category-reports/{CATEGORY}_{SITE}_{YYYYMMDD}/
keyword-reports/{ASIN}_{SITE}_{YYYYMMDD}/
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/
product-research-reports/{PRODUCT_KEYWORD}_{SITE}_{YYYYMMDD}/
product-planning-reports/{ASIN1}_{ASIN2}_{ASIN3}_{SITE}_{YYYYMMDD}/
```

## Common Files

```text
{REPORT_TITLE}.md
raw/
data.json
dashboard.html
{REPORT_TITLE}.xlsx
assumptions.md
```

Not every skill needs every file. Markdown is the baseline deliverable.

## Markdown Preservation

Markdown is the authoritative report and must always be preserved.

Rules:

- Generate Markdown before Excel.
- Do not delete Markdown after Excel conversion.
- Do not overwrite Markdown with Excel content.
- Return Markdown path in the final response.
- If Excel is generated, return both paths.
- If Excel is generated, include a `MCP原始数据` worksheet containing the raw MCP evidence used by the report, with secrets and local paths redacted.

## Naming

Use the report title for every user-facing final filename. The Markdown first-level heading must be `# {REPORT_TITLE}`, and the `.md` or `.xlsx` filename stem must be exactly `{REPORT_TITLE}`.

Command patterns:

```text
{BRAND} {SHORT_PRODUCT_NAME} Listing 全维度穿透分析报告.md
{CATEGORY} {SITE} 品类自动化选品分析报告.md
{ASIN} {BRAND} {SHORT_PRODUCT_NAME} 关键词调研报告.md
{ASIN} {BRAND} {SHORT_PRODUCT_NAME} 用户评论 VOC 深度分析报告.md
{PRODUCT_DIRECTION} {SITE} 选品深度调研报告.md
{PRODUCT_DIRECTION} {SITE} 产品立项企划.md
```

When Listing identity fields are absent, use the ASIN or sanitized user input as the fallback identity. Never use `report.md`, `analysis.md`, or `final.md` for the main report.

## Public Repository Policy

Commit only:

- templates;
- sanitized sample schemas;
- scripts;
- docs;
- empty output directories with README or `.gitkeep`.

Do not commit:

- raw API output;
- generated real reports;
- private Excel reports;
- API keys;
- encrypted local secrets.
