# Product Planning MCP 调用流程

本文档定义 `/product-planning "{ASIN1;ASIN2;ASIN3}" {SITE}` 的证据采集顺序、MCP 工具选择和输出口径。先校验三款种子 ASIN，再从其共同证据推导 `{DERIVED_PRODUCT_DIRECTION}`。

## 1. 总体原则

- 先取 MCP 数据，再写企划结论。
- 每个表格/章节都要有证据来源或明确的数据缺口。
- 不要把 `product_research` 的第一页结果直接当竞品池；必须做标题、类目节点、关键词相关度过滤。
- V1 标准会议版 Excel 默认只输出 `意向产品`、`市场分析`、`竞品分析与优化策略`、`SWOT分析`、`ABA排名【季度】`、`MCP原始数据`、`数据来源`。
- 成本、MOQ、包装、运费、退款率、广告占比不是 SellerSprite MCP 的直接输出，必须来自用户输入、已有文件或标注为情景假设。
- `成本试算` 和 `销售计划` 不属于 V1 默认 Sheet；只有用户明确要求财务测算并提供假设时，才作为可选扩展输出。
- 如果 Gemini/GLM key 缺失，先向用户索要；用户拒绝后只能写规则校验，不能写真实双模型验证。

## 2. 企划模块与 MCP 工具映射

| 企划模块 | 核心问题 | 必调 MCP 工具 | 可选 MCP 工具 | 输出字段/证据 |
|---|---|---|---|---|
| 意向产品 | 产品方向是否有明确市场和关键词 | `product_node`, `keyword_miner` | `google_trend` | 类目节点、商品数、搜索量、购买量、PPC、商品数、供需比 |
| 市场分析 | 类目是否值得进入 | `market_research_statistics`, `market_research` | `market_product_demand_trend`, `market_price_distribution`, `market_rating_distribution`, `market_listing_date_distribution` | 均价、平均销量、平均销售额、评分、评论数、新品占比、价格带、评分带 |
| 竞品分析与优化策略 | 谁是直接竞品，有什么缺口 | `competitor_lookup`, `asin_detail` | `product_research`, `traffic_listing`, `asin_sales_trend` | ASIN、品牌、标题、价格、评分、评价数、类目节点、LQS、履约方式 |
| VOC/评论 | 用户痛点是什么 | `review` | `traffic_keyword` | 低星评论主题、正向卖点、退货/安全/说明书风险 |
| SWOT | 机会和威胁是否有证据 | 复用市场、竞品、关键词、评论工具 | `trademark_list`, `trademark_stats`, `google_trend` | S/W/O/T 每条必须引用数据源 |
| ABA/关键词 | 先打哪些词，避开哪些词 | `keyword_miner`, `keyword_order` | `keyword_research`, `keyword_research_trends`, `aba_research_monthly`, `aba_research_weekly`, `traffic_source` | 搜索量、购买量、PPC、商品数、供需比、点击集中度、转化类型 |
| 成本试算（可选扩展） | 价格是否覆盖成本 | 无直接 MCP 硬依赖 | `market_research_statistics`, `keyword_miner` | 平台均价、竞品价格、PPC 作为售价/广告假设参考；成本用用户数据或情景假设 |
| 销售计划（可选扩展） | 90 天目标是否合理 | `market_research_statistics`, `keyword_miner`, `competitor_lookup` | `asin_sales_trend` | 均值销量、关键词需求、竞品价格/评分/评论壁垒；销量目标必须标注假设 |
| 数据来源 | 是否可审计 | 所有实际调用工具 | 无 | 工具名、入参摘要、字段缺口、采用/未采用原因 |

## 3. 推荐调用顺序

### Step 1: 类目定位

调用：

```json
{
  "tool": "product_node",
  "request": {
    "marketplace": "{SITE}",
    "keyword": "{DERIVED_PRODUCT_DIRECTION}",
    "returnFields": "nodeIdPath,nodeName,path,products"
  }
}
```

处理：

- 选择与产品方向最相关的 `nodeIdPath`。
- 如果 `nodeName/path` 为空但 `nodeIdPath/products` 可用，要记录字段缺口。

### Step 2: 关键词可行性

调用：

