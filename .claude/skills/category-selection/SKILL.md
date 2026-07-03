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

## Data Calls

- `product_node`: discover category nodes from category name.
- `market_research_statistics`: collect Top product/category statistics.
- `keyword_miner`: collect category keyword demand when available.
- `product_research`: collect representative products when node data is insufficient.

## Five-Dimension Score

| Dimension | Weight | What to Check |
|---|---:|---|
| Market size | 20 | sales volume, revenue, demand depth |
| Growth potential | 25 | trend, new product opportunity, demand expansion |
| Competition intensity | 20 | review moat, brand concentration, price war |
| Entry barrier | 20 | supply chain, certification, patents, differentiation |
| Margin space | 15 | price band, estimated cost, ad CPC, return risk |

## Output

Save a Markdown report under:

```text
category-reports/{CATEGORY}_{SITE}_{YYYYMMDD}/report.md
```

Do not commit raw SellerSprite responses or real category reports to public repositories.
