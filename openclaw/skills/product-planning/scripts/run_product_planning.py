#!/usr/bin/env python3
"""Validate evidence and render Product-Planning V1 outputs in one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = BASE_DIR / "scripts"
TEMPLATE_DIR = BASE_DIR / "templates"
TEMPLATE_CANDIDATES = (
    TEMPLATE_DIR / "product_planning_standard_template_V1_data_driven.xlsx",
    TEMPLATE_DIR / "product_planning_standard_template_V1_beautified.xlsx",
    TEMPLATE_DIR / "product_planning_standard_template_V1.xlsx",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--validation", type=Path)
    return parser.parse_args()


def select_template(explicit: Path | None) -> Path:
    if explicit:
        if not explicit.is_file():
            raise FileNotFoundError(f"模板不存在: {explicit}")
        return explicit
    for candidate in TEMPLATE_CANDIDATES:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Product-Planning V1 模板全部缺失")


def main() -> int:
    args = parse_args()
    if not args.evidence.is_file():
        raise FileNotFoundError(f"证据文件不存在: {args.evidence}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    qa_path = args.output_dir / "evidence_qa.json"
    template = select_template(args.template)

    validate_command = [
        sys.executable,
        str(SCRIPT_DIR / "validate_product_planning_evidence.py"),
        str(args.evidence),
        "--output",
        str(qa_path),
    ]
    validation = subprocess.run(validate_command, check=False)
    if validation.returncode != 0:
        return validation.returncode

    render_command = [
        sys.executable,
        str(SCRIPT_DIR / "render_product_planning_v1.py"),
        str(args.evidence),
        "--template",
        str(template),
        "--output-dir",
        str(args.output_dir),
        "--qa",
        str(qa_path),
    ]
    if args.validation:
        render_command.extend(["--validation", str(args.validation)])
    return subprocess.run(render_command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
