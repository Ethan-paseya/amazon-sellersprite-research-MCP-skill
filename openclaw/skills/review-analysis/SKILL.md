---
name: review-analysis
description: Amazon review and VOC analysis using SellerSprite MCP. Use when the user runs `/review-analysis {ASIN} {SITE}` to analyze positive and negative reviews, identify product pain points, listing mismatch, service risks, and product improvement actions.
---

# Review Analysis

## Command

```text
/review-analysis {ASIN} {SITE}
```

## Goal

Turn review data into product decisions: what users love, why users complain, and what should be fixed first.

## Credential Preflight

Before any data call, read `{baseDir}/references/runtime-credential-preflight.md`.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before review analysis.
- If Gemini/GLM validation is part of the requested output and model keys are missing, ask for the missing keys before validation.
- Do not continue with mock reviews or fabricated VOC conclusions.
- Do not write provided keys into reports, raw files, examples, or the open-source repository.

## Required Reference

Read `{baseDir}/references/sellersprite-mcp-api.md` before execution.
Normalize `GB` to SellerSprite MCP `UK` before tool calls.

## Data Calls

- `asin_detail`: product context.
- `review` with `starList: [4,5]`: positive reviews. Use pagination and record sample size.
- `review` with `starList: [1,2,3]`: negative reviews. Use pagination and record sample size.
- Optional `review` filters: `typeList` for image/video/VP/vine reviews, `startTimestamp`, `endTimestamp`, `page`, `size`, and `returnFields`.
- `asin_sales_trend` and `traffic_keyword`: optional context for whether VOC issues correlate with sales or keyword expectation gaps.
- `keepa_info`: optional price/rank history context when available.

Save raw or compact review responses before summarization. Do not quote large review dumps in public reports; aggregate themes and keep customer-identifying data out.

## Analysis Dimensions

| Dimension | What to Identify |
|---|---|
| Product defect | broken parts, durability, failure |
| Design/function gap | usability, missing function, poor fit |
| Material/appearance | smell, scratches, color, texture |
| Description mismatch | expectation gap from title/images/bullets |
| Service/logistics | used item, missing parts, late delivery |
| Return risk | high-friction issues likely to cause returns |

Only mark an issue as a confirmed pain point when it appears in MCP review evidence or an existing user-provided source. Otherwise label it as a hypothesis.

## Output

Save under:

```text
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/report.md
```

Do not publish raw review dumps or customer-identifying data.
