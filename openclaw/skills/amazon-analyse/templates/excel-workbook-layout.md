# Excel Workbook Layout

Use this layout for the optional product-manager meeting workbook.

## Sheets

1. `会议摘要`
   - product one-liner
   - KPI cards
   - PM conclusion
   - key risk
   - recommended action

2. `产品基础信息`
   - title, brand, category, price, rating, rank
   - product feature interpretation
   - meeting discussion points

3. `销售趋势`
   - month
   - price
   - units
   - revenue
   - in-cell bars or chart

4. `关键词布局`
   - keyword
   - search volume
   - purchase rate
   - CPC
   - traffic share
   - PM interpretation

5. `评论VOC`
   - issue type
   - frequency
   - severity
   - evidence summary
   - product action

6. `竞争策略`
   - positioning
   - product gap
   - advertising strategy
   - listing strategy
   - validation plan

7. `数据来源`
   - data provider
   - file/source
   - purpose
   - limitations

8. `MCP原始数据`
   - source file or MCP interface
   - collection time
   - record index
   - field path
   - raw value
   - notes about redaction, truncation, or gaps

## Raw Data Rule

When Excel output is requested, the workbook must include `MCP原始数据`.

This sheet should preserve the raw SellerSprite MCP evidence used by the report after removing secrets, tokens, MCP URLs with real keys, and local absolute paths. Use row-per-field or row-per-record tables so product, sales, keyword, traffic, review, and market metrics can be checked directly against the meeting-summary sheets.

## Compatibility Rule

If generating `.xlsx` by editing OpenXML directly, prefer conservative formatting and in-cell visuals. Do not mutate chart XML unless the workbook is validated in Excel.
