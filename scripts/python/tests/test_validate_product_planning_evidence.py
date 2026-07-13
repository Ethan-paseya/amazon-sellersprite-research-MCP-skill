from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


HERE = Path(__file__).resolve()
REPO = HERE.parents[3]
VALIDATOR_PATH = HERE.parents[1] / "validate_product_planning_evidence.py"
EXAMPLE_PATH = REPO / "templates" / "product_planning_evidence.example.json"

SPEC = importlib.util.spec_from_file_location("product_planning_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ProductPlanningEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def validate(self, data: dict, allow_placeholders: bool = True) -> dict:
        return VALIDATOR.validate_document(data, Path("fixture.json"), allow_placeholders)

    def test_public_example_passes(self) -> None:
        result = self.validate(copy.deepcopy(self.example))
        self.assertEqual("PASS", result["status"])

    def test_duplicate_seed_is_rejected(self) -> None:
        data = copy.deepcopy(self.example)
        data["command"]["seedAsins"][1] = data["command"]["seedAsins"][0]
        result = self.validate(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("COMMAND_SEEDS_UNIQUE", {item["code"] for item in result["errors"]})

    def test_missing_category_reason_is_rejected(self) -> None:
        data = copy.deepcopy(self.example)
        data["categorySelection"]["selected"]["reason"] = ""
        result = self.validate(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("CATEGORY_SELECTED", {item["code"] for item in result["errors"]})

    def test_incomplete_monthly_trend_is_rejected(self) -> None:
        data = copy.deepcopy(self.example)
        data["market"]["monthlyTrend"].pop()
        result = self.validate(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("MARKET_TREND_COUNT", {item["code"] for item in result["errors"]})

    def test_glance_views_proxy_is_warned_not_rejected(self) -> None:
        data = copy.deepcopy(self.example)
        data["market"]["monthlyTrend"] = [
            {
                "month": month,
                "glanceViews": 1000 + index,
                "trendMetric": "glanceViews",
                "evidenceId": f"MKT-{month}",
            }
            for index, month in enumerate(data["queryManifest"]["trendMonths"])
        ]
        result = self.validate(data)
        self.assertEqual("WARN", result["status"])
        self.assertIn("MARKET_TREND_PROXY", {item["code"] for item in result["warnings"]})

    def test_secret_is_rejected(self) -> None:
        data = copy.deepcopy(self.example)
        data["dataSources"][0]["request"] = "secret-key=replace-with-a-real-secret-value"
        result = self.validate(data)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("SAFETY_SECRET", {item["code"] for item in result["errors"]})


if __name__ == "__main__":
    unittest.main()
