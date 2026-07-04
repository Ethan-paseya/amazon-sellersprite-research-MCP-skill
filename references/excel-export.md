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
| `MCP原始数据` | Raw SellerSprite MCP evidence used by the report |

## Raw MCP Data Sheet

When an Excel workbook is generated, `MCP原始数据` is required.

Write the MCP server data captured for the report into this sheet so the meeting workbook can be audited without reopening separate JSON files. The sheet should include the source interface/file name, collection time when available, row or item index, field path, raw value, and notes.

Recommended columns:

| Column | Meaning |
|---|---|
| `数据文件/接口` | Raw file name or MCP tool/interface name |
| `采集时间` | Collection timestamp, or `N/A` when unavailable |
| `记录序号` | Item index within the raw response |
| `字段路径` | JSON path or metric name |
| `原始值` | Original value after secret/path redaction |
| `备注` | Data gap, truncation, or normalization notes |

Rules:

- Keep the Markdown report as the primary deliverable.
- Do not write API keys, MCP URLs with secret keys, tokens, or local absolute paths into Excel.
- Preserve metric fields that support conclusions, including price, rating, review count, rank, sales, revenue, keyword volume, CPC, purchase rate, and traffic share.
- Long review text may be compacted or summarized, but the sheet must state that compaction happened.
- If a raw file is too large for a readable worksheet, write a compact row-per-field or row-per-record extract and keep the raw JSON in the report `raw/` folder.

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
