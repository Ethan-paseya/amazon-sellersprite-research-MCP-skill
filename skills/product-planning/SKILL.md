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
Read bundled `references/product-planning-mcp-flow.zh.md` before deciding which MCP tools support each planning section.
Use `templates/product-planning-report.zh.md` for Markdown output when available.
Use `templates/product-planning-meeting-workbook-layout.zh.md`, `templates/product_planning_standard_template_V1_manifest.json`, and `templates/product_planning_standard_template_V1.xlsx` as the default Excel meeting workbook template when available.
Use `templates/product-planning-workbook-layout.md` only when the user explicitly asks for a full operating workbook with cost and sales-plan sheets.

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
2. Run credential preflight. Missing SellerSprite key blocks evidence collection; missing Gemini/GLM keys block real double-model validation.
3. Locate category nodes with `product_node`; record selected `nodeIdPath` and any missing category-name fields.
4. Validate keyword demand with `keyword_miner`, `keyword_research`, and `keyword_research_trends` when available.
5. Generate and clean competitor candidates with `competitor_lookup` and `product_research`; filter by title relevance and category node before treating an item as a direct competitor.
6. Pull representative competitor details with `asin_detail`; collect sales trend with `asin_sales_trend` when available.
7. Pull VOC with `review` for selected ASINs, split positive and negative samples when enough data exists.
8. Analyze category maturity and barriers with `market_research_statistics`, `market_product_demand_trend`, `market_price_distribution`, `market_rating_distribution`, `market_brand_concentration`, `market_seller_concentration`, and listing-age distribution tools.
9. Build ABA/traffic table with `keyword_order`, `traffic_keyword_stat`, `traffic_keyword`, `traffic_source`, `aba_research_monthly`, and `aba_research_weekly` where available.
10. Check trend/IP side evidence with `google_trend` and `trademark_*` tools when relevant.
11. Define the intended product: price positioning, customer group, functions, unmet needs, material, packaging, style, target cost, target selling price, target margin, launch month, and first batch.
12. For the default meeting workbook, do not create `成本试算` or `销售计划` sheets. Keep cost, fulfillment, freight, refund, and sales-plan values out of Excel unless the user explicitly asks for financial planning and provides assumptions.
13. In the default meeting workbook, preserve auditability with `MCP原始数据` and `数据来源` sheets placed immediately after `ABA排名【季度】`.
14. Output a go/hold/reject decision with P0/P1/P2 actions, validation thresholds, evidence citations, and a data-gap table.

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

## Default Excel Meeting Template

When the user asks for a reusable meeting-style product-planning Excel workbook, use this sheet order:

1. `意向产品`
2. `市场分析`
3. `竞品分析与优化策略`
4. `SWOT分析`
5. `ABA排名【季度】`
6. `MCP原始数据`
7. `数据来源`

Do not include `成本试算` or `销售计划` in this default meeting template. Add them only as optional sheets after explicit user confirmation and with user-provided assumptions.
