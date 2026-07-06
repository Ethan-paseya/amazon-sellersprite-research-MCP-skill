# Amazon SellerSprite MCP Skills

基于 SellerSprite MCP 服务和 Agent Skills 的亚马逊研究工具集，覆盖竞品 Listing 分析、品类选品、关键词调研、评论 VOC 分析、选品深度调研和产品立项企划。

> 本仓库是脱敏开源模板，不包含真实 API key、真实商品报告、卖家数据、ASIN 数据、评论原文或私有选品结论。所有密钥均通过本地 `.mcp.json` 或 `.env` 配置。

SellerSprite MCP 官方文档：https://open.sellersprite.com/mcp

## 项目简介

本项目配置了 SellerSprite 跨境电商数据服务的 MCP 服务器，并提供六个核心技能：

| 技能 | 分析对象 | 命令 | 用途 |
|---|---|---|---|
| `amazon-analyse` | 单个 Listing | `/amazon-analyse {ASIN} {SITE}` | 竞品 Listing 全维度穿透分析 |
| `category-selection` | 整个品类 | `/category-select "{品类}" {SITE}` | 品类自动化选品分析 |
| `keyword-research` | 关键词词库 | `/keyword-research {ASIN} {SITE}` | 关键词深度调研与 8 维智能分类 |
| `review-analysis` | 用户评论 | `/review-analysis {ASIN} {SITE}` | 评论深度分析与痛点挖掘 |
| `product-research` | 选品深度调研 | `/product-research "{产品关键词}" {SITE}` | LLM 驱动的选品深度调研与决策 |
| `product-planning` | 产品立项企划 | `/product-planning "{产品企划}" {SITE}` | V1 标准企划：意向产品、市场、竞品优化、SWOT、ABA、MCP源数据与数据来源 |

## 核心功能

### Listing 级别分析 `amazon-analyse`

- **竞品 Listing 分析**：自动获取产品详情、评论、关键词、销量趋势数据。
- **关键词分析**：分析流量来源、竞品关键词布局、长尾词机会。
- **评论情感与 VOC 分析**：聚类用户喜欢点、差评痛点、改进建议。
- **数据验证**：报告末尾加入 Gemini/GLM/规则校验结果。
- **Excel 会议版**：Markdown 报告保存后，可选转换为产品经理会议版 Excel，并在工作簿中保留 `MCP原始数据` 页用于追溯。

### 品类级别分析 `category-selection`

- **市场大盘分析**：Top 产品、销量、销售额、价格带、评论数、评分。
- **五维评分模型**：市场规模、增长潜力、竞争烈度、进入壁垒、利润空间。
- **机会识别**：识别低竞争价格带、评论痛点、关键词空白和切入角度。
- **进入建议**：输出进入、观察或放弃建议，并给出证据链。

### 关键词深度调研 `keyword-research`

- **词库采集**：通过 SellerSprite MCP 获取 ASIN 流量词和相关扩展词。
- **8 维智能分类**：否定词、品牌词、材质词、场景词、属性词、功能词、核心词、其他。
- **广告策略指导**：否定词清单、精准匹配组、场景广告组、广泛匹配组。
- **多格式输出建议**：Markdown 报告、CSV 词库、否定词清单、分类统计 JSON。

### 评论深度分析 `review-analysis`

- **正负评论分层**：分别分析 4-5 星正向反馈和 1-3 星负向反馈。
- **痛点聚类**：产品缺陷、设计功能缺陷、材质外观问题、描述不符、服务物流问题。
- **风险预警**：识别高退货风险、高差评触发点和售后风险。
- **双轨解决方案**：产品改进建议 + Listing/客服话术优化建议。

### 选品深度调研 `product-research`

- **LLM 驱动分析**：围绕产品关键词进行市场、竞品、VOC、壁垒和机会判断。
- **完整流程**：信息收集 → 数据采集 → 属性标注 → 交叉分析 → 竞品与 VOC → 评估决策 → 报告输出。
- **决策输出**：进入、观察或放弃，并提供验证指标和下一步动作。
- **多格式输出建议**：Markdown 完整报告、结构化数据、可视化看板。

### 产品立项企划 `product-planning`

