---
name: product-planning
description: Amazon product initiation planning workflow using SellerSprite MCP evidence, existing research reports, cost assumptions, and launch targets. Use when the user runs `/product-planning "{PRODUCT_IDEA}" {SITE}` or asks for 产品立项企划、企划表、上架企划、成本试算、销售计划, or to turn product/category/keyword research into a reusable product planning document or Excel workbook.
---

# Product Planning

## Command

```text
/product-planning "{PRODUCT_IDEA}" {SITE}
```

## Goal

Create a decision-ready product initiation plan that connects market evidence, competitor gaps, product definition, cost feasibility, and launch plan.

## Core Rules

- Use MCP data, existing report data, cost assumptions, or clearly labeled manual assumptions as evidence.
- Do not invent market, keyword, review, sales, or cost data.
- Preserve source Markdown/research files when converting into a planning workbook.
- Separate evidence, assumptions, calculations, and final decisions.
- If Excel is generated, include raw or compact source data sheets needed for audit.
- Do not include API keys, MCP URLs with real secret keys, local absolute paths, supplier private quotes, or unreleased private cost data in public examples.

## Credential Preflight

Before any data or validation call, read `references/runtime-credential-preflight.md` when it is available.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before planning evidence collection.
- If Gemini/GLM validation is part of the requested output and model keys are missing, ask for the missing keys before validation.
- Do not continue with mock MCP data, fabricated market evidence, or fake model validation.
- Do not write provided keys into reports, workbooks, assumptions files, raw files, examples, or the open-source repository.

## Required Reference

Read `references/planning-workflow.md` before creating a planning output.
Read bundled `references/sellersprite-mcp-api.md` before collecting SellerSprite data when it is available.
Use `templates/product-planning-report.zh.md` and `templates/product-planning-workbook-layout.md` as repo-level output templates when they are available.

Normalize `GB` to SellerSprite MCP `UK` before tool calls.

## MCP Evidence Calls

- Market/category: `product_node`, `market_research`, `market_research_statistics`, `market_product_demand_trend`, `market_price_distribution`, `market_rating_distribution`, concentration and distribution tools.
- Competitor/products: `product_research`, `competitor_lookup`, `asin_detail`, `asin_sales_trend`.
- Keyword/traffic: `keyword_miner`, `keyword_research`, `keyword_research_trends`, `traffic_keyword_stat`, `traffic_keyword`, `traffic_source`, `traffic_extend`, `traffic_listing`.
- Review/VOC: `review` with positive and negative `starList` groups.
- Trend/IP checks: `google_trend`, `trademark_country_list`, `trademark_list`, `trademark_stats`, `trademark_detail` when relevant.

Cost, MOQ, supplier feasibility, packaging, freight, refund rate, and inventory assumptions must come from user-provided data, existing local files, or clearly labeled scenario assumptions. Do not fabricate them from general knowledge.

## Workflow

1. Parse product idea, site, target launch market, and available source files.
2. Build an evidence inventory from SellerSprite MCP, existing reports, keyword data, review/VOC data, and cost inputs.
3. Define the intended product: price positioning, customer group, functions, unmet needs, material, packaging, style, target cost, target selling price, target margin, launch month, and first batch.
4. Analyze the market: sales trend, seasonality, listing age, rating/review barriers, price bands, brand concentration, and keyword trend.
5. Tear down representative competitors: listing selling points, positive review keywords, negative pain points, and benchmark direction.
6. Build SWOT with evidence-backed S/W/O/T.
7. Build ABA/keyword table: search volume, purchase volume, product count, average price, PPC, supply-demand ratio, click concentration, rank, and strategic note.
8. Run cost and price scenarios: procurement cost, dimensions, gross/chargeable weight, platform fees, FBA/fulfillment, first-leg freight, refund rate, ad ratio, gross margin, and gross profit.
9. Create a first-three-month sales plan: units, revenue, profit, margin, price stage, launch stage, and monitoring metrics.
10. Output a go/hold/reject decision with P0/P1/P2 actions and validation thresholds.

If MCP has no suitable interface for a needed evidence point, mark the data gap first, then use a browser/crawler fallback only for that missing item and label it separately from MCP evidence.

## Output

Save under:

```text
product-planning-reports/{PRODUCT_IDEA}_{SITE}_{YYYYMMDD}/
├── report.md
├── planning.xlsx
├── assumptions.md
└── raw/
```

Use Chinese for user-facing reports unless the user asks otherwise.
