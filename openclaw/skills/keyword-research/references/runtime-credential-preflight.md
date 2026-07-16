# Runtime Credential Preflight

Use this reference before any SellerSprite MCP call or Gemini/GLM validation call.

## Required Credentials

| Credential | Purpose | Required for |
|---|---|---|
| `SELLERSPRITE_API_KEY` | Authorize SellerSprite MCP and return marketplace data | All data-backed reports |
| `GEMINI_API_KEY` | Run Gemini judge in the eval harness | Cross-model validation |
| `GLM_API_KEY` | Run GLM judge in the eval harness | Cross-model validation |
| `GLM_BASE_URL` | GLM API endpoint, default `https://open.bigmodel.cn/api/paas/v4` | GLM validation |

## Preflight Rules

1. Before running the business workflow, check whether SellerSprite MCP tools are available and authenticated.
2. Before final data validation, check whether Gemini and GLM credentials are available.
3. If any required credential is missing, expired, placeholder-only, or produces an authentication error, pause and ask the user for the missing credential or ask them to configure local ignored files.
4. Do not continue with fabricated data, mock MCP responses, or fake model-validation results.
5. Do not print, echo, summarize, or commit credential values.
6. Do not write credentials into Markdown reports, Excel workbooks, raw data, examples, templates, README snippets, or files under `open-source/`.
7. Store credentials only in local ignored files such as `.env` and `.mcp.json`, in the user's configured secret store, or in the current private session if the user explicitly provides them for one-time use.

## Prompt to User When Keys Are Missing

Use a short, direct prompt and request only missing items:

```text
当前流程需要真实数据和双模型验证，但缺少以下凭证：

- SellerSprite MCP API key：用于调用卖家精灵 MCP 获取亚马逊市场/竞品/关键词/评论数据
- Gemini API key：用于 Gemini 数据验证
- GLM API key：用于 GLM 数据验证

请提供缺失的 key，或先在本地 `.env` / `.mcp.json` 配置后让我继续。收到后我只用于本地运行，不会写入报告或开源目录。
```

If only one or two credentials are missing, list only those missing credentials.

## Local Config Shape

`.env`:

```text
SELLERSPRITE_API_KEY=YOUR_SELLERSPRITE_API_KEY
SELLERSPRITE_MCP_URL=https://mcp.sellersprite.com/mcp
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GLM_API_KEY=YOUR_GLM_API_KEY
GLM_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

`.mcp.json`:

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

Both `.env` and `.mcp.json` must remain ignored by Git.

## Expected Fallback Behavior

- Missing SellerSprite key: stop before data collection and ask for the key.
- SellerSprite auth/network failure: report the failure and ask the user to verify the key or network.
- Missing Gemini/GLM key: stop before claiming real cross-validation and ask for the missing model key.
- User declines validation keys: mark validation as `未执行真实双模型调用`, include only deterministic/manual checks, and do not call the result Gemini/GLM validation.
- User declines SellerSprite key: do not generate a data-backed business report.
