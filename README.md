# Amazon SellerSprite MCP Skills

基于 SellerSprite MCP 和 Agent Skills 的亚马逊分析工具集。项目结构参考常见 Claude/Codex skill 仓库：根目录提供全局说明，`.claude/skills` 提供 Claude Code 安装格式，`skills` 提供通用/Codex 安装格式，`references` 提供接口和报告规范，`templates` 提供 Markdown/Excel 输出模板。

> 本仓库是脱敏开源模板，不包含真实 API key、真实商品报告、卖家数据、ASIN 数据、评论原文或私有选品结论。

## 项目简介

本项目包含五个核心技能：

| 技能 | 分析对象 | 命令 | 用途 |
|---|---|---|---|
| `amazon-analyse` | 单个 Listing | `/amazon-analyse {ASIN} {SITE}` | 竞品 Listing 全维度穿透分析 |
| `category-selection` | 整个品类 | `/category-select "{品类}" {SITE}` | 品类自动化选品分析 |
| `keyword-research` | 关键词词库 | `/keyword-research {ASIN} {SITE}` | 关键词深度调研与 8 维智能分类 |
| `review-analysis` | 用户评论 | `/review-analysis {ASIN} {SITE}` | 评论深度分析与痛点挖掘 |
| `product-research` | 选品深度调研 | `/product-research "{产品关键词}" {SITE}` | LLM 驱动的选品深度调研与决策 |

## 核心功能

### Listing 级别分析 `amazon-analyse`

- 自动采集产品详情、销量趋势、关键词流量、评论 VOC 等数据。
- 生成结构化中文 Markdown 报告。
- 报告末尾加入 Gemini/GLM/规则校验的 `数据验证` 区块。
- Markdown 报告永远保留，Excel 只是可选附加输出。
- 可选生成产品经理会议版 Excel。

### 品类自动化选品 `category-selection`

- 市场大盘分析：Top 产品、销量、销售额、价格带、评分与评论密度。
- 五维评分：市场规模、增长潜力、竞争烈度、进入壁垒、利润空间。
- 输出品类进入建议：进入、观察、放弃，并给出证据链。

### 关键词深度调研 `keyword-research`

- 采集 ASIN 相关关键词和流量词。
- 按 8 维分类：否定词、品牌词、材质词、场景词、属性词、功能词、核心词、其他。
- 输出广告结构建议、否定词清单和 Listing 埋词建议。

### 评论深度分析 `review-analysis`

- 正负评论分层分析。
- 聚类产品痛点、描述不符、服务/物流问题。
- 输出产品改进建议、Listing 修正建议和客服话术方向。

### 选品深度调研 `product-research`

- 基于产品关键词做市场和竞品研究。
- 结合属性标注、关键词、VOC、壁垒和利润空间。
- 输出是否值得进入、如何切入、验证指标和下一步动作。

## 快速开始

### 环境要求

- Codex、Claude Code 或兼容 Agent Skill 的运行环境
- PowerShell 5+ 或 PowerShell 7+
- SellerSprite MCP key
- 可选：Gemini API key、GLM API key

### 配置 MCP

复制示例配置：

```powershell
Copy-Item .mcp.json.example .mcp.json
Copy-Item .env.example .env
```

在 `.mcp.json` 或 `.env` 中填入你自己的 key。不要提交真实 `.mcp.json` 或 `.env`。

### 安装 Skills

Claude Code 风格：

```powershell
Copy-Item -Recurse .\.claude\skills\* $env:USERPROFILE\.claude\skills\
```

Codex 风格：

```powershell
Copy-Item -Recurse .\skills\* $env:USERPROFILE\.codex\skills\
```

也可以使用安装脚本：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-skill.ps1 -Target codex
powershell -ExecutionPolicy Bypass -File .\scripts\install-skill.ps1 -Target claude
```

### 使用分析技能

```text
/amazon-analyse {ASIN} US
/category-select "phone stand" US
/keyword-research {ASIN} US
/review-analysis {ASIN} US
/product-research "magnetic phone tripod" US
```

## 输出目录

```text
reports/{ASIN}_{SITE}_{YYYYMMDD}/
category-reports/{CATEGORY}_{SITE}_{YYYYMMDD}/
keyword-reports/{ASIN}_{SITE}_{YYYYMMDD}/
review-analysis-reports/{ASIN}_{SITE}_{YYYYMMDD}/
product-research-reports/{KEYWORD}_{SITE}_{YYYYMMDD}/
```

## 目录结构

```text
.
├── .claude/skills/                  # Claude Code skill 安装格式
├── skills/                          # 通用/Codex skill 安装格式
├── references/                      # MCP、报告、Excel、验证规范
├── templates/                       # Markdown 和 Excel 模板
├── scripts/                         # 模板生成、脱敏扫描、安装辅助脚本
├── reports/                         # Listing 分析输出，默认不提交
├── category-reports/                # 品类分析输出，默认不提交
├── keyword-reports/                 # 关键词分析输出，默认不提交
├── review-analysis-reports/         # 评论分析输出，默认不提交
├── product-research-reports/        # 选品分析输出，默认不提交
├── docs/                            # 工作流与脱敏说明
├── .mcp.json.example                # MCP 配置示例
├── .env.example                     # 环境变量示例
├── CLAUDE.md                        # Agent 项目说明
└── SECURITY.md
```

## SellerSprite MCP 接口

| 接口 | 用途 | 参数提示 |
|---|---|---|
| `asin_detail` | 产品详情 | `{ marketplace, asin }` |
| `asin_sales_trend` | 销量/销售额/价格趋势 | `{ marketplace, asin }` |
| `review` | 评论样本 | `{ marketplace, asin, starList }` |
| `traffic_keyword` | ASIN 反查流量词 | `{ request: { marketplace, asin } }` |
| `traffic_extend` | 竞品/关键词扩展 | `{ request: { marketplace, asinList, queryType } }` |
| `product_node` | 类目名称搜索 | `{ marketplace, searchName }` |
| `market_research_statistics` | 类目市场统计 | `{ marketplace, nodeIdPath }` |
| `keyword_miner` | 关键词挖掘 | `{ marketplace, keyword }` |
| `product_research` | 产品搜索/选品研究 | `{ marketplace, searchName, ...filters }` |

详见 [references/sellersprite-mcp-api.md](references/sellersprite-mcp-api.md)。

## Markdown 与 Excel 规则

- Markdown 是主报告，必须保留。
- Excel 是可选会议版附加输出。
- `/amazon-analyse` 在 Markdown 保存后询问：`是否需要转换为Excel表格输出？`
- 无论是否转换 Excel，都不能删除、覆盖或跳过 Markdown。


## 许可证

MIT
