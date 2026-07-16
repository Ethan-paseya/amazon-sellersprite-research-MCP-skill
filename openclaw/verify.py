#!/usr/bin/env python3
"""Offline integrity and sanitization checks for the OpenClaw release layer."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent
SKILL_NAMES = (
    "amazon-analyse",
    "category-selection",
    "keyword-research",
    "review-analysis",
    "product-research",
    "product-planning",
)
SENSITIVE_PATTERNS = (
    ("Google/Gemini API key", re.compile(r"AIza[0-9A-Za-z_\-]{20,}")),
    ("GitHub token", re.compile(r"(?:github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[0-9A-Za-z_]{20,}")),
    ("GLM/BigModel API key", re.compile(r"[0-9a-fA-F]{32}\.[0-9A-Za-z_\-]{8,}")),
    ("Gemini env value", re.compile(r"GEMINI_API_KEY\s*=\s*(?!YOUR|\$\{GEMINI_API_KEY\}|$)[^\s]+")),
    ("GLM env value", re.compile(r"GLM_API_KEY\s*=\s*(?!YOUR|\$\{GLM_API_KEY\}|$)[^\s]+")),
    ("SellerSprite env value", re.compile(r"SELLERSPRITE_API_KEY\s*=\s*(?!YOUR|\$\{SELLERSPRITE_API_KEY\}|$)[^\s]+")),
    ("SellerSprite URL secret", re.compile(r"https://mcp\.sellersprite\.com/mcp\?secret-key=(?!YOUR)[0-9A-Za-z._\-]+")),
    ("SellerSprite header secret", re.compile(r'"secret-key"\s*:\s*"(?!YOUR|\$\{SELLERSPRITE_API_KEY\})[0-9A-Za-z._\-]+"')),
    ("Local Windows user path", re.compile(r"C:[\\/]+Users[\\/]+ETHAN", re.IGNORECASE)),
    ("Real-looking ASIN", re.compile(r"\bB0[A-Z0-9]{8}\b")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--probe-openclaw", action="store_true")
    return parser.parse_args()


def skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def check_xlsx(path: Path, root: Path, errors: list[str]) -> None:
    try:
        with zipfile.ZipFile(path) as archive:
            for member in archive.namelist():
                if member.endswith(".xml"):
                    ElementTree.fromstring(archive.read(member))
    except (OSError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        errors.append(f"Excel 包损坏: {path.relative_to(root)}: {exc}")


def verify_release(root: Path) -> dict[str, object]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    required_product_files = (
        "scripts/run_product_planning.py",
        "scripts/render_product_planning_v1.py",
        "scripts/validate_product_planning_evidence.py",
        "templates/product_planning_standard_template_V1_data_driven.xlsx",
        "templates/product_planning_evidence.example.json",
    )

    for name in SKILL_NAMES:
        skill_file = root / "skills" / name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"缺少 Skill: {name}")
            continue
        metadata = skill_frontmatter(skill_file)
        if metadata.get("name") != name or not metadata.get("description"):
            errors.append(f"Skill frontmatter 无效: {name}")
        text = skill_file.read_text(encoding="utf-8")
        if "scripts/python/" in text:
            errors.append(f"仍引用仓库级 scripts/python: {name}")
        for prefix in ("references/", "templates/", "scripts/"):
            unresolved = re.search(rf"(?<!\{{baseDir\}}/){re.escape(prefix)}", text)
            if unresolved:
                warnings.append(f"可能存在非 baseDir 相对路径: {name}: {prefix}")

    product_root = root / "skills" / "product-planning"
    for relative in required_product_files:
        if not (product_root / relative).is_file():
            errors.append(f"product-planning 缺少运行文件: {relative}")

    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.suffix == ".xlsx":
            check_xlsx(path, root, errors)
            continue
        if path.suffix.lower() not in {".md", ".py", ".json", ".json5", ".txt", ".example"} and path.name != ".env.example":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"UTF-8 读取失败: {path.relative_to(root)}: {exc}")
            continue
        for label, pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                errors.append(f"检测到疑似敏感值: {path.relative_to(root)}: {label}")
        if path.suffix == ".py":
            try:
                compile(text, str(path), "exec")
            except SyntaxError as exc:
                errors.append(f"Python 语法错误: {path.relative_to(root)}:{exc.lineno}: {exc.msg}")

    return {
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "skills": len(SKILL_NAMES),
        "errors": errors,
        "warnings": warnings,
    }


def probe_openclaw(errors: list[str]) -> None:
    commands = (["openclaw", "skills", "list"], ["openclaw", "mcp", "doctor", "sellersprite", "--probe"])
    for command in commands:
        try:
            completed = subprocess.run(command, check=False)
        except OSError as exc:
            errors.append(f"无法执行 {' '.join(command)}: {exc}")
            continue
        if completed.returncode != 0:
            errors.append(f"命令失败: {' '.join(command)}")


def main() -> int:
    args = parse_args()
    result = verify_release(args.root)
    if args.probe_openclaw:
        probe_openclaw(result["errors"])
        result["status"] = "FAIL" if result["errors"] else result["status"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
