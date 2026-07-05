# SellerSprite MCP 中文使用说明

本文档根据 SellerSprite MCP 官方文档与本仓库整理的 `references/sellersprite-mcp-api.md` 编写，用于说明各类 Amazon 研究任务应如何调用 SellerSprite MCP 工具。

官方文档：https://open.sellersprite.com/mcp

## 1. 运行前准备

### 1.1 必需凭证

| 凭证 | 用途 | 缺失时处理 |
|---|---|---|
| `SELLERSPRITE_API_KEY` | 调用 SellerSprite MCP 获取 Amazon 市场、竞品、关键词、评论数据 | 停止数据采集并向用户索要 |
| `GEMINI_API_KEY` | Gemini 数据验证 | 需要双模型验证时主动索要 |
| `GLM_API_KEY` | GLM 数据验证 | 需要双模型验证时主动索要 |

### 1.2 MCP 配置

推荐使用 header 传 key：

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

不要把真实 key 写进开源仓库、报告、Excel、raw 文件或示例文档。

### 1.3 站点代码

SellerSprite MCP 使用以下站点代码：

```text
US, JP, UK, DE, FR, IT, ES, CA, IN, MX, BR, AU, AE
```

如果用户输入 `GB`，调用 MCP 前应规范化为 `UK`。

## 2. 通用调用原则

1. 先调用 MCP 获取真实数据，再写结论。
2. 每个结论必须能回溯到 MCP 返回、已有本地报告、用户假设或明确标注的外部补充数据。
3. 不要用模型经验补价格、销量、销售额、CPC、评论数、专利、供应链、库存或季节性数据。
4. 先保存 raw/compact 证据，再生成 Markdown 或 Excel。
5. 如果 MCP 工具返回空字段，要把它写成数据缺口，不能悄悄填补。
6. 当 `product_research` 或 `competitor_lookup` 出现跨品类噪声时，必须用标题、类目节点、关键词相关度进行二次过滤。

## 3. 常用工具分组

### 3.1 类目与市场

| 工具 | 用途 | 典型使用场景 |
|---|---|---|
| `product_node` | 根据关键词查类目节点 | 先找到 `nodeIdPath`，为市场分析和商品筛选提供类目条件 |
| `market_research` | 类目市场筛选 | 判断类目规模、均价、销量、评分、利润、品牌/卖家集中度 |
| `market_research_statistics` | 已选节点深度统计 | 对目标节点做进入可行性验证 |
| `market_product_demand_trend` | 类目需求趋势 | 判断需求、退货风险、搜索购买比 |
| `market_price_distribution` | 价格带分布 | 判断哪个价格带销量效率更好 |
| `market_rating_distribution` | 评分分布 | 判断质量门槛和改进空间 |
| `market_brand_concentration` | 品牌集中度 | 判断是否被头部品牌垄断 |
| `market_seller_concentration` | 卖家集中度 | 判断是否被少数卖家控制 |
| `market_listing_date_distribution` | 上架时间分布 | 判断新品是否还能跑出来 |

### 3.2 商品与竞品

| 工具 | 用途 | 典型使用场景 |
|---|---|---|
| `product_research` | 多条件商品筛选 | 找候选竞品、潜力品、价格带样本 |
| `competitor_lookup` | 竞品搜索/ASIN 对比 | 词组匹配、精准匹配、ASIN 列表对比 |
| `asin_detail` | 单 ASIN 详情 | 获取标题、品牌、价格、评分、评分数、类目、卖家、LQS |
| `asin_sales_trend` | ASIN 销售趋势 | 验证销量、销售额、价格变化 |
| `traffic_listing` | 关联商品 | 找目标 ASIN 的强关联竞品 |

### 3.3 关键词与流量

| 工具 | 用途 | 典型使用场景 |
|---|---|---|
| `keyword_miner` | 关键词需求/竞争/PPC | 获取搜索量、购买量、PPC、商品数、供需比、点击集中度 |
| `keyword_research` | 关键词市场筛选 | 批量筛选高需求、低竞争、高增长词 |
| `keyword_research_trends` | 关键词趋势 | 判断关键词是否上升、稳定或衰退 |
| `keyword_order` | ASIN 反查转化词/ABA 相关词 | 拆解竞品真实曝光和转化关键词 |
| `aba_research_monthly` | 月度 ABA 市场机会 | 找热门、异动、持续增长、潜力、长尾市场 |
| `aba_research_weekly` | 周度 ABA 市场机会 | 观察短周期关键词变化 |
| `traffic_keyword_stat` | ASIN 流量词概览 | 判断竞品流量是否依赖广告 |
| `traffic_keyword` | ASIN 流量词明细 | 获取自然/广告/推荐流量词 |
| `traffic_source` | ASIN 或关键词流量结构 | 判断流量来源和广告依赖 |
| `traffic_extend` | 流量扩展 | 扩展竞品或关键词流量池 |

### 3.4 评论、趋势和 IP

| 工具 | 用途 | 典型使用场景 |
|---|---|---|
| `review` | 评论列表 | 正负评论分层、VOC、退货风险、产品改进点 |
| `google_trend` | Google 趋势 | 验证站外需求趋势 |
| `trademark_country_list` | 商标局列表 | 选择商标查询国家/地区 |
| `trademark_list` | 商标列表 | 查品牌名、产品名是否存在商标风险 |
| `trademark_stats` | 商标统计 | 快速判断商标记录规模 |
| `trademark_detail` | 商标详情 | 深入查看商标状态和类别 |

## 4. 输出要求

### 4.1 Markdown 报告

必须保留 Markdown 主报告。报告中每个关键判断后应写明证据来源，例如：

```text
证据：keyword_miner / camera strap / US
```

### 4.2 Excel 工作簿

如果生成 Excel，必须包含 `MCP原始数据` 工作表，用于保存脱敏后的证据字段。

### 4.3 数据缺口

当 MCP 返回空字段或工具不适配时，使用如下格式：

```text
数据缺口：market_price_distribution 返回价格带字段为空，本报告不对价格带销量占比做结论。
```

## 5. product-planning 特别规则

`product-planning` 是跨模块流程，必须按以下顺序采集证据：

1. `product_node` 定位类目节点。
2. `keyword_miner` / `keyword_research` 验证关键词需求。
3. `competitor_lookup` / `product_research` 找代表竞品，并过滤噪声。
4. `asin_detail` / `review` 拆竞品和 VOC。
5. `market_research_statistics` / `market_*` 工具验证类目成熟度、集中度、价格带和新品机会。
6. `keyword_order` / `traffic_*` 工具拆竞品流量和 ABA 关键词。
7. `trademark_*` / `google_trend` 做趋势和 IP 辅助验证。
8. 成本、MOQ、包装、运费、退款率、广告占比必须来自用户数据或明确标注的情景假设。

详见 `references/product-planning-mcp-flow.zh.md`。
