#!/usr/bin/env python3
"""Cross-platform tooling for amazon-sellersprite-research-MCP-skill.

This module is the recommended cross-platform toolchain for this repository.
It offers Python equivalents for repository checks, installation, publishing,
and template generation across macOS, Linux, Windows, and CI.
Only Python standard-library modules are used.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


SKILLS = (
    "amazon-analyse",
    "category-selection",
    "keyword-research",
    "review-analysis",
    "product-research",
    "product-planning",
)

REPORT_DIRS = (
    "reports",
    "category-reports",
    "keyword-reports",
    "review-analysis-reports",
    "product-research-reports",
    "product-planning-reports",
)

REQUIRED_FILES = (
    "README.md",
    ".env.example",
    ".mcp.json.example",
    "CLAUDE.md",
    "SECURITY.md",
    ".claude/skills/amazon-analyse/SKILL.md",
    ".claude/skills/amazon-analyse/references/runtime-credential-preflight.md",
    ".claude/skills/amazon-analyse/references/sellersprite-mcp-api.md",
    ".claude/skills/category-selection/SKILL.md",
    ".claude/skills/category-selection/references/runtime-credential-preflight.md",
    ".claude/skills/category-selection/references/sellersprite-mcp-api.md",
    ".claude/skills/keyword-research/SKILL.md",
    ".claude/skills/keyword-research/references/runtime-credential-preflight.md",
    ".claude/skills/keyword-research/references/sellersprite-mcp-api.md",
    ".claude/skills/review-analysis/SKILL.md",
    ".claude/skills/review-analysis/references/runtime-credential-preflight.md",
    ".claude/skills/review-analysis/references/sellersprite-mcp-api.md",
    ".claude/skills/product-research/SKILL.md",
    ".claude/skills/product-research/references/runtime-credential-preflight.md",
    ".claude/skills/product-research/references/sellersprite-mcp-api.md",
    ".claude/skills/product-planning/SKILL.md",
    ".claude/skills/product-planning/references/product-planning-mcp-flow.zh.md",
    ".claude/skills/product-planning/references/runtime-credential-preflight.md",
    ".claude/skills/product-planning/references/sellersprite-mcp-api.md",
    ".claude/skills/product-planning/references/planning-workflow.md",
    "skills/amazon-analyse/SKILL.md",
    "skills/amazon-analyse/references/runtime-credential-preflight.md",
    "skills/amazon-analyse/references/sellersprite-mcp-api.md",
    "skills/category-selection/SKILL.md",
    "skills/category-selection/references/runtime-credential-preflight.md",
    "skills/category-selection/references/sellersprite-mcp-api.md",
    "skills/keyword-research/SKILL.md",
    "skills/keyword-research/references/runtime-credential-preflight.md",
    "skills/keyword-research/references/sellersprite-mcp-api.md",
    "skills/review-analysis/SKILL.md",
    "skills/review-analysis/references/runtime-credential-preflight.md",
    "skills/review-analysis/references/sellersprite-mcp-api.md",
    "skills/product-research/SKILL.md",
    "skills/product-research/references/runtime-credential-preflight.md",
    "skills/product-research/references/sellersprite-mcp-api.md",
    "skills/product-planning/SKILL.md",
    "skills/product-planning/references/product-planning-mcp-flow.zh.md",
    "skills/product-planning/references/runtime-credential-preflight.md",
    "skills/product-planning/references/sellersprite-mcp-api.md",
    "skills/product-planning/references/planning-workflow.md",
    "docs/sellersprite-mcp-usage.zh.md",
    "docs/python-tools.md",
    "references/product-planning-mcp-flow.zh.md",
    "references/runtime-credential-preflight.md",
    "references/sellersprite-mcp-api.md",
    "scripts/python/sellersprite_skill_tools.py",
    "scripts/python/scan_sensitive.py",
    "scripts/python/check_runtime_config.py",
    "scripts/python/check_package.py",
    "scripts/python/test_open_source_skills.py",
    "scripts/python/install_skill.py",
    "scripts/python/publish_github_api.py",
    "scripts/python/create_placeholder_template.py",
    "templates/amazon-single-product-report.zh.md",
    "templates/product-planning-report.zh.md",
    "templates/product-planning-meeting-workbook-layout.zh.md",
    "templates/product-planning-workbook-layout.md",
    "templates/amazon_single_product_meeting_template.xlsx",
    "templates/product_planning_standard_template_V1.xlsx",
    "templates/product_planning_standard_template_V1_manifest.json",
    "reports/README.md",
    "category-reports/README.md",
    "keyword-reports/README.md",
    "review-analysis-reports/README.md",
    "product-research-reports/README.md",
    "product-planning-reports/README.md",
)


@dataclass(frozen=True)
class Pattern:
    label: str
    regex: re.Pattern[str]


SENSITIVE_PATTERNS = (
    Pattern("Google/Gemini API key", re.compile(r"AIza[0-9A-Za-z_\-]{20,}")),
    Pattern("GitHub token", re.compile(r"(github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[0-9A-Za-z_]{20,}")),
    Pattern("GLM/BigModel API key", re.compile(r"[0-9a-fA-F]{32}\.[0-9A-Za-z_\-]{8,}")),
    Pattern("Gemini env value", re.compile(r"GEMINI_API_KEY\s*=\s*(?!YOUR|YOUR_GEMINI_API_KEY|\$\{GEMINI_API_KEY\}|$)[^\s]+")),
    Pattern("GLM env value", re.compile(r"GLM_API_KEY\s*=\s*(?!YOUR|YOUR_GLM_API_KEY|\$\{GLM_API_KEY\}|$)[^\s]+")),
    Pattern("SellerSprite env value", re.compile(r"SELLERSPRITE_API_KEY\s*=\s*(?!YOUR|YOUR_SELLERSPRITE_API_KEY|\$\{SELLERSPRITE_API_KEY\}|$)[^\s]+")),
    Pattern("SellerSprite URL secret", re.compile(r"https://mcp\.sellersprite\.com/mcp\?secret-key=(?!YOUR|YOUR_SELLERSPRITE_API_KEY)[0-9A-Za-z._\-]+")),
    Pattern("SellerSprite header secret", re.compile(r'"secret-key"\s*:\s*"(?!YOUR|\$\{SELLERSPRITE_API_KEY\})[0-9A-Za-z._\-]+"')),
    Pattern("Local Windows user path", re.compile(r"C:[\\/]+Users[\\/]+ETHAN")),
    Pattern("Real-looking ASIN", re.compile(r"\bB0[A-Z0-9]{8}\b")),
)


def repo_root(path: str | Path = ".") -> Path:
    return Path(path).expanduser().resolve()


def iter_files(root: Path) -> Iterable[Path]:
    excluded = {".git", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in excluded for part in path.parts):
            continue
        yield path


def is_binary_skip(path: Path) -> bool:
    return path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".bin", ".ico", ".pdf"}


def read_text_lossy(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def find_sensitive_in_text(text: str, source: str) -> list[str]:
    return [f"{source} :: {pattern.label}" for pattern in SENSITIVE_PATTERNS if pattern.regex.search(text)]


def scan_sensitive(path: str | Path = ".") -> int:
    root = repo_root(path)
    findings: list[str] = []
    for file_path in iter_files(root):
        ext = file_path.suffix.lower()
        if ext in {".xlsx", ".docx", ".pptx"}:
            with zipfile.ZipFile(file_path) as archive:
                for name in archive.namelist():
                    entry_ext = Path(name).suffix.lower()
                    if entry_ext not in {".xml", ".rels", ".txt", ".json", ".csv"}:
                        continue
                    text = archive.read(name).decode("utf-8", errors="ignore")
                    findings.extend(find_sensitive_in_text(text, f"{file_path}!{name}"))
            continue
        if is_binary_skip(file_path):
            continue
        findings.extend(find_sensitive_in_text(read_text_lossy(file_path), str(file_path)))

    if not findings:
        print("No obvious sensitive patterns found.")
        return 0
    print("Potential sensitive content found:")
    for finding in findings:
        print(finding)
    return 1


def read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        values[name.strip()] = value.strip()
    return values


def is_real_value(value: str | None, placeholders: Iterable[str]) -> bool:
    if value is None or not value.strip():
        return False
    if value.startswith("YOUR_"):
        return False
    if value.startswith("${") and value.endswith("}"):
        return False
    return value not in set(placeholders)


def check_runtime_config(path: str | Path = ".", strict: bool = False) -> int:
    root = repo_root(path)
    dotenv = read_dotenv(root / ".env")
    checks = (
        ("SELLERSPRITE_API_KEY", "SellerSprite MCP data", ("YOUR_SELLERSPRITE_API_KEY", "YOUR_KEY"), None),
        ("GEMINI_API_KEY", "Gemini validation", ("YOUR_GEMINI_API_KEY",), None),
        ("GLM_API_KEY", "GLM validation", ("YOUR_GLM_API_KEY",), None),
        ("GLM_BASE_URL", "GLM endpoint", ("YOUR_GLM_BASE_URL",), "https://open.bigmodel.cn/api/paas/v4"),
    )
    rows: list[tuple[str, str, bool, str]] = []
    for name, purpose, placeholders, default in checks:
        source = "missing"
        value = None
        if name in dotenv:
            value = dotenv[name]
            source = ".env"
        elif os.environ.get(name):
            value = os.environ[name]
            source = "environment"
        elif default:
            value = default
            source = "default"
        rows.append((name, purpose, is_real_value(value, placeholders), source))

    mcp_path = root / ".mcp.json"
    mcp_configured = False
    if mcp_path.exists():
        text = read_text_lossy(mcp_path)
        mcp_configured = bool(re.search(r'"url"\s*:\s*"https://mcp\.sellersprite\.com/mcp"', text) and re.search(r'"secret-key"\s*:', text))
    rows.append((".mcp.json sellersprite", "MCP server registration", mcp_configured, ".mcp.json" if mcp_path.exists() else "missing"))

    print(f"{'Name':34} {'Configured':10} {'Source':12} Purpose")
    print("-" * 90)
    for name, purpose, configured, source in rows:
        print(f"{name:34} {str(configured):10} {source:12} {purpose}")

    missing = [row for row in rows if not row[2]]
    if missing:
        print("Missing or placeholder-only runtime configuration:")
        for name, purpose, _, _ in missing:
            print(f"- {name}: {purpose}")
        print("Provide the missing keys at runtime, or configure local ignored .env/.mcp.json files.")
        return 1 if strict else 0
    print("Runtime configuration looks complete. Values were not printed.")
    return 0


def validate_xlsx_xml(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if name.endswith(".xml"):
                ElementTree.fromstring(archive.read(name))


def check_package(path: str | Path = ".") -> int:
    root = repo_root(path)
    print("Running sensitive-content scan...")
    scan_result = scan_sensitive(root)
    if scan_result != 0:
        return scan_result

    print("Checking required files...")
    missing = [item for item in REQUIRED_FILES if not (root / item).exists()]
    if missing:
        for item in missing:
            print(f"Missing required file: {item}")
        return 1

    print("Checking Excel template packages...")
    for item in ("templates/amazon_single_product_meeting_template.xlsx", "templates/product_planning_standard_template_V1.xlsx"):
        validate_xlsx_xml(root / item)

    print("Package check passed.")
    return 0


def test_open_source_skills(path: str | Path = ".") -> int:
    root = repo_root(path)
    print("Testing open-source skill business logic...")
    for item in ("references/runtime-credential-preflight.md", "references/sellersprite-mcp-api.md", ".env.example", ".mcp.json.example"):
        if not (root / item).exists():
            print(f"Missing required open-source support file: {item}")
            return 1
    for item in (".env", ".mcp.json"):
        if (root / item).exists():
            print(f"Runtime secret-bearing file must not exist in open-source package: {item}")
            return 1

    for skill in SKILLS:
        for family in ("skills", ".claude/skills"):
            skill_dir = root / family / skill
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                print(f"Missing SKILL.md: {family}/{skill}")
                return 1
            text = read_text_lossy(skill_md)
            required_bits = (
                ("Credential Preflight", "Missing Credential Preflight section"),
                ("runtime-credential-preflight.md", "Skill does not reference runtime credential preflight"),
                ("SellerSprite MCP API key", "Skill does not explicitly request SellerSprite key when missing"),
            )
            for needle, message in required_bits:
                if needle not in text:
                    print(f"{message}: {family}/{skill}")
                    return 1
            if not re.search(r"Gemini/GLM|Gemini or GLM", text):
                print(f"Skill does not explicitly handle Gemini/GLM validation keys: {family}/{skill}")
                return 1
            for ref in ("runtime-credential-preflight.md", "sellersprite-mcp-api.md"):
                if not (skill_dir / "references" / ref).exists():
                    print(f"Missing bundled reference {ref}: {family}/{skill}")
                    return 1

    print("Running sensitive-content scan...")
    scan_result = scan_sensitive(root)
    if scan_result != 0:
        return scan_result
    print("Open-source skill logic test passed.")
    return 0


def install_skill(target: str = "codex", skill: str = "all", path: str | Path = ".") -> int:
    root = repo_root(path)
    names = list(SKILLS) if skill == "all" else [skill]
    home = Path.home()
    if target == "claude":
        src_root = root / ".claude" / "skills"
        dest_root = home / ".claude" / "skills"
    else:
        src_root = root / "skills"
        dest_root = home / ".codex" / "skills"
    dest_root.mkdir(parents=True, exist_ok=True)
    for name in names:
        src = src_root / name
        if not src.exists():
            print(f"Missing skill source: {src}")
            return 1
        dest = dest_root / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        print(f"Installed {name} to {dest_root}")
    return 0


def github_json(method: str, uri: str, token: str, body: dict | None = None, allow_404: bool = False):
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "amazon-sellersprite-research-MCP-skill-python",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(uri, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if text else None
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            return None
        raise


def publish_github_api(
    repo_name: str = "amazon-sellersprite-research-MCP-skill",
    description: str = "SellerSprite MCP based Amazon research skills for listing, category, keyword, review, and product opportunity analysis.",
    branch: str = "main",
    private: bool = False,
    path: str | Path = ".",
) -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Missing GITHUB_TOKEN. Set it only for the current shell, then rerun.")
        return 1
    root = repo_root(path)
    me = github_json("GET", "https://api.github.com/user", token)
    owner = me["login"]
    repo_uri = f"https://api.github.com/repos/{owner}/{repo_name}"
    repo = github_json("GET", repo_uri, token, allow_404=True)
    if repo is None:
        print(f"Creating repository {owner}/{repo_name}...")
        github_json("POST", "https://api.github.com/user/repos", token, {"name": repo_name, "description": description, "private": private, "auto_init": False})
    else:
        print(f"Repository already exists: {owner}/{repo_name}")

    for file_path in files_for_publish(root):
        relative = file_path.relative_to(root).as_posix()
        encoded_path = urllib.parse.quote(relative)
        uri = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{encoded_path}"
        existing = github_json("GET", uri, token, allow_404=True)
        content = base64.b64encode(file_path.read_bytes()).decode("ascii")
        body = {"message": f"{'Update' if existing else 'Add'} {relative}", "content": content, "branch": branch}
        if existing and existing.get("sha"):
            body["sha"] = existing["sha"]
        print(f"Uploading {relative}")
        github_json("PUT", uri, token, body)

    print(f"Done: https://github.com/{owner}/{repo_name}")
    return 0


def files_for_publish(root: Path) -> Iterable[Path]:
    for file_path in sorted(iter_files(root)):
        relative = file_path.relative_to(root)
        relative_posix = relative.as_posix()
        if relative_posix in {".env", ".mcp.json"}:
            continue
        parts = relative.parts
        if parts and parts[0] in {"raw", "tmp", "cache", "logs", "node_modules"}:
            continue
        if parts and parts[0] in REPORT_DIRS and file_path.name not in {"README.md", ".gitkeep"}:
            continue
        yield file_path


def col_name(index: int) -> str:
    name = ""
    while index > 0:
        index, mod = divmod(index - 1, 26)
        name = chr(65 + mod) + name
    return name


def cell_xml(col: int, row: int, value: object, style: int = 0) -> str:
    ref = f"{col_name(col)}{row}"
    style_attr = f' s="{style}"' if style else ""
    if value is None or value == "":
        return f'<c r="{ref}"{style_attr}/>'
    return f'<c r="{ref}" t="inlineStr"{style_attr}><is><t>{escape(str(value))}</t></is></c>'


def row_xml(row: int, values: list[object], styles: list[int] | None = None) -> str:
    styles = styles or []
    return f'<row r="{row}">' + "".join(cell_xml(i + 1, row, value, styles[i] if i < len(styles) else 0) for i, value in enumerate(values)) + "</row>"


def sheet_xml(rows: list[dict], widths: list[int], freeze_row: int = 1, auto_filter: str = "", merge_cells: str = "") -> str:
    body = "".join(row_xml(i + 1, row["values"], row.get("styles", [])) for i, row in enumerate(rows))
    last_col = max((len(row["values"]) for row in rows), default=1)
    last_row = max(len(rows), 1)
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{width}" customWidth="1"/>' for i, width in enumerate(widths))
    if freeze_row > 0:
        pane = f'<pane ySplit="{freeze_row}" topLeftCell="A{freeze_row + 1}" activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft" activeCell="A{freeze_row + 1}" sqref="A{freeze_row + 1}"/>'
    else:
        pane = '<selection activeCell="A1" sqref="A1"/>'
    filter_xml = f'<autoFilter ref="{auto_filter}"/>' if auto_filter else ""
    merges = f'<mergeCells count="1"><mergeCell ref="{merge_cells}"/></mergeCells>' if merge_cells else ""
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1:{col_name(last_col)}{last_row}"/>
  <sheetViews><sheetView showGridLines="0" workbookViewId="0">{pane}</sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="18"/>
  <cols>{cols}</cols>
  <sheetData>{body}</sheetData>
  {filter_xml}
  {merges}
</worksheet>'''


def create_placeholder_template(output_path: str | Path = "templates/amazon_single_product_meeting_template.xlsx") -> int:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheets = placeholder_sheets()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        archive.writestr("_rels/.rels", root_rels_xml())
        workbook_sheets = []
        workbook_rels = []
        for idx, sheet in enumerate(sheets, start=1):
            workbook_sheets.append(f'<sheet name="{escape(sheet["name"])}" sheetId="{idx}" r:id="rId{idx}"/>')
            workbook_rels.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>')
            archive.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(sheet["rows"], sheet["widths"], 1, sheet.get("filter", ""), sheet.get("merge", "")))
        styles_rel = len(sheets) + 1
        archive.writestr("xl/workbook.xml", workbook_xml("".join(workbook_sheets)))
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml("".join(workbook_rels), styles_rel))
        archive.writestr("xl/styles.xml", styles_xml())
    print(f"Created {output}")
    return 0


def placeholder_sheets() -> list[dict]:
    return [
        {"name": "会议摘要", "widths": [20, 52, 18, 18, 18, 18], "merge": "A1:F1", "rows": [
            {"values": ["{{PRODUCT_TITLE}} 产品经理会议版", "", "", "", "", ""], "styles": [1, 1, 1, 1, 1, 1]},
            {"values": ["会议目标", "{{MEETING_GOAL}}", "", "", "", ""], "styles": [2, 0, 0, 0, 0, 0]},
            {"values": ["ASIN", "{{ASIN}}", "品牌", "{{BRAND}}", "站点", "{{SITE}}"], "styles": [2, 0, 2, 0, 2, 0]},
            {"values": ["价格", "{{PRICE}}", "评分", "{{RATING}}", "评论数", "{{RATINGS_COUNT}}"], "styles": [2, 0, 2, 0, 2, 0]},
            {"values": ["PM结论", "{{PM_CONCLUSION}}", "", "", "", ""], "styles": [2, 0, 0, 0, 0, 0]},
        ]},
        {"name": "产品基础信息", "widths": [18, 46, 34, 34], "filter": "A1:D6", "rows": [
            {"values": ["字段", "内容", "PM解读", "会议关注点"], "styles": [2, 2, 2, 2]},
            {"values": ["标题", "{{PRODUCT_TITLE}}", "{{TITLE_INSIGHT}}", "{{TITLE_DISCUSSION}}"]},
            {"values": ["类目", "{{CATEGORY}}", "{{CATEGORY_INSIGHT}}", "{{CATEGORY_DISCUSSION}}"]},
            {"values": ["价格", "{{PRICE}}", "{{PRICE_INSIGHT}}", "{{PRICE_DISCUSSION}}"]},
            {"values": ["评分", "{{RATING}}", "{{RATING_INSIGHT}}", "{{RATING_DISCUSSION}}"]},
            {"values": ["核心卖点", "{{FEATURES}}", "{{FEATURE_INSIGHT}}", "{{FEATURE_DISCUSSION}}"]},
        ]},
        {"name": "销售趋势", "widths": [14, 14, 14, 28, 16, 28], "filter": "A1:F8", "rows": [
            {"values": ["月份", "价格", "销量", "销量条", "销售额", "销售额条"], "styles": [2, 2, 2, 2, 2, 2]},
            {"values": ["{{MONTH_1}}", "{{PRICE_1}}", "{{UNITS_1}}", "{{UNITS_BAR_1}}", "{{REVENUE_1}}", "{{REVENUE_BAR_1}}"]},
            {"values": ["{{MONTH_2}}", "{{PRICE_2}}", "{{UNITS_2}}", "{{UNITS_BAR_2}}", "{{REVENUE_2}}", "{{REVENUE_BAR_2}}"]},
        ]},
        {"name": "关键词布局", "widths": [28, 14, 14, 12, 12, 12, 28, 44], "filter": "A1:H8", "rows": [
            {"values": ["关键词", "搜索量", "购买量", "购买率", "CPC", "流量占比", "占比条", "PM解读"], "styles": [2, 2, 2, 2, 2, 2, 2, 2]},
            {"values": ["{{KEYWORD_1}}", "{{SEARCHES_1}}", "{{PURCHASES_1}}", "{{PURCHASE_RATE_1}}", "{{CPC_1}}", "{{TRAFFIC_SHARE_1}}", "{{TRAFFIC_BAR_1}}", "{{KEYWORD_NOTE_1}}"]},
            {"values": ["{{KEYWORD_2}}", "{{SEARCHES_2}}", "{{PURCHASES_2}}", "{{PURCHASE_RATE_2}}", "{{CPC_2}}", "{{TRAFFIC_SHARE_2}}", "{{TRAFFIC_BAR_2}}", "{{KEYWORD_NOTE_2}}"]},
        ]},
        {"name": "评论VOC", "widths": [24, 12, 12, 50, 54], "filter": "A1:E8", "rows": [
            {"values": ["问题/优势类型", "样本数", "严重度", "证据摘要", "产品动作"], "styles": [2, 2, 2, 2, 2]},
            {"values": ["{{VOC_TYPE_1}}", "{{VOC_COUNT_1}}", "{{VOC_SEVERITY_1}}", "{{VOC_EVIDENCE_1}}", "{{VOC_ACTION_1}}"]},
            {"values": ["{{VOC_TYPE_2}}", "{{VOC_COUNT_2}}", "{{VOC_SEVERITY_2}}", "{{VOC_EVIDENCE_2}}", "{{VOC_ACTION_2}}"]},
        ]},
        {"name": "竞争策略", "widths": [16, 38, 42, 48, 12], "filter": "A1:E6", "rows": [
            {"values": ["模块", "洞察", "证据", "PM动作", "优先级"], "styles": [2, 2, 2, 2, 2]},
            {"values": ["定位", "{{POSITIONING_INSIGHT}}", "{{POSITIONING_EVIDENCE}}", "{{POSITIONING_ACTION}}", "P0"]},
            {"values": ["产品", "{{PRODUCT_INSIGHT}}", "{{PRODUCT_EVIDENCE}}", "{{PRODUCT_ACTION}}", "P0"]},
            {"values": ["广告", "{{ADS_INSIGHT}}", "{{ADS_EVIDENCE}}", "{{ADS_ACTION}}", "P1"]},
        ]},
        {"name": "数据来源", "widths": [24, 52, 52], "filter": "A1:C6", "rows": [
            {"values": ["数据来源", "文件/接口", "用途"], "styles": [2, 2, 2]},
            {"values": ["{{DATA_PROVIDER}}", "asin_detail", "商品基础信息"]},
            {"values": ["{{DATA_PROVIDER}}", "asin_sales_trend", "销售趋势"]},
            {"values": ["{{DATA_PROVIDER}}", "traffic_keyword / traffic_extend", "关键词与流量"]},
            {"values": ["{{DATA_PROVIDER}}", "review", "评论VOC"]},
        ]},
        {"name": "MCP原始数据", "widths": [28, 22, 12, 38, 70, 38], "filter": "A1:F8", "rows": [
            {"values": ["数据文件/接口", "采集时间", "记录序号", "字段路径", "原始值", "备注"], "styles": [2, 2, 2, 2, 2, 2]},
            {"values": ["{{RAW_SOURCE_1}}", "{{RAW_COLLECTED_AT_1}}", "{{RAW_INDEX_1}}", "{{RAW_FIELD_PATH_1}}", "{{RAW_VALUE_1}}", "{{RAW_NOTE_1}}"]},
            {"values": ["{{RAW_SOURCE_2}}", "{{RAW_COLLECTED_AT_2}}", "{{RAW_INDEX_2}}", "{{RAW_FIELD_PATH_2}}", "{{RAW_VALUE_2}}", "{{RAW_NOTE_2}}"]},
            {"values": ["{{RAW_SOURCE_3}}", "{{RAW_COLLECTED_AT_3}}", "{{RAW_INDEX_3}}", "{{RAW_FIELD_PATH_3}}", "{{RAW_VALUE_3}}", "{{RAW_NOTE_3}}"]},
        ]},
    ]


def content_types_xml(sheet_count: int) -> str:
    sheets = "\n".join(f'  <Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, sheet_count + 1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
{sheets}
</Types>'''


def root_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''


def workbook_xml(sheets_xml: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <bookViews><workbookView activeTab="0"/></bookViews>
  <sheets>{sheets_xml}</sheets>
</workbook>'''


def workbook_rels_xml(rels_xml: str, styles_rel_id: int) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {rels_xml}
  <Relationship Id="rId{styles_rel_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3"><font><sz val="10"/><name val="Microsoft YaHei"/></font><font><b/><sz val="16"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/></font></fonts>
  <fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF5B9BD5"/><bgColor indexed="64"/></patternFill></fill></fills>
  <borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFill="1" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cross-platform tools for Amazon SellerSprite MCP Skills.")
    parser.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan-sensitive", help="Scan source and Office packages for secret-like values.")
    scan.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    scan.set_defaults(func=lambda args: scan_sensitive(args.path))

    runtime = sub.add_parser("check-runtime-config", help="Check .env/.mcp.json runtime configuration without printing keys.")
    runtime.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    runtime.add_argument("--strict", action="store_true", help="Exit 1 when any runtime value is missing.")
    runtime.set_defaults(func=lambda args: check_runtime_config(args.path, args.strict))

    package = sub.add_parser("check-package", help="Run sanitization, required-file, and xlsx XML checks.")
    package.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    package.set_defaults(func=lambda args: check_package(args.path))

    logic = sub.add_parser("test-open-source-skills", help="Check open-source skill business logic and preflight references.")
    logic.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    logic.set_defaults(func=lambda args: test_open_source_skills(args.path))

    install = sub.add_parser("install-skill", help="Install one or all skills to ~/.codex/skills or ~/.claude/skills.")
    install.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    install.add_argument("--target", choices=("codex", "claude"), default="codex")
    install.add_argument("--skill", choices=("all",) + SKILLS, default="all")
    install.set_defaults(func=lambda args: install_skill(args.target, args.skill, args.path))

    publish = sub.add_parser("publish-github-api", help="Publish files through GitHub Contents API. Requires GITHUB_TOKEN.")
    publish.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    publish.add_argument("--repo-name", default="amazon-sellersprite-research-MCP-skill")
    publish.add_argument("--description", default="SellerSprite MCP based Amazon research skills for listing, category, keyword, review, and product opportunity analysis.")
    publish.add_argument("--branch", default="main")
    publish.add_argument("--private", action="store_true")
    publish.set_defaults(func=lambda args: publish_github_api(args.repo_name, args.description, args.branch, args.private, args.path))

    placeholder = sub.add_parser("create-placeholder-template", help="Create the single-product meeting xlsx placeholder template.")
    placeholder.add_argument("--path", default=".", help="Repository root. Default: current directory.")
    placeholder.add_argument("--output", default="templates/amazon_single_product_meeting_template.xlsx")
    placeholder.set_defaults(func=lambda args: create_placeholder_template(Path(args.path) / args.output))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover - CLI safety net
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
