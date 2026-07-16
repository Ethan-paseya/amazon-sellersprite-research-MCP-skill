---
name: product-planning
description: 基于三款种子竞品和 SellerSprite MCP 证据生成 Amazon 产品立项企划。适用于 `/product-planning "{ASIN1;ASIN2;ASIN3}" {SITE}`、产品立项企划、企划表、会议版 Excel、竞品与市场证据整合；默认输出 Markdown 主报告和 Product-Planning V1 七 Sheet Excel。
---

# Product Planning

## 命令

```text
/product-planning "{ASIN1;ASIN2;ASIN3}" {SITE}
```

命令必须包含恰好三个以分号分隔的唯一 ASIN。不要在后续流程中重复向用户索要同一组 ASIN。`GB` 在 SellerSprite MCP 调用前归一为 `UK`。

## Credential Preflight 与必读资料

执行前按顺序读取：

1. `{baseDir}/references/runtime-credential-preflight.md`
2. `{baseDir}/references/integrated-workflow.zh.md`
3. `{baseDir}/references/sellersprite-mcp-api.md`
4. `{baseDir}/references/product-planning-mcp-flow.zh.md`

若仓库模板可用，使用：

- `{baseDir}/templates/product-planning-report.zh.md`
- `{baseDir}/templates/product-planning-meeting-workbook-layout.zh.md`
- `{baseDir}/templates/product_planning_standard_template_V1_manifest.json`
- `{baseDir}/templates/product_planning_standard_template_V1_data_driven.xlsx`（默认首选）
- `{baseDir}/templates/product_planning_standard_template_V1_beautified.xlsx`（兼容备份）
- `{baseDir}/templates/product_planning_standard_template_V1.xlsx`（旧版备份）

## 核心原则

- SellerSprite MCP 是市场、竞品、关键词和评论数据的首要证据来源。
- 所有事实必须来自 MCP、Amazon 前端补充证据、已有源报告或用户明确提供的数据/假设。
- MCP 未返回的字段写 `N/A` 并登记数据缺口，不得编造、插值或用零值占位。
- Amazon 前端只补充 MCP 缺失的主图、页面卖点或其他必要字段，并与 MCP 证据分开标注。
- Markdown 是主报告；Excel 是额外会议版输出，不能替代或删除 Markdown。
- 成本、MOQ、包装、物流、退款率、广告占比和销量目标不由 MCP 推导。默认不生成成本试算和销售计划。

## 标准执行流程

### 1. 输入与凭证预检

解析并校验三个 ASIN 和站点。缺少 SellerSprite MCP API key 时停止真实采集并向用户索要；缺少 Gemini/GLM 凭证只阻止真实双模型验证，不得伪造验证结果。密钥不能进入报告、Excel、日志、示例或开源目录。

### 2. 校验三款种子

对每个 ASIN 调用 `asin_detail`，检查存在性、站点、标题相关性、产品形态和类目节点。无效、重复、跨站点或明显无关时要求用户替换，不能进入最终竞品表。

从三款有效种子的共同类目、功能、场景、目标用户和关键词推导产品方向。用户未提供的工程设计、供应链和财务信息不得补写。

### 3. 补充第四竞品

使用 `competitor_lookup`、必要时 `product_research` 建立候选池，再用 `asin_detail` 校验。保留用户三款竞品，系统只补充一款，用于覆盖头部评价壁垒、低价冲击或高配差异化。没有合格候选时第四款写 `N/A` 并记录原因。

### 4. 锁定市场分析类目

从已验证竞品 `nodeIdPath` 中选择重复出现且与产品形态直接一致的最深叶子节点。没有重复叶子时，才评估覆盖多数种子的最小父节点；父节点购买意图过宽时不得采用。保存候选、覆盖率、相关性、相邻类目、拒绝原因和证据 ID。

### 5. 锁定查询口径

在市场接口调用前创建 `queryManifest`，至少记录：

- `marketplace`
- `analysisMonth`
- `lastCompleteMonth`
- 连续 12 个月 `trendMonths`
- `topN`
- `newProductMonths`
- `selectedNodeIdPath`

当前未完整月份只作快照。趋势和分布改用其他月份时必须记录原因。

### 6. 采集 MCP 证据

按以下顺序调用并保存脱敏入参摘要、返回行数、采用状态、缺失字段和 `evidenceId`：

