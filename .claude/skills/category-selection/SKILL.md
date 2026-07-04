---
name: category-selection
description: Amazon category opportunity research using SellerSprite MCP. Use when the user runs `/category-select "{CATEGORY}" {SITE}` to evaluate a full category with market size, growth potential, competition, barriers, margin space, and product-entry recommendations.
---

# Category Selection

## Command

```text
/category-select "{CATEGORY}" {SITE}
```

## Goal

Evaluate whether a category is worth entering and identify product-entry angles.

## Credential Preflight

Before any data call, read `references/runtime-credential-preflight.md` when it is available.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before category analysis.
- If Gemini/GLM validation is part of the requested output and model keys are missing, ask for the missing keys before validation.
- Do not continue with mock MCP data or fabricated market conclusions.
- Do not write provided keys into reports, raw files, examples, or the open-source repository.

## Required Reference

Read `references/sellersprite-mcp-api.md` before execution when it is available.
Normalize `GB` to SellerSprite MCP `UK` before tool calls.

## Data Calls

- `product_node`: discover category nodes from category name.
- `market_research_statistics`: collect category summary statistics.
- `market_research`: collect representative category products and sortable metrics.
- `market_product_demand_trend`: check demand trend and seasonality.
- `market_price_distribution`: identify price bands and sales efficiency.
- `market_rating_distribution`: judge maturity and quality-improvement space.
- `market_product_concentration`, `market_brand_concentration`, `market_seller_concentration`: quantify head concentration.
- `market_seller_country_distribution` and `market_seller_type_concentration`: assess seller structure and fulfillment pattern.
- `market_listing_date_distribution`, `market_listing_trend_distribution`, `market_ratings_count_distribution`, `market_ebc_distribution`: assess new-product window, review moat, and listing-content maturity.
- `keyword_research` and `keyword_miner`: collect category/entry keyword demand, CPC/PPC, purchase rate, supply-demand ratio, and click concentration when available.
- `product_research` and `competitor_lookup`: collect representative products when node data is insufficient or when comparing specific entry angles.
- `google_trend`: optional external demand trend validation.

If MCP cannot provide a required dimension, write it as a data gap. Use browser/crawler fallback only after confirming no suitable MCP tool exists, and label it as external supplemental data.

## Five-Dimension Score

| Dimension | Weight | What to Check |
|---|---:|---|
| Market size | 20 | sales volume, revenue, demand depth |
| Growth potential | 25 | trend, new product opportunity, demand expansion |
| Competition intensity | 20 | review moat, brand concentration, price war |
| Entry barrier | 20 | supply chain, certification, patents, differentiation |
| Margin space | 15 | price band, estimated cost, ad CPC, return risk |

Do not score patents, supply chain, compatibility, seasonality, or inventory risk unless there is MCP evidence, user-provided evidence, or explicitly labeled supplemental crawl evidence.

## Output

Save a Markdown report under:

```text
category-reports/{CATEGORY}_{SITE}_{YYYYMMDD}/report.md
```

Do not commit raw SellerSprite responses or real category reports to public repositories.
