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

## Workflow

1. Clarify product keyword and site.
2. Collect representative products using `product_research`.
3. Collect keyword and category context when available.
4. Label product attributes: price, rating, reviews, feature, material, scenario.
5. Compare opportunity patterns.
6. Analyze VOC and barriers.
7. Output decision: enter, observe, or reject.

## Research Dimensions

| Dimension | Questions |
|---|---|
| Demand | Is there enough search and sales demand? |
| Competition | Are review moats and brands too strong? |
| Differentiation | Can the product be meaningfully improved? |
| Profit | Is price/CPC/return risk acceptable? |
| Supply chain | Is production feasible? |
| Launch path | What keywords and segments should be tested first? |

## Output

Save under:

```text
product-research-reports/{PRODUCT_KEYWORD}_{SITE}_{YYYYMMDD}/report.md
```

Do not publish raw product exports or private cost assumptions.
