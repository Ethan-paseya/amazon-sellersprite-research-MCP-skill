# Sanitization Checklist

Before publishing to GitHub, confirm:

- [ ] No real API keys.
- [ ] No MCP URL with real `secret-key`.
- [ ] No `.env` file.
- [ ] No encrypted key blob.
- [ ] No raw SellerSprite responses.
- [ ] No generated business reports containing real product strategy.
- [ ] No customer/order/seller private data.
- [ ] No WeChat/desktop temp paths containing personal identifiers.
- [ ] No proprietary prompts from private workflows unless intentionally open sourced.
- [ ] Excel templates contain placeholders only.

Recommended grep patterns:

```text
AIza
secret-key=
SELLERSPRITE
GLM_API_KEY
GEMINI_API_KEY
B0[A-Z0-9]{8}
```

Allowed placeholders:

- `YOUR_SELLERSPRITE_KEY`
- `YOUR_GEMINI_API_KEY`
- `YOUR_GLM_API_KEY`
- `{ASIN}`
- `{SITE}`
