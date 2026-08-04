# Commands

## 1. Listing Analysis

```text
/amazon-analyse {ASIN} {SITE}
```

Purpose:

- collect SellerSprite MCP listing data;
- produce a Markdown report;
- run data validation;
- optionally produce product-manager meeting Excel.

Output:

```text
reports/{ASIN}_{SITE}_{YYYYMMDD}/{BRAND} {SHORT_PRODUCT_NAME} Listing 全维度穿透分析报告.md
```

## 2. Category Selection

```text
/category-select "{CATEGORY}" {SITE}
```

Purpose:

- evaluate full category opportunity;
- score market size, growth, competition, barriers, and margin;
- produce enter/observe/reject recommendation.

Output:

```text
category-reports/{CATEGORY}_{SITE}_{YYYYMMDD}/{CATEGORY} {SITE} 品类自动化选品分析报告.md
```

## 3. Keyword Research

```text
/keyword-research {ASIN} {SITE}
```

Purpose:

- collect keyword library;
- classify terms into 8 dimensions;
- produce listing and ad strategy.

Output:

```text
keyword-reports/{ASIN}_{SITE}_{YYYYMMDD}/
└── {ASIN} {BRAND} {SHORT_PRODUCT_NAME} 关键词调研报告.md
```

## 4. Review Analysis

```text
/review-analysis {ASIN} {SITE}
```

Purpose:

- analyze positive and negative reviews;
- identify product pain points and return risk;
- produce improvement and listing correction actions.

Output:

```text
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/{ASIN} {BRAND} {SHORT_PRODUCT_NAME} 用户评论 VOC 深度分析报告.md
```

## 5. Product Research

```text
/product-research "{PRODUCT_KEYWORD}" {SITE}
```

Purpose:

- research a product direction;
- compare representative products;
- evaluate demand, competition, differentiation, profit, and launch path.

Output:

```text
product-research-reports/{PRODUCT_KEYWORD}_{SITE}_{YYYYMMDD}/{PRODUCT_DIRECTION} {SITE} 选品深度调研报告.md
```

## 6. Product Planning

```text
/product-planning "{ASIN1;ASIN2;ASIN3}" {SITE}
```

Purpose:

- validate three seed competitors, then infer a product direction and turn the evidence into a product initiation plan;
- define intended product, market evidence, competitor gaps, SWOT, ABA/keyword logic, MCP source data, and data-source traceability;
- produce reusable Markdown and optional V1 Excel planning workbook;
- exclude `成本试算` and `销售计划` by default unless the user explicitly asks for financial planning and provides assumptions.

Output:

```text
product-planning-reports/{ASIN1}_{ASIN2}_{ASIN3}_{SITE}_{YYYYMMDD}/
├── {PRODUCT_DIRECTION} {SITE} 产品立项企划.md
└── {PRODUCT_DIRECTION} {SITE} 产品立项企划.xlsx
```

For every command, the first-level report heading and the main report filename must use the same `REPORT_TITLE`. Generic main-report filenames such as `report.md`, `analysis.md`, and `final.md` are not allowed.