- **V1 企划闭环**：意向产品 → 市场分析 → 竞品分析与优化策略 → SWOT → ABA/关键词 → MCP原始数据 → 数据来源。
- **证据驱动**：企划结论必须来自 SellerSprite MCP、Amazon 前端、已有研究报告、用户输入或明确标注的外部补充数据。
- **会议版 Excel**：默认不输出 `成本试算` 和 `销售计划`；如需财务测算，必须由用户提供成本、物流、售价、广告占比等假设后单独追加。
- **可追溯输出**：每个关键结论都要能回查到 MCP 工具、入参摘要、返回字段或数据缺口。

---

## 快速开始

### 环境要求

- Claude Code CLI、Codex 或其他兼容 Agent Skills 的环境
- 有效的 SellerSprite MCP API Key
- PowerShell 5+ / PowerShell 7+，或 Bash shell
- Gemini API Key、GLM API Key：用于完整的双模型交叉验证；如果缺失，运行时会主动询问，且不能声称已完成真实 Gemini/GLM 验证。

### 获取 SellerSprite API Key

1. 登录 SellerSprite。
2. 打开 SellerSprite MCP/API 相关页面。
3. 创建或复制你的 MCP API Key。
4. 不要把真实 key 提交到 GitHub。

本仓库只提供占位示例：

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

### 配置 MCP

复制示例文件：

```powershell
Copy-Item .mcp.json.example .mcp.json
Copy-Item .env.example .env
```

编辑 `.mcp.json`：

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

编辑 `.env`：

```text
SELLERSPRITE_API_KEY=YOUR_SELLERSPRITE_API_KEY
SELLERSPRITE_MCP_URL=https://mcp.sellersprite.com/mcp
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GLM_API_KEY=YOUR_GLM_API_KEY
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
DEFAULT_AMAZON_SITE=US
REPORTS_DIR=reports
```

`.mcp.json` 和 `.env` 已在 `.gitignore` 中忽略，请勿提交。

### 运行时凭证预检

开源版本不会携带任何真实 key。每个 skill 在正式采集数据前必须执行凭证预检：

| 凭证 | 用途 | 缺失时行为 |
|---|---|---|
| `SELLERSPRITE_API_KEY` | 调用 SellerSprite MCP 获取亚马逊市场、竞品、关键词、评论数据 | 主动向用户索要；不提供则停止数据型报告 |
| `GEMINI_API_KEY` | Gemini 作为交叉验证 judge | 主动向用户索要；不提供则不能写“已执行 Gemini 验证” |
| `GLM_API_KEY` | GLM 作为交叉验证 judge | 主动向用户索要；不提供则不能写“已执行 GLM 验证” |

本地可先运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-runtime-config.ps1 -Path .
```

该脚本只显示是否配置完成，不会打印 key。

运行中如果缺少凭证，Agent 应提示：

```text
当前流程需要真实数据和双模型验证，但缺少以下凭证：

- SellerSprite MCP API key：用于调用卖家精灵 MCP 获取亚马逊市场/竞品/关键词/评论数据
- Gemini API key：用于 Gemini 数据验证
- GLM API key：用于 GLM 数据验证

请提供缺失的 key，或先在本地 `.env` / `.mcp.json` 配置后让我继续。收到后我只用于本地运行，不会写入报告或开源目录。
```

### 安装 Skills

Claude Code 风格：

```powershell
Copy-Item -Recurse .\.claude\skills\* $env:USERPROFILE\.claude\skills\
```

Codex 风格：

```powershell
Copy-Item -Recurse .\skills\* $env:USERPROFILE\.codex\skills\
```

也可以使用脚本：

```powershell
# 安装全部技能到 Codex
powershell -ExecutionPolicy Bypass -File .\scripts\install-skill.ps1 -Target codex

# 安装全部技能到 Claude Code
powershell -ExecutionPolicy Bypass -File .\scripts\install-skill.ps1 -Target claude

# 只安装单个技能
powershell -ExecutionPolicy Bypass -File .\scripts\install-skill.ps1 -Target codex -Skill amazon-analyse
```

---

## 使用分析技能

### 1. Listing 竞品分析

```text
# 分析美国站竞品
/amazon-analyse {ASIN} US

