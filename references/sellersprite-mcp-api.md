# SellerSprite MCP API Reference

This reference records the SellerSprite MCP contract used by these skills. It is based on the official SellerSprite MCP documentation and the current callable MCP schemas exposed to Codex.

Official documentation: https://open.sellersprite.com/mcp

## Server Configuration

Preferred configuration uses a clean endpoint plus a `secret-key` header:

```json
{
  "mcpServers": {
    "sellersprite": {
      "type": "streamableHttp",
      "url": "https://mcp.sellersprite.com/mcp",
      "headers": {
        "secret-key": "${SELLERSPRITE_API_KEY}"
      },
      "name": "SellerSprite MCP"
    }
  }
}
```

Fallback form, when a client cannot set headers:

```text
https://mcp.sellersprite.com/mcp?secret-key=YOUR_SELLERSPRITE_API_KEY
```

Do not commit either `.mcp.json` or `.env` with a real key.

## Marketplace Codes

Use SellerSprite MCP marketplace codes exactly as exposed by the runtime schema:

```text
US, JP, UK, DE, FR, IT, ES, CA, IN, MX, BR, AU, AE
```

Some older Amazon workflows use `GB` for the UK site. Normalize user input `GB` to SellerSprite MCP `UK` before calling tools, while preserving the user's original site label in report text if useful.

## Calling Conventions

- Many tools use a wrapper shape: `{ "request": { ... } }`.
- Product/detail tools such as `asin_detail`, `asin_sales_trend`, `review`, `asin_prediction`, `keepa_info`, `asin_coupon_trend`, `asin_detail_with_coupon_trend`, and `bsr_prediction` generally accept direct top-level arguments.
- Always pass `marketplace`.
- Prefer `returnFields` for large calls when only specific metrics are needed.
- For monthly market data, use `month` in `yyyyMM`.
- For `keyword_order`, use `reverseType: "W"` with a Saturday `yyyyMMdd` date, or `reverseType: "M"` with a `yyyyMM` date.
- For list APIs, use `page` and `size`, save pagination decisions, and avoid silently truncating evidence.
- `competitor_lookup` supports up to 40 ASINs per call; split larger lists.
- When no `variation` is specified for `competitor_lookup`, set `variation: "Y"` to exclude variants unless the analysis specifically needs child ASINs.
- Save raw/compact responses in the report's `raw/` folder, then write conclusions only from those responses or clearly labeled assumptions.

## Evidence Rule

All conclusions must be tied to one of these evidence types:

1. SellerSprite MCP response.
2. Existing local research report or workbook.
3. User-provided assumption.
4. Explicitly labeled external/front-end crawl fallback when MCP has no relevant tool.

Do not invent price, sales, revenue, CPC, review, patent, supply-chain, compatibility, seasonality, or inventory conclusions.

## Tool Map by Skill

| Skill | Primary MCP tools | Optional / fallback tools |
|---|---|---|
| `amazon-analyse` | `asin_detail`, `asin_sales_trend`, `traffic_keyword`, `traffic_keyword_stat`, `traffic_source`, `traffic_extend`, `review` | `asin_prediction`, `keepa_info`, `asin_coupon_trend`, `asin_detail_with_coupon_trend`, `traffic_listing`, `keyword_order`, `keyword_miner`, `trademark_list`, `trademark_stats` |
| `category-selection` | `product_node`, `market_research`, `market_research_statistics`, `market_product_demand_trend`, `market_price_distribution`, `market_rating_distribution`, `market_product_concentration`, `market_brand_concentration`, `market_seller_concentration` | `market_seller_country_distribution`, `market_seller_type_concentration`, `market_listing_date_distribution`, `market_listing_trend_distribution`, `market_ratings_count_distribution`, `market_ebc_distribution`, `product_research`, `keyword_research`, `google_trend` |
| `keyword-research` | `traffic_keyword`, `traffic_keyword_stat`, `traffic_source`, `traffic_extend`, `keyword_miner`, `keyword_research`, `keyword_research_trends` | `keyword_order`, `aba_research_trend`, `aba_research_monthly`, `aba_research_weekly`, `google_trend` |
| `review-analysis` | `asin_detail`, `review` with positive and negative `starList` groups | `keepa_info`, `asin_sales_trend`, `traffic_keyword` for expectation-gap context |
| `product-research` | `product_node`, `product_research`, `competitor_lookup`, `market_research`, `market_research_statistics`, `keyword_miner`, `keyword_research`, `review` | `traffic_listing`, `traffic_source`, `market_*_distribution`, `google_trend`, `trademark_country_list`, `trademark_list`, `trademark_stats`, `trademark_detail` |
| `product-planning` | Use the tools required by the source research stage: category, competitor, keyword, review, and trend tools | Cost assumptions and launch plans must be user-provided or clearly labeled as scenario assumptions |

## Product / ASIN Tools

| Tool | Purpose | Typical arguments |
|---|---|---|
| `asin_detail` | Product title, brand, price, rating, reviews, category, seller, listing quality, badges | `{ "marketplace": "US", "asin": "{ASIN}", "returnFields": "asin,title,brand,price,rating,ratings,nodeIdPath" }` |
| `asin_sales_trend` | Monthly sales, revenue, price, parent/child trend | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `asin_prediction` | Sales/rank forecast when available | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `keepa_info` | Keepa-style historical price/rank context when available | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `asin_coupon_trend` | Coupon trend | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `asin_detail_with_coupon_trend` | Product detail plus coupon trend | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `bsr_prediction` | BSR forecast when available | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `review` | Review title/content/rating/date/type filtering | `{ "marketplace": "US", "asin": "{ASIN}", "starList": [1,2,3], "page": 1, "size": 50 }` |

