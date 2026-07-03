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

## Data Calls

- `asin_detail`: product context.
- `review` with `starList: [4,5]`: positive reviews.
- `review` with `starList: [1,2,3]`: negative reviews.

## Analysis Dimensions

| Dimension | What to Identify |
|---|---|
| Product defect | broken parts, durability, failure |
| Design/function gap | usability, missing function, poor fit |
| Material/appearance | smell, scratches, color, texture |
| Description mismatch | expectation gap from title/images/bullets |
| Service/logistics | used item, missing parts, late delivery |
| Return risk | high-friction issues likely to cause returns |

## Output

Save under:

```text
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/report.md
```

Do not publish raw review dumps or customer-identifying data.
