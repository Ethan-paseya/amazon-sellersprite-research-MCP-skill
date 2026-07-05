# Product Planning Workflow

This workflow is distilled from a mature product initiation workbook. Keep it evidence-led and reusable.

## Planning Workbook Tabs

| Tab | Purpose | Required Content |
|---|---|---|
| `意向产品` | Define what will be launched | category, product idea, reference image placeholder, price positioning, customer group, functions, unmet needs, material, packaging, color/style, target purchase cost, target selling price, target margin, launch month, first batch |
| `市场分析` | Decide whether the category deserves entry | sales trend, seasonality, listing age distribution, rating/review distribution, price band, brand concentration, keyword trend, market summary |
| `竞品分析与优化策略` | Convert competitor evidence into product actions | representative ASINs, brand, price, sales, listing selling points, positive review keywords, negative review pain points, benchmark direction |
| `SWOT分析` | Convert evidence into decision logic | strengths from internal capability, weaknesses/gaps, market opportunities, threats/failure modes |
| `ABA排名【季度】` | Build keyword and traffic logic | keyword, monthly search volume, monthly purchases, product count, average price, PPC, supply-demand ratio, click concentration, SellerSprite rank, strategic note |
| `成本试算` | Test financial feasibility | exchange rate, procurement cost, size, weight, chargeable weight, site price, commission, FBA/fulfillment, first-leg freight, refund/defect rate, ad ratio, gross margin, gross profit |
| `销售计划` | Commit to launch assumptions | logistics method, lifecycle stage, price stage, first three month units, revenue, profit, margin, launch action |
| `数据来源` | Preserve audit trail | MCP tools/files, source report, manual assumption list, calculation notes, data gaps |

## Evidence Rules

- Market conclusions must cite market, keyword, or competitor data.
- Competitor product actions must cite listing points, positive reviews, or negative reviews.
- Cost conclusions must cite cost assumptions, formulas, or manually supplied numbers.
- If data is missing, write `N/A` and add a gap note; do not fill with plausible-looking numbers.
- For SellerSprite MCP execution details, read `product-planning-mcp-flow.zh.md`.

## MCP Tool Sequence

| Stage | Required MCP tools | Decision rule |
|---|---|---|
| Category discovery | `product_node` | Select a relevant `nodeIdPath`; record missing node names as a data gap |
| Keyword demand | `keyword_miner`, `keyword_research`, `keyword_research_trends` | Keep only relevant keywords with usable demand/competition fields |
| Competitor pool | `competitor_lookup`, `product_research` | Filter noisy results by title relevance and category node |
| Competitor detail | `asin_detail`, optional `asin_sales_trend` | Use price, rating, ratings, fulfillment, LQS, node path as benchmark evidence |
| VOC | `review` | Extract pain points only from review evidence |
| Category validation | `market_research_statistics`, `market_product_demand_trend`, `market_price_distribution`, `market_rating_distribution`, concentration/distribution tools | Treat empty fields as data gaps |
| ABA/traffic | `keyword_order`, `traffic_keyword_stat`, `traffic_keyword`, `traffic_source`, `aba_research_monthly`, `aba_research_weekly` | Use available fields; do not infer absent traffic shares |
| Risk supplement | `google_trend`, `trademark_*` | Use only as auxiliary evidence; if empty, mark as gap |

## Recommended Decision Gates

| Gate | Pass Signal | Hold/Reject Signal |
|---|---|---|
| Demand | Core and long-tail keywords show enough search/purchase demand | demand exists only in unrelated keywords |
| Competition | Review moat is breakable or niche entry point exists | top listings own traffic and reviews with no clear gap |
| Differentiation | At least one pain point can be solved visibly | product is only a copy of winning listings |
| Profit | Target margin remains acceptable after ad/refund/logistics | profit depends on unrealistic CPC, refund, or freight assumptions |
| Supply Chain | Existing supplier/process can support sampling and QC | unverified material, safety, patent, or compliance risk blocks launch |
| Launch Timing | seasonality supports first 90 days | launch window starts in demand trough without budget buffer |

## Output Style

- Start with a one-page decision summary.
- Put calculations and assumptions in tables.
- Use P0/P1/P2 action priority.
- Keep the final decision explicit: `进入`, `观察`, or `放弃`.
- Preserve Markdown as the main report and use Excel as the operating workbook.
