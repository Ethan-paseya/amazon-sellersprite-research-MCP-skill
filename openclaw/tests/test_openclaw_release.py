#!/usr/bin/env python3
"""Regression tests for the OpenClaw release installer and verifier."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_module("openclaw_installer", ROOT / "install.py")
verifier = load_module("openclaw_verifier", ROOT / "verify.py")


class OpenClawReleaseTests(unittest.TestCase):
    def test_release_passes_offline_verification(self) -> None:
        result = verifier.verify_release(ROOT)
        self.assertEqual("PASS", result["status"], result)

    def test_installer_preserves_previous_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            target = temp / "skills"
            previous = target / "amazon-analyse"
            previous.mkdir(parents=True)
            (previous / "SKILL.md").write_text("old version", encoding="utf-8")
            old_state = os.environ.get("OPENCLAW_STATE_DIR")
            os.environ["OPENCLAW_STATE_DIR"] = str(temp / "state")
            try:
                result = installer.install_all(target)
            finally:
                if old_state is None:
                    os.environ.pop("OPENCLAW_STATE_DIR", None)
                else:
                    os.environ["OPENCLAW_STATE_DIR"] = old_state

            self.assertEqual("INSTALLED", result["status"])
            self.assertEqual(6, len(result["skills"]))
            self.assertIn("name: amazon-analyse", (target / "amazon-analyse" / "SKILL.md").read_text(encoding="utf-8"))
            backup = Path(result["backup"])
            self.assertEqual("old version", (backup / "amazon-analyse" / "SKILL.md").read_text(encoding="utf-8"))

    def test_dry_run_does_not_write_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "skills"
            result = installer.install_all(target, dry_run=True)
            self.assertEqual("DRY_RUN", result["status"])
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
