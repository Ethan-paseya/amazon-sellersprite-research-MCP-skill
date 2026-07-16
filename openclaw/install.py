#!/usr/bin/env python3
"""Install the six Amazon SellerSprite Skills into an OpenClaw skill root."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parent
SOURCE_SKILLS = ROOT / "skills"
SKILL_NAMES = (
    "amazon-analyse",
    "category-selection",
    "keyword-research",
    "review-analysis",
    "product-research",
    "product-planning",
)
MCP_DEFINITION = {
    "url": "https://mcp.sellersprite.com/mcp",
    "transport": "streamable-http",
    "headers": {"secret-key": "${SELLERSPRITE_API_KEY}"},
}


def state_dir() -> Path:
    configured = os.environ.get("OPENCLAW_STATE_DIR")
    return Path(configured).expanduser() if configured else Path.home() / ".openclaw"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=state_dir() / "skills")
    parser.add_argument("--install-deps", action="store_true")
    parser.add_argument("--configure-mcp", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def validate_sources() -> None:
    missing = [name for name in SKILL_NAMES if not (SOURCE_SKILLS / name / "SKILL.md").is_file()]
    if missing:
        raise FileNotFoundError(f"缺少 Skill: {', '.join(missing)}")


def install_all(target_root: Path, dry_run: bool = False) -> dict[str, object]:
    validate_sources()
    target_root = target_root.expanduser().resolve()
    release_root = ROOT.resolve()
    if target_root == release_root or release_root in target_root.parents:
        raise ValueError("安装目标不能位于 openclaw 发行源码目录内部")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_root = state_dir().expanduser().resolve() / "skill-backups" / "amazon-sellersprite-research" / timestamp
    transaction_id = uuid4().hex
    staged: dict[str, Path] = {}
    backups: dict[str, Path] = {}
    installed: list[str] = []

    if dry_run:
        return {
            "status": "DRY_RUN",
            "target": str(target_root),
            "skills": list(SKILL_NAMES),
            "backup": str(backup_root),
        }

    target_root.mkdir(parents=True, exist_ok=True)
    try:
        for name in SKILL_NAMES:
            staging = target_root / f".{name}.staging-{transaction_id}"
            shutil.copytree(SOURCE_SKILLS / name, staging)
            if not (staging / "SKILL.md").is_file():
                raise RuntimeError(f"暂存校验失败: {name}")
            staged[name] = staging

        for name in SKILL_NAMES:
            target = target_root / name
            if target.exists():
                backup_root.mkdir(parents=True, exist_ok=True)
                backup = backup_root / name
                shutil.move(str(target), str(backup))
                backups[name] = backup

        for name in SKILL_NAMES:
            staged[name].replace(target_root / name)
            installed.append(name)
    except Exception:
        recovery_root = backup_root / "failed-new-version"
        for name in reversed(installed):
            current = target_root / name
            if current.exists():
                recovery_root.mkdir(parents=True, exist_ok=True)
                shutil.move(str(current), str(recovery_root / name))
        for name, backup in backups.items():
            if backup.exists() and not (target_root / name).exists():
                shutil.move(str(backup), str(target_root / name))
        raise
    finally:
        for staging in staged.values():
            if staging.exists():
                shutil.rmtree(staging)

    return {
        "status": "INSTALLED",
        "target": str(target_root),
        "skills": installed,
        "backup": str(backup_root) if backups else None,
    }


def install_dependencies() -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")],
        check=True,
    )


def configure_mcp() -> None:
    executable = shutil.which("openclaw")
    if not executable:
        raise FileNotFoundError("未找到 openclaw CLI，无法自动写入 MCP 配置")
    subprocess.run(
        [executable, "mcp", "set", "sellersprite", json.dumps(MCP_DEFINITION, separators=(",", ":"))],
        check=True,
    )


def main() -> int:
    args = parse_args()
    if args.install_deps and not args.dry_run:
        install_dependencies()
    result = install_all(args.target, args.dry_run)
    if args.configure_mcp and not args.dry_run:
        configure_mcp()
        result["mcp"] = "CONFIGURED"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
