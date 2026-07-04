---
name: keyword-research
description: Amazon keyword library research using SellerSprite MCP. Use when the user runs `/keyword-research {ASIN} {SITE}` to collect keyword data, classify terms into eight dimensions, and produce advertising and listing keyword strategy outputs.
---

# Keyword Research

## Command

```text
/keyword-research {ASIN} {SITE}
```

## Goal

Build a structured keyword library for listing optimization and ad campaign planning.

## Credential Preflight

Before any data call, read `references/runtime-credential-preflight.md` when it is available.

- If SellerSprite MCP is not configured, unavailable, or returns an authentication error, ask the user for the SellerSprite MCP API key before keyword research.
- If Gemini/GLM validation is part of the requested output and model keys are missing, ask for the missing keys before validation.
- Do not continue with mock keyword metrics or fabricated ABA/search-volume data.
- Do not write provided keys into reports, CSVs, raw files, examples, or the open-source repository.

## Required Reference

Read `references/sellersprite-mcp-api.md` before execution when it is available.
Normalize `GB` to SellerSprite MCP `UK` before tool calls.

## Data Calls

- `traffic_keyword_stat`: ASIN traffic source overview.
- `traffic_keyword`: ASIN traffic keyword details.
- `traffic_source`: organic/recommendation/ad traffic source structure.
- `traffic_extend`: competitor and related keyword exposure.
- `keyword_miner`: keyword demand, purchase rate, PPC/bid, product count, monopoly click rate, title density, and relevance.
- `keyword_research`: keyword market screening and opportunity filters.
- `keyword_research_trends`: keyword trend.
- `keyword_order`: ABA ranking/reverse lookup when rank evidence is needed.
- `aba_research_trend`, `aba_research_monthly`, `aba_research_weekly`: ABA market patterns when available.
- `google_trend`: optional external trend validation.

Save raw or compact MCP responses before classifying keywords. Do not infer search volume, purchase volume, CPC, or competition metrics when the corresponding MCP field is absent.

## Eight-Dimension Classification

| Type | Meaning | Usage |
|---|---|---|
| NEGATIVE | irrelevant or risky terms | add to negative list |
| BRAND | brand or competitor brand terms | isolate or negate |
| MATERIAL | material terms | exact/phrase match |
| SCENARIO | usage scenario terms | scenario ad groups |
| ATTRIBUTE | attribute modifiers | long-tail targeting |
| FUNCTION | function terms | broad expansion |
| CORE | core product terms | main campaign |
| OTHER | supplemental terms | manual review |

## Output

Save under:

```text
keyword-reports/{ASIN}_{SITE}_{YYYYMMDD}/
```

Recommended files: `report.md`, `keywords.csv`, `negative_words.txt`, `categorized_summary.json`.
