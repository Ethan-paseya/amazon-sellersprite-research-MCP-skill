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

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\scan-sensitive.ps1
```

Manually inspect the result before publishing.
