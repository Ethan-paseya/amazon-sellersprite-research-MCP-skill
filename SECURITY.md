# Security

## Secrets

Never commit API keys, MCP URLs containing real secret keys, encrypted key blobs, raw marketplace data, or generated customer/business reports.

Use `.env` for local secrets and keep `.env.example` placeholder-only.

## Data Handling

This workflow may send report summaries to third-party model providers for evaluation. Before sending data externally:

- remove customer names, seller names, internal notes, and order-level data;
- summarize raw review text instead of sending full review dumps;
- keep ASIN and public marketplace metrics only when that is acceptable for your use case;
- document what was sent and what was withheld.

## Pre-Publish Check

Recommended check:

```bash
python scripts/python/sellersprite_skill_tools.py check-package
python scripts/python/sellersprite_skill_tools.py scan-sensitive
```

Manually inspect the result before publishing. Do not commit `__pycache__/`, `.pyc`, `.env`, `.mcp.json`, raw data folders, or generated private reports.
