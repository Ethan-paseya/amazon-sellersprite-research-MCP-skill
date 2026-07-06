# Project Structure

```text
amazon-sellersprite-research-MCP-skill/
├── .claude/
│   └── skills/
│       ├── amazon-analyse/
│       ├── category-selection/
│       ├── keyword-research/
│       ├── review-analysis/
│       ├── product-research/
│       └── product-planning/
├── skills/
│   ├── amazon-analyse/
│   ├── category-selection/
│   ├── keyword-research/
│   ├── review-analysis/
│   ├── product-research/
│   └── product-planning/
├── references/
│   ├── sellersprite-mcp-api.md
│   ├── report-management.md
│   ├── excel-export.md
│   └── eval-harness.md
├── templates/
│   ├── amazon-single-product-report.zh.md
│   ├── excel-workbook-layout.md
│   ├── product-planning-workbook-layout.md
│   └── amazon_single_product_meeting_template.xlsx
├── scripts/
│   ├── python/
│   │   ├── sellersprite_skill_tools.py
│   │   ├── scan_sensitive.py
│   │   ├── check_runtime_config.py
│   │   ├── check_package.py
│   │   ├── test_open_source_skills.py
│   │   ├── install_skill.py
│   │   ├── publish_github_api.py
│   │   └── create_placeholder_template.py
├── examples/
│   └── sanitized-report.md
├── reports/
├── category-reports/
├── keyword-reports/
├── review-analysis-reports/
├── product-research-reports/
├── product-planning-reports/
├── docs/
├── .mcp.json.example
├── .env.example
├── CLAUDE.md
├── SECURITY.md
└── README.md
```

## Why Two Skill Paths?

- `.claude/skills/*` mirrors Claude Code style repositories.
- `skills/*` is a generic/Codex-friendly copy.

Keep both in sync when changing the skill.

## Tooling

- `scripts/python/*` is the recommended toolchain for checks, installation, package validation, and GitHub publishing.
