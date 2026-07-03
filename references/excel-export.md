# Excel Export Guide

Excel output is optional. It should help product managers run meetings, not replace the Markdown report.

## Required Sheets

| Sheet | Purpose |
|---|---|
| `会议摘要` | Decision summary, KPI cards, PM conclusion |
| `产品基础信息` | Listing basics and interpretation |
| `销售趋势` | Month, price, units, revenue |
| `关键词布局` | Keyword opportunity and CPC/traffic view |
| `评论VOC` | Positive/negative review themes and actions |
| `竞争策略` | Positioning, product, ad, listing, validation actions |
| `数据来源` | Source files, limitations, data gaps |

## Compatibility

When generating `.xlsx` without Excel itself:

- prefer tables and in-cell bars;
- avoid hand-editing complex chart XML unless tested;
- validate every XML file in the package;
- keep a stable fallback workbook without charts.

## Template

Use:

```text
templates/amazon_single_product_meeting_template.xlsx
```

The template contains placeholders only. Runtime code should fill placeholders from the generated report and cleaned JSON.