## Traffic and Keyword Tools

| Tool | Purpose | Typical arguments |
|---|---|---|
| `traffic_keyword_stat` | ASIN traffic keyword overview by source | `{ "marketplace": "US", "asin": "{ASIN}", "month": "202606" }` |
| `traffic_keyword` | ASIN traffic keyword details | `{ "request": { "marketplace": "US", "asin": "{ASIN}", "month": "202606" } }` |
| `traffic_source` | Traffic source structure for ASIN or keyword | `{ "request": { "marketplace": "US", "q": "{ASIN_OR_KEYWORD}", "page": 1, "size": 50 } }` |
| `traffic_extend` | Keyword/competitor traffic expansion | `{ "request": { "marketplace": "US", "asinList": ["{ASIN}"], "queryType": 2 } }` |
| `traffic_listing` | Listings related to traffic or keyword context | `{ "request": { "marketplace": "US", "keyword": "{KEYWORD}", "page": 1, "size": 50 } }` |
| `keyword_miner` | Keyword demand, competition, PPC, purchase rate, monopoly and relevance | `{ "request": { "marketplace": "US", "keyword": "{KEYWORD}", "page": 1, "size": 50 } }` |
| `keyword_research` | Keyword market screening with filters | `{ "request": { "marketplace": "US", "keywords": "{KEYWORD}", "page": 1, "size": 50 } }` |
| `keyword_research_trends` | Keyword trend | `{ "marketplace": "US", "searchKeyword": "{KEYWORD}" }` |
| `keyword_order` | ABA keyword ranking/competitor reverse lookup | `{ "request": { "marketplace": "US", "keyword": "{KEYWORD}", "reverseType": "M", "date": "202606" } }` |
| `aba_research_trend` | ABA trend for keywords | `{ "marketplace": "US", "keyword": "{KEYWORD}" }` |
| `aba_research_monthly` | ABA monthly market pattern screening | `{ "request": { "marketplace": "US", "searchModel": 5, "month": "202606" } }` |
| `aba_research_weekly` | ABA weekly market pattern screening | `{ "request": { "marketplace": "US", "date": "20260627" } }` |
| `google_trend` | Google search trend validation | `{ "request": { "marketplace": "US", "keyword": "{KEYWORD}", "monthly": true } }` |

## Category / Market Tools

| Tool | Purpose | Typical arguments |
|---|---|---|
| `product_node` | Search category node by keyword/name/node path | `{ "request": { "marketplace": "US", "keyword": "{CATEGORY}" } }` |
| `market_research` | Category market screening and sortable metrics | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "month": "202606", "page": 1, "size": 50 } }` |
| `market_research_statistics` | Category summary statistics | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "month": "202606" } }` |
| `market_product_demand_trend` | Demand trend in a category | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "month": "202606" } }` |
| `market_price_distribution` | Price-band quantity/sales share/efficiency | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "topN": 10 } }` |
| `market_rating_distribution` | Rating value distribution and market maturity | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "topN": 10 } }` |
| `market_product_concentration` | Head product concentration | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "topN": 10 } }` |
| `market_brand_concentration` | Head brand concentration | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "topN": 10 } }` |
| `market_seller_concentration` | Head seller concentration | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}", "topN": 10 } }` |
| `market_seller_country_distribution` | Seller-country distribution | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |
| `market_seller_type_concentration` | FBA/FBM/Amazon self-operated structure | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |
| `market_listing_date_distribution` | Listing age distribution | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |
| `market_listing_trend_distribution` | New listing trend | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |
| `market_ratings_count_distribution` | Review-count moat distribution | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |
| `market_ebc_distribution` | EBC/A+ adoption distribution | `{ "request": { "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" } }` |

## Product Research and Competitor Tools

| Tool | Purpose | Typical arguments |
|---|---|---|
| `product_research` | Search products with filters for opportunity discovery | `{ "request": { "marketplace": "US", "keyword": "{PRODUCT_KEYWORD}", "page": 1, "size": 50, "variation": "Y" } }` |
| `competitor_lookup` | Search or compare products by ASIN, keyword, brand, seller, node | `{ "request": { "marketplace": "US", "keyword": "{PRODUCT_KEYWORD}", "variation": "Y", "page": 1, "size": 50 } }` |

## Trademark / IP Tools

| Tool | Purpose | Typical arguments |
|---|---|---|
| `trademark_country_list` | Available trademark offices | `{}` |
| `trademark_list` | Search trademarks by text/brand/applicant/status/class | `{ "request": { "text": "{BRAND_OR_PRODUCT_TERM}", "page": 1, "size": 20 } }` |
| `trademark_stats` | Trademark statistics | `{ "request": { "text": "{BRAND_OR_PRODUCT_TERM}" } }` |
| `trademark_detail` | Trademark record detail | Provider-specific trademark id/detail arguments |

## Fallback Rule

If SellerSprite MCP has no interface for a required evidence point, only then use a crawl/browser skill or user-provided files. Mark the output as `外部补充数据` and keep it separate from MCP evidence in raw files and Excel sheets.

## Data Handling

- Save raw responses under a per-report `raw/` directory.
- Save cleaned JSON separately from raw transport responses.
- Do not commit raw responses to public repositories.
- Do not include private seller notes, order data, API keys, local absolute paths, or customer-identifying data in model-validation prompts.
- When exporting Excel, include a `MCP原始数据` sheet with compact, redacted evidence fields so conclusions can be audited.
