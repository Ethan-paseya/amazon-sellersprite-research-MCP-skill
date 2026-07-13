# Python Tools

`validate_product_planning_evidence.py` 是新版 Product-Planning 的渲染前质量门禁。它校验三款种子、四款竞品、类目节点选择、固定月份口径、12 月类目趋势、关键词覆盖、VOC 样本、决策证据、V1 Sheet 顺序和敏感信息。`FAIL` 必须先修复；`WARN` 必须进入数据缺口和验证摘要。

```text
python scripts/python/validate_product_planning_evidence.py evidence.json --output evidence_qa.json
```

公开示例可使用：

```text
python scripts/python/validate_product_planning_evidence.py templates/product_planning_evidence.example.json --allow-placeholders
```

`build_product_planning_reusable_template.py` 用于从 `templates/product_planning_meeting_template.xlsx` 生成 Product Planning V1 的干净可复用会议模板。正式企划优先使用 `templates/product_planning_standard_template_V1_beautified.xlsx`；旧模板保留为兼容备份。

```text
python -m pip install openpyxl Pillow
python scripts/python/build_product_planning_reusable_template.py
```

`embed_product_planning_frontend_image.py` 用于把第一个种子 ASIN 已验证的 Amazon 前端首图等比例嵌入 `意向产品!A5`，同时在 `数据来源` Sheet 登记公开来源。图片必须先由 Agent 在 Amazon 商品详情页核实，脚本本身不抓取网页，也不保存凭证。

```text
python scripts/python/embed_product_planning_frontend_image.py planning.xlsx main-image.jpg --asin {FIRST_SEED_ASIN} --marketplace US --source-url https://www.amazon.com/dp/{FIRST_SEED_ASIN}
```

运行 `/product-planning` 的 Agent 负责在命令中接收 3 个 ASIN，并在填充模板前完成 SellerSprite MCP `asin_detail`、`competitor_lookup`、`product_research` 和 `review` 取证。脚本不保存密钥，也不直接访问 MCP。模板和脚本仅保留通用占位符，不包含真实 ASIN、图片、评论、报告或密钥。
