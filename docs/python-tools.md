# Python Tooling

The recommended execution entrypoint is Python.

## Requirements

- Python 3.10+
- No third-party Python packages are required.

On Windows, if `python` is not on PATH, use the full interpreter path. Example:

```text
%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe scripts/python/sellersprite_skill_tools.py --help
```

## Main CLI

```bash
python scripts/python/sellersprite_skill_tools.py --help
```

Available commands:

| Command | Purpose |
|---|---|
| `scan-sensitive` | Scan source files and Office packages for secret-like values |
| `check-runtime-config` | Check `.env`, environment variables, and `.mcp.json` without printing keys |
| `check-package` | Run sanitization, required-file checks, and Excel XML checks |
| `test-open-source-skills` | Verify skill preflight and key-request behavior |
| `install-skill` | Install skills to `~/.codex/skills` or `~/.claude/skills` |
| `publish-github-api` | Publish the repository through GitHub Contents API |
| `create-placeholder-template` | Generate the single-product Excel placeholder workbook |