```json
{
  "tool": "keyword_miner",
  "request": {
    "marketplace": "{SITE}",
    "keyword": "{DERIVED_PRODUCT_DIRECTION}",
    "page": 1,
    "size": 20,
    "returnFields": "keyword,searches,purchases,bid,products,supplyDemandRatio,monopolyClickRate,titleDensity,relevancy"
  }
}
```

处理：

- 优先保留相关度高、标题密度低、PPC 可控、供需比合理的词。
- 如果 `purchaseRate` 等字段为空，不对该字段做结论。

### Step 3: 竞品池生成与降噪

先用 `competitor_lookup`：

```json
{
  "tool": "competitor_lookup",
  "request": {
    "marketplace": "{SITE}",
    "keyword": "{DERIVED_PRODUCT_DIRECTION}",
    "matchType": 1,
    "variation": "Y",
    "page": 1,
    "size": 20
  }
}
```

再用 `product_research` 做补充筛选：

```json
{
  "tool": "product_research",
  "request": {
    "marketplace": "{SITE}",
    "keyword": "{DERIVED_PRODUCT_DIRECTION}",
    "variation": "Y",
    "page": 1,
    "size": 20
  }
}
```

降噪规则：

- 标题必须命中核心产品词或高相关长尾词。
- 类目节点要与目标类目一致或高度相近。
- 明显跨品类商品只进入“噪声样本”，不能作为直接竞品。

### Step 4: 竞品详情

对筛选后的代表 ASIN 调用：

```json
{
  "tool": "asin_detail",
  "marketplace": "{SITE}",
  "asin": "{ASIN}",
  "returnFields": "asin,title,brand,price,rating,ratings,nodeIdPath,fulfillment,sellerName,lqs"
}
```

输出：

- 价格带
- 评分/评论壁垒
- Listing 质量
- 履约方式
- 品牌位置

### Step 5: VOC

调用：

```json
{
  "tool": "review",
  "marketplace": "{SITE}",
  "asin": "{ASIN}",
  "starList": [1, 2, 3],
  "page": 1,
  "size": 20
}
```

输出：

- 产品安全/耐用性风险
- 使用体验风险
- 尺寸/兼容性风险
- 说明书/预期不符风险
- 可转化为产品需求的高频痛点

### Step 6: 类目深度验证

对目标 `nodeIdPath` 调用：

```json
market_research_statistics
market_product_demand_trend
market_price_distribution
market_rating_distribution
market_brand_concentration
market_seller_concentration
market_listing_date_distribution
```

输出：

- 市场均价、平均销量、平均销售额
- 评分/评论门槛
- 品牌和卖家集中度
- 新品机会
- 价格带机会

如果某工具返回大量空字段，必须写入数据缺口。

### Step 7: ABA/流量验证

对代表 ASIN 调用：

```json
keyword_order
traffic_keyword_stat
traffic_keyword
traffic_source
```

输出：

- 竞品核心转化词
- 广告依赖度
- 自然流量 vs 广告流量
- 关键词优先级

### Step 8: 成本与销售计划（可选扩展）

V1 标准会议版默认不输出成本与销售计划 Sheet。只有用户明确要求财务测算，并提供采购、物流、售价、广告占比、退款率等假设时，才执行本步骤。

MCP 只提供市场参考，不直接提供真实采购成本。必须分清：

| 项目 | 来源 |
|---|---|
| 目标售价 | 竞品价格 + 市场均价 |
| PPC/广告假设 | `keyword_miner` |
| 目标销量 | 市场均值 + 竞品销量 + 人工情景假设 |
| 采购成本 | 用户输入或供应商资料 |
| 运费/FBA/退款率 | 用户输入、平台规则或情景假设 |

## 4. 报告必须包含的数据缺口表

| 工具 | 缺口 | 对结论的影响 | 处理 |
|---|---|---|---|
| `{tool}` | `{missing_field}` | `{impact}` | `{fallback_or_note}` |

## 5. 结论评级

| 结论 | 条件 |
|---|---|
| `进入` | 关键词需求明确、竞品痛点可解决、价格带有空间、评论壁垒可突破 |
| `观察` | 有需求但数据缺口较多，或竞品噪声/类目混杂，需要补充调研 |
| `放弃` | 关键词需求弱、竞品垄断强、利润依赖不现实假设、核心痛点不可解决 |