# 分析德国站竞品
/amazon-analyse {ASIN} DE
```

报告保存：

```text
reports/{ASIN}_{SITE}_{YYYYMMDD}/
├── report.md
├── raw/
│   ├── asin_detail.clean.json
│   ├── asin_sales_trend.clean.json
│   ├── traffic_keyword.clean.json
│   ├── traffic_extend.clean.json
│   └── reviews_*.clean.json
└── optional_excel.xlsx
```

Markdown 报告生成后会提示：

```text
是否需要转换为Excel表格输出？
```

无论是否转换 Excel，Markdown 报告都必须保留。

如果选择转换为 Excel，工作簿必须包含 `MCP原始数据` 工作表。该工作表写入本次报告使用过的 SellerSprite MCP 原始返回数据或紧凑字段展开结果，用于核对价格、评分、销量、销售额、关键词、CPC、购买率、流量占比、评论主题等结论来源。写入前必须移除 API key、token、真实 secret-key URL、本地绝对路径等敏感信息。

### 2. 品类选品分析

```text
# 分析美国站手机支架品类
/category-select "phone stand" US

# 分析英国站笔记本电脑背包品类
/category-select "laptop backpack" UK
```

报告保存：

```text
category-reports/{品类名称}_{SITE}_{YYYYMMDD}/
├── report.md
├── data.json
└── dashboard.html
```

五维评分模型：

| 维度 | 分值 | 评分逻辑 |
|---|---:|---|
| 市场规模 | 20 | 销量、销售额、需求深度 |
| 增长潜力 | 25 | 新品机会、趋势、需求扩展 |
| 竞争烈度 | 20 | 品牌集中度、评论壁垒、价格战 |
| 进入壁垒 | 20 | 供应链、认证、专利、差异化难度 |
| 利润空间 | 15 | 均价、CPC、退货风险、成本空间 |

综合评级：

| 总分 | 评级 | 建议 |
|---:|---|---|
| 80-100 | 优秀 | 强烈推荐进入 |
| 70-79 | 良好 | 可以考虑进入 |
| 50-69 | 一般 | 谨慎进入 |
| 0-49 | 较差 | 不建议进入 |

### 3. 关键词深度调研

```text
/keyword-research {ASIN} US
```

报告保存：

```text
keyword-reports/{ASIN}_{SITE}_{YYYYMMDD}/
├── report.md
├── keywords.csv
├── negative_words.txt
├── keywords_*.csv
└── categorized_summary.json
```

8 维智能分类：

| 维度 | 说明 | 应用策略 |
|---|---|---|
| NEGATIVE | 否定/敏感词 | 直接否定 |
| BRAND | 品牌词 | 竞品打法或否定 |
| MATERIAL | 材质词 | 精准匹配 |
| SCENARIO | 场景词 | 按场景拆分广告组 |
| ATTRIBUTE | 属性修饰词 | 长尾精准匹配 |
| FUNCTION | 功能词 | 广泛匹配扩流 |
| CORE | 核心产品词 | 主词投放 |
| OTHER | 其他 | 补充埋词或人工复核 |

### 4. 评论深度分析

```text
/review-analysis {ASIN} US
```

报告保存：

```text
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/
├── report.md
└── data/
    ├── product_detail.clean.json
    ├── reviews_positive.clean.json
    ├── reviews_negative.clean.json
    └── negative_reviews_analysis.json
```

6 维痛点分析框架：

| 维度 | 识别内容 | 严重程度 |
|---|---|---|
| 产品缺陷 | 破损、耐久、失效 | 高/中/低 |
| 结构/组装问题 | 零件松动、接口断裂、安装困难 | 高/中/低 |
| 设计/功能缺陷 | 操作复杂、功能缺失、体验差 | 高/中/低 |
| 外观/材质问题 | 异味、划痕、色差、材质不适 | 高/中/低 |
| 描述不符 | 尺寸、颜色、功能预期偏差 | 高/中/低 |
| 服务/物流问题 | 二手/瑕疵品、配件缺失、退换货困难 | 高/中/低 |

### 5. 选品深度调研

```text
# 分析一个产品方向
/product-research "magnetic phone tripod" US

# 分析英国站产品方向
/product-research "laptop backpack" UK
```

报告保存：

```text
product-research-reports/{产品关键词}_{SITE}_{YYYYMMDD}/
├── report.md
├── data.json
└── dashboard.html
```

完整流程：

```text
信息收集 → 数据采集 → 属性标注 → 交叉分析 → 竞品与 VOC → 壁垒评估 → 选品决策 → 报告输出
```

### 6. 产品立项企划

```text
# 基于产品方向输出立项企划
/product-planning "camera strap" US

