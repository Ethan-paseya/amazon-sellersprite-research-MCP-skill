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
report.md
raw/
data.json
dashboard.html
optional_excel.xlsx
planning.xlsx
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

Prefer the report title for final filenames.

Fallback:

```text
{ASIN}_{SITE}_product_analysis_{YYYYMMDD}.md
{ASIN}_{SITE}_meeting_workbook_{YYYYMMDD}.xlsx
{CATEGORY}_{SITE}_category_report_{YYYYMMDD}.md
{PRODUCT_KEYWORD}_{SITE}_research_{YYYYMMDD}.md
```

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
