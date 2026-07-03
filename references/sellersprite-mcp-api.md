# SellerSprite MCP API Reference

This file documents the provider contract used by the skills. Replace endpoint and credentials with your own environment configuration.

## MCP Server

```json
{
  "mcpServers": {
    "sellersprite": {
      "type": "streamableHttp",
      "url": "https://mcp.sellersprite.com/mcp?secret-key=YOUR_SELLERSPRITE_KEY",
      "name": "SellerSprite MCP"
    }
  }
}
```

## Product Calls

| Tool | Purpose | Arguments |
|---|---|---|
| `asin_detail` | Product title, brand, price, rating, category, rank | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `asin_sales_trend` | Sales, revenue, price trend | `{ "marketplace": "US", "asin": "{ASIN}" }` |
| `review` | Reviews by rating band | `{ "marketplace": "US", "asin": "{ASIN}", "starList": [1,2,3] }` |
| `traffic_keyword` | ASIN traffic keywords | `{ "request": { "marketplace": "US", "asin": "{ASIN}" } }` |
| `traffic_extend` | Keyword and competitor traffic extension | `{ "request": { "marketplace": "US", "asinList": ["{ASIN}"], "queryType": 2 } }` |
| `product_research` | Product search and product opportunity discovery | `{ "marketplace": "US", "searchName": "{PRODUCT_KEYWORD}" }` |

## Category Calls

| Tool | Purpose | Arguments |
|---|---|---|
| `product_node` | Search category node by name | `{ "marketplace": "US", "searchName": "{CATEGORY}" }` |
| `category_tree` | Category tree context | `{ "marketplace": "US" }` |
| `market_research_statistics` | Category market statistics | `{ "marketplace": "US", "nodeIdPath": "{NODE_ID_PATH}" }` |
| `market_research` | Category market product filtering | provider-specific filters |

## Keyword Calls

| Tool | Purpose | Arguments |
|---|---|---|
| `keyword_miner` | Keyword detail and expansion | `{ "marketplace": "US", "keyword": "{KEYWORD}" }` |
| `keyword_research` | Category keyword research | `{ "marketplace": "US", "nodeId": "{NODE_ID}" }` |
| `keyword_research_trends` | Keyword trend | `{ "marketplace": "US", "searchKeyword": "{KEYWORD}" }` |

## Site Codes

Common Amazon sites: `US`, `GB`, `DE`, `FR`, `CA`, `JP`, `ES`, `IT`, `MX`, `AE`, `AU`, `BR`, `SA`.

## Data Handling

- Save raw responses under a per-report `raw/` directory.
- Save cleaned JSON separately from raw transport responses.
- Do not commit raw responses to public repositories.
- Do not include private seller notes, order data, or customer data in model-validation prompts.
