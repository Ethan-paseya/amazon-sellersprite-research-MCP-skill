# Amazon SellerSprite MCP Skills

基于 SellerSprite MCP 服务和 Agent Skills 的亚马逊研究工具集，覆盖竞品 Listing 分析、品类选品、关键词调研、评论 VOC 分析和选品深度调研。

> 本仓库是脱敏开源模板，不包含真实 API key、真实商品报告、卖家数据、ASIN 数据、评论原文或私有选品结论。所有密钥均通过本地 `.mcp.json` 或 `.env` 配置。

## 项目简介

本项目配置了 SellerSprite 跨境电商数据服务的 MCP 服务器，并提供五个核心技能：

| 技能 | 分析对象 | 命令 | 用途 |
|---|---|---|---|
| `amazon-analyse` | 单个 Listing | `/amazon-analyse {ASIN} {SITE}` | 竞品 Listing 全维度穿透分析 |
| `category-selection` | 整个品类 | `/category-select "{品类}" {SITE}` | 品类自动化选品分析 |
| `keyword-research` | 关键词词库 | `/keyword-research {ASIN} {SITE}` | 关键词深度调研与 8 维智能分类 |
| `review-analysis` | 用户评论 | `/review-analysis {ASIN} {SITE}` | 评论深度分析与痛点挖掘 |
| `product-research` | 选品深度调研 | `/product-research "{产品关键词}" {SITE}` | LLM 驱动的选品深度调研与决策 |

## 核心功能

### Listing 级别分析 `amazon-analyse`

- **竞品 Listing 分析**：自动获取产品详情、评论、关键词、销量趋势数据。
- **关键词分析**：分析流量来源、竞品关键词布局、长尾词机会。
- **评论情感与 VOC 分析**：聚类用户喜欢点、差评痛点、改进建议。
- **数据验证**：报告末尾加入 Gemini/GLM/规则校验结果。
- **Excel 会议版**：Markdown 报告保存后，可选转换为产品经理会议版 Excel。

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

---

## 快速开始

### 环境要求

- Claude Code CLI、Codex 或其他兼容 Agent Skills 的环境
- 有效的 SellerSprite MCP API Key
- PowerShell 5+ / PowerShell 7+，或 Bash shell
- 可选：Gemini API Key、GLM API Key，用于报告数据验证

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
      "url": "https://mcp.sellersprite.com/mcp?secret-key=YOUR_SELLERSPRITE_KEY",
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
      "url": "https://mcp.sellersprite.com/mcp?secret-key=YOUR_SELLERSPRITE_KEY",
      "name": "SellerSprite MCP"
    }
  }
}
```

编辑 `.env`：

```text
SELLERSPRITE_MCP_URL=https://mcp.sellersprite.com/mcp?secret-key=YOUR_SELLERSPRITE_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GLM_API_KEY=YOUR_GLM_API_KEY
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
DEFAULT_AMAZON_SITE=US
REPORTS_DIR=reports
```

`.mcp.json` 和 `.env` 已在 `.gitignore` 中忽略，请勿提交。

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

### 2. 品类选品分析

```text
# 分析美国站手机支架品类
/category-select "phone stand" US

# 分析英国站笔记本电脑背包品类
/category-select "laptop backpack" GB
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
/product-research "laptop backpack" GB
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

---

## 支持站点

| 站点 | 代码 | 站点 | 代码 |
|---|---|---|---|
| 美国 | US | 日本 | JP |
| 英国 | GB | 西班牙 | ES |
| 德国 | DE | 意大利 | IT |
| 法国 | FR | 加拿大 | CA |
| 印度 | IN | 墨西哥 | MX |
| 澳大利亚 | AU | 阿联酋 | AE |
| 巴西 | BR | 沙特 | SA |

---

## SellerSprite MCP 接口

### 产品相关

| 接口 | 功能 |
|---|---|
| `asin_detail` | 产品详情 |
| `asin_sales_trend` | 销量/销售额/价格趋势 |
| `review` | 用户评论 |
| `traffic_keyword` | ASIN 反查流量词 |
| `traffic_extend` | 竞品/关键词流量扩展 |
| `product_research` | 产品搜索与选品研究 |

### 品类相关

| 接口 | 功能 |
|---|---|
| `product_node` | 类目名称搜索获取 nodeId |
| `category_tree` | 类目树结构 |
| `market_research_statistics` | 类目市场统计 |
| `market_research` | 类目市场筛选 |

### 关键词相关

| 接口 | 功能 |
|---|---|
| `keyword_miner` | 关键词详情与扩展 |
| `keyword_research` | 类目关键词研究 |
| `keyword_research_trends` | 关键词趋势 |

详见 [references/sellersprite-mcp-api.md](references/sellersprite-mcp-api.md)。

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

没有模型 key 或网络不可用时，写明 `未执行真实调用`，并输出人工/规则校验结果。

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
│       └── product-research/
├── skills/
│   ├── amazon-analyse/
│   ├── category-selection/
│   ├── keyword-research/
│   ├── review-analysis/
│   └── product-research/
├── references/
├── templates/
├── scripts/
├── reports/
├── category-reports/
├── keyword-reports/
├── review-analysis-reports/
├── product-research-reports/
└── README.md
```

---

## 技能开发原则

1. **YAML frontmatter**：`description` 必须写清触发场景。
2. **Progressive disclosure**：`SKILL.md` 保持精简，细节放入 `references/`。
3. **Scripts**：用于确定性执行和可复用产物生成。
4. **Templates**：Markdown/Excel 等输出模板放入 `templates/`。
5. **Security first**：真实 key、raw 数据、真实报告不进入开源仓库。

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

A: Markdown 是主报告，必须保留。Excel 只是可选会议版附加输出。

---

## 更新日志

### v1.0.0

- 新增五个 SellerSprite MCP 技能：
  - `amazon-analyse`
  - `category-selection`
  - `keyword-research`
  - `review-analysis`
  - `product-research`
- 新增 Markdown 报告模板。
- 新增 Excel 会议版模板。
- 新增 Gemini/GLM 数据验证规范。

---

## 许可证

MIT License

---

## 致谢

- 感谢 [liangdabiao/amazon-sorftime-research-MCP-skill](https://github.com/liangdabiao/amazon-sorftime-research-MCP-skill/tree/main) 项目提供的 README 结构、技能组织方式和报告目录设计参考。
