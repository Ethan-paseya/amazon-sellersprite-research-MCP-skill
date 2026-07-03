# Eval Harness

The validation layer checks whether the report is faithful to the data.

## Inputs

- Markdown report text
- Cleaned SellerSprite data summary
- Known data gaps

## Checks

| Check | Goal |
|---|---|
| Data consistency | Metrics match source data |
| Method transparency | Sources and gaps are disclosed |
| Reasoning reliability | Claims are supported |
| Risk completeness | Product, ad, review, and market risks are covered |
| Actionability | P0/P1/P2 actions have evidence and metrics |

## Providers

Use environment variables:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GLM_API_KEY=YOUR_GLM_API_KEY
```

If calls fail or keys are unavailable, write `未执行真实调用` and include a manual validation table.
