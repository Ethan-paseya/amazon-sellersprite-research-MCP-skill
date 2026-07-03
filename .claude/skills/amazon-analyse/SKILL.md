---
name: amazon-analyse
description: Amazon single-product analysis workflow. Use when the user runs `/amazon-analyse {ASIN} {SITE}` to collect SellerSprite MCP data, produce a Markdown product analysis report, optionally export a product-manager meeting Excel workbook, and run data validation without exposing secrets.
---

# Amazon Analyse

## Command

```text
/amazon-analyse {ASIN} {SITE}
```

## Core Rules

- Always create and preserve the Markdown report.
- Excel is optional and must never replace the Markdown report.
- Do not print, store, or commit API keys.
- Do not include raw secrets in generated reports.
- Keep filenames aligned with the report title when possible.
- Store raw data separately from final reports.

## Data Provider

Use SellerSprite MCP or a compatible marketplace data source.

Load the MCP endpoint from environment variables or `.mcp.json`:

```text
SELLERSPRITE_MCP_URL=https://mcp.sellersprite.com/mcp?secret-key=YOUR_KEY
```

Never hard-code a real MCP URL or secret key.

## Recommended Data Calls

- `asin_detail`: product metadata.
- `asin_sales_trend`: sales, revenue, and price trend.
- `traffic_keyword`: ASIN traffic keywords.
- `traffic_extend`: keyword and competitor traffic context.
- `review`: positive and negative review samples.

See `references/sellersprite-mcp-api.md` for schemas.

## Markdown Report Flow

1. Parse ASIN and site.
2. Collect data.
3. Save raw responses under a report-specific directory.
4. Generate a Chinese Markdown report.
5. Add a final data validation section.
6. Save the Markdown report before any Excel conversion step.

## Data Validation

Append a section named:

```text
Gemini Eval Harness 数据验证
```

Check:

- price/rating/review count/rank consistency;
- sales and keyword metric consistency;
- source and data-gap transparency;
- reasoning reliability;
- risk completeness;
- actionability of P0/P1/P2 recommendations.

When Gemini/GLM keys and network are available, use them as judges. Otherwise write `未执行真实调用` and include a manual validation summary.

## Optional Excel Output Prompt

After the Markdown report has been saved, ask:

```text
是否需要转换为Excel表格输出？
```

Offer:

- `需要`: create an additional Excel workbook using the meeting workbook layout.
- `不需要`: stop after Markdown and return the Markdown path.

Hard rule:

- Always preserve the Markdown report regardless of whether Excel conversion is requested.
- If Excel is generated, return both paths: Markdown report and Excel workbook.

## Excel Workbook Layout

Use `templates/excel-workbook-layout.md` as the layout reference.

Recommended sheets:

- `会议摘要`
- `产品基础信息`
- `销售趋势`
- `关键词布局`
- `评论VOC`
- `竞争策略`
- `数据来源`

Prefer conservative `.xlsx` generation. If direct chart XML editing is unreliable, use in-cell bars and styled tables instead of chart objects.
