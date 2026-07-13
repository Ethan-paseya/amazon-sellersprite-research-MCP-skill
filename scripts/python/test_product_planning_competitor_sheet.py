#!/usr/bin/env python3
"""Regression tests for the Product Planning V1 competitor-sheet renderer."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent))
import generate_product_planning_competitor_sheet as renderer


def record(asin: str, price: float, rating_count: int, score: float = 0.9) -> dict:
    return {
        "asin": asin,
        "validated": True,
        "relevant": True,
        "detailSource": "asin_detail",
        "brand": f"Brand-{asin[-2:]}",
        "title": f"Relevant product {asin}",
        "price": price,
        "rating": 4.5,
        "ratingCount": rating_count,
        "fulfillment": "FBA",
        "availableDate": "2026-01-01",
        "nodeIdPath": "1:2:3",
        "features": ["feature evidence"],
        "positiveReviews": ["positive review evidence"],
        "lowStarPainPoints": ["low-star pain point"],
        "productManagerAction": "validated PM action",
        "optimizationStrategy": "evidence-backed optimization",
        "priority": "P0",
        "relevanceScore": score,
    }


def evidence(with_candidate: bool = True) -> dict:
    data = {
        "productIdea": "test product direction",
        "competitorSheet": {
            "selectedCompetitors": [
                record("A1B2C3D4E5", 19.99, 80),
                record("F1G2H3I4J5", 9.99, 30),
                record("K1L2M3N4O5", 25.99, 40),
            ],
            "candidateCompetitors": [],
            "conclusions": [
                "样品验证结论，证据来自低星评论。",
                "Listing 表达结论，证据来自前端和高星评论。",
                "定价结论，证据来自 4 个竞品价格带。",
            ],
        },
    }
    if with_candidate:
        data["competitorSheet"]["candidateCompetitors"].append(record("P1Q2R3S4T5", 7.99, 600, 0.95))
    return data


def competitor_chart_xml(archive: zipfile.ZipFile) -> str:
    for entry in archive.namelist():
        if not entry.startswith("xl/charts/") or not entry.endswith(".xml"):
            continue
        xml = archive.read(entry).decode("utf-8")
        if "$D$5:$D$8" in xml and "$F$5:$F$8" in xml:
            return xml
    raise AssertionError("Competitor chart with four-row price and rating ranges was not found")


class CompetitorSheetTests(unittest.TestCase):
    def test_rejects_duplicate_asins(self) -> None:
        with self.assertRaises(ValueError):
            renderer.parse_user_asins("A1B2C3D4E5,A1B2C3D4E5,F1G2H3I4J5")

    def test_adds_one_system_competitor(self) -> None:
        user_asins = renderer.parse_user_asins("A1B2C3D4E5,F1G2H3I4J5,K1L2M3N4O5")
        competitors, gaps = renderer.resolve_competitors(evidence(), user_asins)
        self.assertEqual(4, len(competitors))
        self.assertTrue(competitors[-1].system_added)
        self.assertEqual([], gaps)

    def test_records_gap_when_no_candidate_is_usable(self) -> None:
        user_asins = renderer.parse_user_asins("A1B2C3D4E5,F1G2H3I4J5,K1L2M3N4O5")
        competitors, gaps = renderer.resolve_competitors(evidence(False), user_asins)
        self.assertEqual(3, len(competitors))
        self.assertEqual(1, len(gaps))

    def test_writes_four_row_chart_and_removes_local_path(self) -> None:
        root = Path(__file__).resolve().parents[2]
        template = root / "templates" / "product_planning_standard_template_V1_beautified.xlsx"
        user_asins = renderer.parse_user_asins("A1B2C3D4E5,F1G2H3I4J5,K1L2M3N4O5")
        competitors, gaps = renderer.resolve_competitors(evidence(), user_asins)
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "planning.xlsx"
            renderer.render_workbook(template, output, evidence(), competitors, gaps)
            with zipfile.ZipFile(output) as archive:
                for entry in archive.namelist():
                    if entry.endswith(".xml"):
                        ET.fromstring(archive.read(entry))
                workbook_xml = archive.read("xl/workbook.xml").decode("utf-8")
                self.assertNotIn(str(Path.home()), workbook_xml)
                chart = competitor_chart_xml(archive)
                self.assertIn("$D$5:$D$8", chart)
                self.assertIn("$F$5:$F$8", chart)
                sheet = archive.read("xl/worksheets/sheet3.xml").decode("utf-8")
                self.assertIn("P1Q2R3S4T5", sheet)
                self.assertIn("系统补充", sheet)

    def test_blank_template_keeps_four_row_chart_range(self) -> None:
        root = Path(__file__).resolve().parents[2]
        template = root / "templates" / "product_planning_standard_template_V1_beautified.xlsx"
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "blank.xlsx"
            renderer.render_blank_competitor_template(template, output)
            with zipfile.ZipFile(output) as archive:
                sheet = archive.read("xl/worksheets/sheet3.xml").decode("utf-8")
                chart = competitor_chart_xml(archive)
                self.assertNotIn("DJI Osmo", sheet)
                self.assertIn("$D$5:$D$8", chart)
                self.assertIn("$F$5:$F$8", chart)


if __name__ == "__main__":
    unittest.main()
