# Workflow

## 1. Command

```text
/amazon-analyse {ASIN} {SITE}
```

Example:

```text
/amazon-analyse {ASIN} US
```

## 2. Data Collection

Use SellerSprite MCP or a compatible marketplace data provider.

Recommended calls:

- `asin_detail`: product title, brand, price, rating, category, rank.
- `asin_sales_trend`: sales, revenue, price trend.
- `asin_prediction`, `bsr_prediction`, `keepa_info`: forecast/history context when available.
- `asin_coupon_trend` or `asin_detail_with_coupon_trend`: coupon/promotion context when available.
- `traffic_keyword_stat`: ASIN traffic keyword source overview.
- `traffic_keyword`: traffic keywords for the ASIN.
- `traffic_source`: organic/recommendation/ad traffic source structure.
- `traffic_extend`: competitor and keyword exposure context.
- `traffic_listing`: keyword/listing traffic context when available.
- `keyword_miner`, `keyword_order`, `keyword_research_trends`: keyword demand, ranking, PPC, and trend checks.
- `review`: positive and negative review samples.
- `trademark_list` / `trademark_stats`: optional brand/IP risk evidence when relevant.

Do not store raw credentials in request examples.
Normalize `GB` to SellerSprite MCP `UK` before tool calls.
If MCP cannot provide a required evidence point, document the gap first. Use browser/crawler fallback only for that missing evidence and label it separately from MCP evidence.

## 3. Markdown Report

Always generate and preserve a Markdown report first. This report is the authoritative output.

Recommended sections:

- Analysis object
- Product basics
- Sales trend
- Keyword layout
- Review VOC
- Competitive strategy
- Product manager action plan
- Data validation

## 4. Optional Excel Output

After the Markdown report has been saved, ask:

```text
是否需要转换为Excel表格输出？
```

Rules:

- `需要`: create an additional Excel workbook.
- `不需要`: keep only the Markdown report.
- Always preserve the Markdown report.
- Never delete, overwrite, or replace the Markdown report with Excel.
- When Excel is generated, include a `MCP原始数据` worksheet with the raw MCP evidence used by the report after removing API keys, secret-key URLs, tokens, and local absolute paths.

## 5. Cross Validation

Run a lightweight eval harness when keys and network access are available:

- deterministic checks: price, rating, ranking, keyword metrics;
- Gemini or another LLM judge;
- GLM or another secondary judge;
- final verdict: `PASS`, `WARN`, `FAIL`, or `NEEDS_HUMAN_REVIEW`.

If model calls are unavailable, write a manual validation summary instead.
