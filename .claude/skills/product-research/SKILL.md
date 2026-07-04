---
name: product-research
description: Amazon product opportunity research using SellerSprite MCP and LLM reasoning. Use when the user runs `/product-research "{PRODUCT_KEYWORD}" {SITE}` to research a product direction, evaluate market opportunity, competitors, VOC, barriers, and launch decision.
---

# Product Research

## Command

```text
/product-research "{PRODUCT_KEYWORD}" {SITE}
```

## Goal

Evaluate a product opportunity and produce a decision-ready research report.

## Credential Preflight

Before any data call, read `references/runtime-credential-preflight.md` when it is available.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before product research.
- If Gemini/GLM validation is part of the requested output and model keys are missing, ask for the missing keys before validation.
- Do not continue with mock MCP data or fabricated opportunity conclusions.
- Do not write provided keys into reports, raw files, dashboards, examples, or the open-source repository.

## Required Reference

Read `references/sellersprite-mcp-api.md` before execution when it is available.
Normalize `GB` to SellerSprite MCP `UK` before tool calls.

## Data Calls

- `product_node`: map the product direction to relevant Amazon category nodes.
- `product_research`: collect candidate products and opportunity-filtered samples.
- `competitor_lookup`: compare representative products by keyword, ASIN, brand, seller, node, month, and variation setting.
- `market_research` and `market_research_statistics`: quantify category market size and competition.
- `market_price_distribution`, `market_rating_distribution`, `market_product_demand_trend`: check pricing, maturity, and demand trend.
- `market_product_concentration`, `market_brand_concentration`, `market_seller_concentration`: quantify head concentration.
- `keyword_miner`, `keyword_research`, `keyword_research_trends`: validate keyword demand, CPC/PPC, purchase rate, supply-demand ratio, and trend.
- `traffic_listing`, `traffic_source`, `traffic_extend`: inspect traffic patterns for representative competitors when available.
- `review`: collect VOC from representative ASINs.
- `google_trend`: optional external demand validation.
- `trademark_country_list`, `trademark_list`, `trademark_stats`, `trademark_detail`: use only for naming/IP/trademark risk checks.

If MCP cannot answer a required question, mark the gap and then use a crawl/browser fallback only for that missing evidence.

## Workflow

1. Clarify product keyword and site.
2. Normalize site code for SellerSprite MCP.
3. Collect representative products using `product_research` and `competitor_lookup`.
4. Collect keyword, category, market distribution, and traffic context from MCP.
5. Save raw or compact MCP responses before reasoning.
6. Label product attributes: price, rating, reviews, feature, material, scenario.
7. Compare opportunity patterns with evidence references.
8. Analyze VOC and barriers using review/category/trademark evidence or labeled assumptions.
9. Output decision: enter, observe, or reject.

## Research Dimensions

| Dimension | Questions |
|---|---|
| Demand | Is there enough search and sales demand? |
| Competition | Are review moats and brands too strong? |
| Differentiation | Can the product be meaningfully improved? |
| Profit | Is price/CPC/return risk acceptable? |
| Supply chain | Is production feasible? |
| Launch path | What keywords and segments should be tested first? |

Do not invent supply-chain, patent, compatibility, seasonality, inventory, or certification risks. Use MCP data first, then existing user files, then explicitly labeled assumptions or crawl evidence.

## Output

Save under:

```text
product-research-reports/{PRODUCT_KEYWORD}_{SITE}_{YYYYMMDD}/report.md
```

Do not publish raw product exports or private cost assumptions.
