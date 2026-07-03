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
- `traffic_keyword`: traffic keywords for the ASIN.
- `traffic_extend`: competitor and keyword exposure context.
- `review`: positive and negative review samples.

Do not store raw credentials in request examples.

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

## 5. Cross Validation

Run a lightweight eval harness when keys and network access are available:

- deterministic checks: price, rating, ranking, keyword metrics;
- Gemini or another LLM judge;
- GLM or another secondary judge;
- final verdict: `PASS`, `WARN`, `FAIL`, or `NEEDS_HUMAN_REVIEW`.

If model calls are unavailable, write a manual validation summary instead.