1. 市场：`market_research_statistics`、`market_product_demand_trend`、价格/评分/评分数/上架时间/上架年份分布、集中度工具。
2. 关键词：`keyword_miner`、`keyword_research`、`keyword_research_trends`。
3. 竞品：`asin_detail`、`asin_sales_trend`，必要时使用可用的价格、优惠或流量工具。
4. VOC：`review`，4-5 星用于已验证卖点，1-3 星用于痛点。
5. ABA/流量：可按分析需要调用 `keyword_order`、`traffic_keyword_stat`、`traffic_keyword`、`traffic_source` 或可用 ABA 工具；结果仅用于 Markdown 与审计证据，不自动写入 `ABA排名【季度】` Sheet。
6. 辅助风险：按需使用 `google_trend`、`trademark_*`。

`market_product_demand_trend` 空返回时只按官方文档允许的月份参数重试；不得用 ASIN 聚合替代类目趋势。

### 7. 生成统一证据对象

把所有采用数据归一到 `evidence.json`。参考 `{baseDir}/templates/product_planning_evidence.example.json`。数值保持原始数值类型，货币、百分比和中文展示由渲染层处理。

每个关键结论、SWOT 条目、决策门禁和行动必须引用 `evidenceId`。`MCP原始数据` 与 `数据来源` Sheet 也从该对象生成。

### 8. 运行规则校验

正式渲染前运行：

```text
python3 "{baseDir}/scripts/validate_product_planning_evidence.py" evidence.json --output evidence_qa.json
```

- `FAIL`：停止生成正式报告，先修复证据或口径。
- `WARN`：可继续，但警告必须写入数据缺口和验证摘要。
- `PASS`：允许正式渲染。

### 9. 生成 Markdown 与 Excel

默认 V1 Sheet 顺序固定：

1. `意向产品`
2. `市场分析`
3. `竞品分析与优化策略`
4. `SWOT分析`
5. `ABA排名【季度】`
6. `MCP原始数据`
7. `数据来源`

`意向产品` 的参考图默认使用第一款种子 ASIN 经核验的 Amazon 前端主图。无法验证时写 `N/A`，不能替换为无关图片。

Excel 默认从 `product_planning_standard_template_V1_data_driven.xlsx` 渲染。该模板只保留七 Sheet 结构、字段位置、样式和图表，不包含真实业务数据；运行时由通过校验的 `evidence.json` 填充。意向产品中功能一至四为已验证卖点，使用灰底红字；功能五至七为评论中可转化的未满足需求，使用亮黄底红字。首选模板缺失或损坏时回退到美化版，再回退到旧 V1 模板，并在数据来源中记录原因。

`市场分析` 必须使用已锁定节点的 12 月趋势、关键词、上架时间/年份、评分数、评分值和价格分布；每张图下方给出不超过三条产品经理点评。

`竞品分析与优化策略` 固定展示三款用户竞品与一款系统补充竞品，包含售价柱状图加评分数折线图、Listing/VOC 优化矩阵。结论不超过三条，落到样品验证、Listing 表达、定价或投放动作。

`SWOT分析` 只重组前三 Sheet 的证据，不新增事实。`ABA排名【季度】` 固定为空白人工维护页：渲染时清除全部单元格、合并区域、图片与图表，不自动写入 ABA 排名、搜索量、关键词或点评。

在 OpenClaw 主机中，规则校验通过后统一运行：

```text
python3 "{baseDir}/scripts/run_product_planning.py" evidence.json --output-dir product-planning-reports/run
```

该入口会先执行证据门禁，再调用固定模板生成 Markdown 与 Excel。不要绕过它直接拼装工作簿。

### 10. 输出质量与交叉验证

交付前检查：

- Markdown、Excel 和文件名标题一致；
- 无 `{{...}}`、`TODO`、模板词或零值假占位；
- 图表引用实际数据区域，空数据不生成误导性图表；
- `.xlsx` Office XML 完整，可用桌面 Excel 时确认无修复提示；
- 静态扫描无 API key、token、MCP 密钥 URL、绝对路径、原始评论或私有数据。

可用时生成脱敏摘要并执行 Gemini + GLM 交叉验证。模型只能评估数据口径、结论一致性、风险完整性和行动可执行性，不能覆盖 MCP 原始事实。模型建议若需要新事实，必须回到 MCP 或前端重新取证。

## 输出目录

```text
product-planning-reports/{ASIN1}_{ASIN2}_{ASIN3}_{SITE}_{YYYYMMDD}/
├── {REPORT_TITLE}.md
├── {REPORT_TITLE}.xlsx
├── evidence.json
├── evidence_qa.json
├── multi_model_validation.json
└── raw/
```

`raw/` 只用于本地运行，不进入开源目录。用户面向报告默认使用中文。

## 最终决策

最终状态只允许 `进入`、`观察` 或 `放弃`。每个门禁必须包含阈值、实际证据和 `evidenceId`。行动按 P0/P1/P2 排序，缺少供应链、成本、专利或合规证据时登记为待验证项，不得给出确定性判断。
