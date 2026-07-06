---
name: amazon-analyse
description: Amazon single-product analysis workflow. Use when the user runs `/amazon-analyse {ASIN} {SITE}` to collect marketplace data, produce a Markdown product analysis report, optionally export a product-manager meeting Excel workbook, and run data validation without exposing secrets.
---

# Amazon Analyse

## Command

```text
/amazon-analyse {ASIN} {SITE}
```

Examples:

```text
/amazon-analyse {ASIN} US
```

## Core Rules

- Always create and preserve the Markdown report.
- Excel is optional and must never replace the Markdown report.
- When Excel is generated, include the raw MCP responses used for the report in a dedicated workbook sheet.
- Do not print, store, or commit API keys.
- Do not include raw secrets in generated reports.
- Keep filenames aligned with the report title when possible.
- Store raw data separately from final reports.

## Credential Preflight

Before any data or validation call, read `references/runtime-credential-preflight.md` when it is available.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before data collection.
- If Gemini or GLM credentials are missing, ask for the missing model key before claiming real Gemini/GLM validation.
- Do not continue with mock MCP data or fake model validation.
- Do not write provided keys into reports, raw files, Excel workbooks, templates, examples, or the open-source repository.

## Data Provider

Use SellerSprite MCP or a compatible marketplace data source.

Before collecting data, read the bundled SellerSprite MCP reference when available:

```text
references/sellersprite-mcp-api.md
```

Load the MCP endpoint and key from environment variables, for example:

```text
SELLERSPRITE_API_KEY=YOUR_KEY
SELLERSPRITE_MCP_URL=https://mcp.sellersprite.com/mcp
```

Prefer the official MCP configuration style: clean URL plus a `secret-key` header. Never hard-code the real MCP URL with a key or print the key.

Normalize user input `GB` to SellerSprite MCP `UK` before tool calls.

## Recommended Data Calls

- `asin_detail`: product metadata.
- `asin_sales_trend`: sales, revenue, and price trend.
- `asin_prediction`, `bsr_prediction`, `keepa_info`: forecast/history context when available.
- `asin_coupon_trend` or `asin_detail_with_coupon_trend`: promotion/coupon context when available.
- `traffic_keyword_stat`: ASIN traffic keyword source overview.
- `traffic_keyword`: ASIN traffic keywords.
- `traffic_source`: organic/recommendation/ad traffic source structure.
- `traffic_extend`: keyword and competitor traffic context.
- `traffic_listing`: keyword/listing traffic context when available.
- `keyword_miner`, `keyword_order`, `keyword_research_trends`: keyword demand, ranking, PPC, and trend checks.
- `review`: positive and negative review samples.
- `trademark_list` / `trademark_stats`: only when brand, naming, or IP risk is discussed.

If a needed evidence point is not supported by MCP, mark it as a data gap first. Only then use a browser/crawler fallback and label it as external supplemental data.

## Markdown Report Flow

1. Parse ASIN and site.
2. Normalize site code for SellerSprite MCP.
3. Collect MCP data and save raw or compact responses under a report-specific directory.
4. Build conclusions only from MCP evidence, existing user files, or clearly labeled assumptions.
5. Generate a Chinese Markdown report.
6. Add a final data validation section.
7. Save the Markdown report before any Excel conversion step.

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

After the Markdown report has been saved, ask the user in the chat/front-end response only:

```text
是否需要转换为Excel表格输出？
```

Offer:

- `需要`: create an additional Excel workbook using the meeting workbook layout.
- `不需要`: stop after Markdown and return the Markdown path.

Hard rule:

- Always preserve the Markdown report regardless of whether Excel conversion is requested.
- Do not append this Excel conversion prompt to the Markdown report body. It is a UI/chat prompt, not report content.
- If Excel is generated, return both paths: Markdown report and Excel workbook.
- If Excel is generated, add a `MCP原始数据` sheet that contains the report's raw MCP files or compact raw JSON payloads. Redact secrets, tokens, local absolute paths, and any user-private credentials before writing the sheet.

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
- `MCP原始数据`

Prefer conservative `.xlsx` generation. If direct chart XML editing is unreliable, use in-cell bars and styled tables instead of chart objects.

`MCP原始数据` should be audit-oriented, not decorative. Recommended columns:

- `数据文件/接口`
- `采集时间`
- `记录序号`
- `字段路径`
- `原始值`
- `备注`

Use this sheet to preserve the evidence trail behind the Markdown and meeting views. Keep raw review text compact when it is long, but do not silently drop metric fields that support report conclusions.
