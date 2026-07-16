# OpenClaw + 飞书部署说明

本目录是仓库的 OpenClaw 专用发行层。它不会安装 Codex 插件，而是把六个自包含 Skill 安装到运行飞书机器人的 OpenClaw Gateway 主机。

## 环境要求

- OpenClaw CLI 与 Gateway 已安装；
- Python 3.10 或更高版本；
- SellerSprite MCP API Key；
- Gemini 与 GLM API Key 仅在执行脱敏双模型验证时需要；
- Gateway 允许访问 SellerSprite、Gemini 和 GLM HTTPS 接口。

## 推荐安装

在 OpenClaw Gateway 主机执行：

```bash
git clone https://github.com/Ethan-paseya/amazon-sellersprite-research-MCP-skill.git
cd amazon-sellersprite-research-MCP-skill
python3 openclaw/verify.py
```

## 配置凭证

把 `openclaw/.env.example` 中的变量写入 Gateway 主机的全局文件：

```text
~/.openclaw/.env
```

不要把真实 key 写入仓库、飞书聊天、报告、Excel 或命令行历史。MCP 配置使用 `${SELLERSPRITE_API_KEY}`，真实值只在 Gateway 激活时解析。

完成凭证配置后安装：

```bash
python3 openclaw/install.py --install-deps --configure-mcp
```

安装器默认写入 `~/.openclaw/skills/`。已存在的同名 Skill 会先备份到：

```text
~/.openclaw/skill-backups/amazon-sellersprite-research/{UTC时间}/
```

六个 Skill 会先全部暂存并校验，再统一替换；任一步失败都会恢复旧版本。

## 安装后验证

```bash
openclaw skills list
openclaw mcp status --verbose
openclaw mcp doctor sellersprite --probe
python3 openclaw/verify.py --probe-openclaw
```

修改 Skill 或 MCP 配置后，按当前部署方式重载或重启 Gateway。

## 飞书调用

```text
/amazon-analyse {ASIN} US
/category-select "Phone Strap" US
/keyword-research {ASIN} US
/review-analysis {ASIN} US
/product-research "magnetic phone tripod" US
/product-planning "{ASIN1;ASIN2;ASIN3}" US
```

Markdown 始终保留。生成 Excel 后，OpenClaw 还需要具备飞书文件上传工具或附件权限，才能把 Gateway 工作区中的 `.xlsx` 文件发回会话。

## 更新与回退

更新前先验证新代码：

```bash
git pull --ff-only
python3 openclaw/verify.py
python3 openclaw/install.py
```

需要回到旧版本时，切换到已验证 Git tag 后重新运行安装器。当前已安装版本会再次进入带时间戳的备份目录，不会被直接删除。

## 常见问题

- `Skill 未出现`：检查 `SKILL.md`、`openclaw skills list` 和 Agent Skill allowlist。
- `MCP 不可用`：检查 `SELLERSPRITE_API_KEY` 是否位于 Gateway 全局环境，而不是项目 `.env`。
- `MCP 能列出但不能调用`：运行 `openclaw mcp doctor sellersprite --probe`，并确认 Gateway 具有外网访问权限。
- `Excel 未返回飞书`：先确认文件已在 Gateway 工作区生成，再检查飞书机器人文件上传权限。
- `product-planning` 失败：使用统一入口 `scripts/run_product_planning.py`，不要绕过证据校验直接生成 Excel。
