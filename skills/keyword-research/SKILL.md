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

## Data Calls

- `traffic_keyword`: ASIN traffic keywords.
- `traffic_extend`: competitor and related keyword exposure.
- `keyword_miner`: keyword detail and expansion.

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