# 基于已有研究结果整理企划表
/product-planning "magnetic phone tripod" US
```

报告保存：

```text
product-planning-reports/{产品企划}_{SITE}_{YYYYMMDD}/
├── report.md
├── planning.xlsx
├── assumptions.md
└── raw/
```

企划流程：

```text
意向产品 → 市场分析 → 竞品分析与优化策略 → SWOT → ABA/关键词 → MCP原始数据 → 数据来源 → 进入/观察/放弃决策
```

---

## 支持站点

| 站点 | 代码 | 站点 | 代码 |
|---|---|---|---|
| 美国 | US | 日本 | JP |
| 英国 | UK | 西班牙 | ES |
| 德国 | DE | 意大利 | IT |
| 法国 | FR | 加拿大 | CA |
| 印度 | IN | 墨西哥 | MX |
| 澳大利亚 | AU | 阿联酋 | AE |
| 巴西 | BR |  |  |

说明：SellerSprite MCP 工具 schema 使用 `UK` 表示英国站。若用户输入旧习惯 `GB`，执行 skill 时应先规范化为 `UK` 再调用 MCP。

---

## SellerSprite MCP 接口

### 产品相关

| 接口 | 功能 |
|---|---|
| `asin_detail` | 产品详情 |
| `asin_sales_trend` | 销量/销售额/价格趋势 |
| `asin_prediction` / `bsr_prediction` | 销量或排名预测 |
| `keepa_info` | 历史价格/排名辅助信息 |
| `asin_coupon_trend` / `asin_detail_with_coupon_trend` | 优惠券/促销趋势 |
| `review` | 用户评论 |
| `competitor_lookup` | 竞品搜索和对比 |
| `product_research` | 产品搜索与选品研究 |

### 流量与关键词相关

| 接口 | 功能 |
|---|---|
| `traffic_keyword_stat` | ASIN 流量词概览统计 |
| `traffic_keyword` | ASIN 反查流量词 |
| `traffic_source` | 自然/推荐/广告流量结构 |
| `traffic_extend` | 竞品/关键词流量扩展 |
| `traffic_listing` | 流量或关键词相关 Listing |
| `keyword_miner` | 关键词需求、竞争、PPC、购买率等 |
| `keyword_research` | 关键词市场筛选 |
| `keyword_research_trends` | 关键词趋势 |
| `keyword_order` | ABA 排名/反查 |
| `aba_research_trend` / `aba_research_monthly` / `aba_research_weekly` | ABA 趋势与市场模式 |

### 品类相关

| 接口 | 功能 |
|---|---|
| `product_node` | 类目名称搜索获取 nodeId |
| `market_research_statistics` | 类目市场统计 |
| `market_research` | 类目市场筛选 |
| `market_product_demand_trend` | 类目需求趋势 |
| `market_price_distribution` | 价格带分布 |
| `market_rating_distribution` | 评分分布 |
| `market_product_concentration` | 商品集中度 |
| `market_brand_concentration` | 品牌集中度 |
| `market_seller_concentration` | 卖家集中度 |
| `market_seller_country_distribution` | 卖家国家分布 |
| `market_seller_type_concentration` | 卖家/FBA/FBM/自营结构 |
| `market_listing_date_distribution` / `market_listing_trend_distribution` | 上架时间和新品趋势 |
| `market_ratings_count_distribution` | 评论数壁垒分布 |
| `market_ebc_distribution` | EBC/A+ 覆盖情况 |

### 商标/IP 与趋势补充

| 接口 | 功能 |
|---|---|
| `trademark_country_list` / `trademark_list` / `trademark_stats` / `trademark_detail` | 商标检索和风险辅助判断 |
| `google_trend` | Google 搜索趋势辅助验证 |

详见 [references/sellersprite-mcp-api.md](references/sellersprite-mcp-api.md)。

中文使用说明见 [docs/sellersprite-mcp-usage.zh.md](docs/sellersprite-mcp-usage.zh.md)。
`product-planning` 的逐模块 MCP 调用流程见 [references/product-planning-mcp-flow.zh.md](references/product-planning-mcp-flow.zh.md)。

---

## 数据验证

`amazon-analyse` 报告末尾必须加入：

```text
Gemini Eval Harness 数据验证
```

验证维度：

| 验证项 | 说明 |
|---|---|
| 数据一致性 | 价格、评分、评论数、销量、类目、关键词是否与原始数据一致 |
| 口径透明度 | 是否说明来源、缺口、冲突和采用口径 |
| 推理可靠性 | 是否存在过度推断 |
| 风险完整性 | 是否覆盖产品、广告、评论、履约风险 |
| 建议可执行性 | P0/P1/P2 动作是否有依据和验证指标 |

没有模型 key 时，必须先主动向用户索要 Gemini/GLM key。用户拒绝或网络不可用时，才写明 `未执行真实双模型调用`，并且只能输出人工/规则校验结果，不能把结果描述为 Gemini/GLM 真实验证。

---

## 项目结构

```text
amazon-sellersprite-research-MCP-skill/
├── .mcp.json.example
├── .env.example
├── .claude/
│   └── skills/
│       ├── amazon-analyse/
│       ├── category-selection/
│       ├── keyword-research/
│       ├── review-analysis/
│       ├── product-research/
│       └── product-planning/
├── skills/
│   ├── amazon-analyse/
│   ├── category-selection/
│   ├── keyword-research/
│   ├── review-analysis/
│   ├── product-research/
│   └── product-planning/
├── references/
├── templates/
├── scripts/
├── reports/
├── category-reports/
├── keyword-reports/
├── review-analysis-reports/
├── product-research-reports/
├── product-planning-reports/
└── README.md
```

---

## 技能开发原则

1. **YAML frontmatter**：`description` 必须写清触发场景。
2. **Progressive disclosure**：`SKILL.md` 保持精简，细节放入 `references/`。
3. **Scripts**：用于确定性执行和可复用产物生成。
4. **Templates**：Markdown/Excel 等输出模板放入 `templates/`。
5. **Security first**：真实 key、raw 数据、真实报告不进入开源仓库；但本地生成的私有 Excel 可以包含脱敏后的 `MCP原始数据` 工作表，方便业务复核。

---

## 常见问题

### Q: ASIN 查询不到产品？

A: 先用 `asin_detail` 验证 ASIN 是否存在。若返回空结果：

1. 确认 ASIN 格式是否正确。
2. 确认站点是否正确。
3. 改用 `product_research` 搜索关键词寻找候选产品。

### Q: 报告中出现乱码？

A: 检查数据解析和文件编码，所有 Markdown 建议使用 UTF-8 保存。

### Q: Excel 报告无法打开？

A: 优先使用稳定模板和单元格内可视化。直接改写 `.xlsx` 图表 XML 时要谨慎，必须验证 Excel 可打开。

### Q: 能否把生成报告提交到 GitHub？

A: 不建议。真实报告、raw JSON、评论数据、私有结论默认都不应开源。

### Q: Excel 和 Markdown 哪个是主报告？

A: Markdown 是主报告，必须保留。Excel 只是可选会议版附加输出；若输出 Excel，必须同时包含 `MCP原始数据` 工作表，方便从会议摘要反查到 MCP 数据依据。

---

## 更新日志

### v1.0.2

- 确认 `product-planning` V1 标准会议版模板：`意向产品`、`市场分析`、`竞品分析与优化策略`、`SWOT分析`、`ABA排名【季度】`、`MCP原始数据`、`数据来源`。
- 新增 `product_planning_standard_template_V1.xlsx` 和 `product_planning_standard_template_V1_manifest.json`。
- 统一 README、`skills/product-planning` 与 `.claude/skills/product-planning` 的 V1 口径。
- 复跑脱敏扫描，确认不包含真实 API key、GitHub token、MCP secret URL、本地用户路径或真实 ASIN 样例。

### v1.0.1

- 移除开源 Excel 模板中的本地 `absPath` 元数据。
- 复跑脱敏扫描，确认不包含真实 API key、GitHub token、MCP secret URL、本地用户路径或真实 ASIN 样例。
- 增加 `VERSION` 文件，便于发布和版本追踪。

### v1.0.0

- 新增六个 SellerSprite MCP 技能：
  - `amazon-analyse`
  - `category-selection`
  - `keyword-research`
  - `review-analysis`
  - `product-research`
  - `product-planning`
- 新增 Markdown 报告模板。
- 新增 Excel 会议版模板，包含 `MCP原始数据` 审计工作表。
- 新增产品立项企划流程模板。
- 新增 Gemini/GLM 数据验证规范。

---

## 许可证

MIT License

---

## 致谢

- 感谢 [liangdabiao/amazon-sorftime-research-MCP-skill](https://github.com/liangdabiao/amazon-sorftime-research-MCP-skill/tree/main) 项目提供的 README 结构、技能组织方式和报告目录设计参考。
