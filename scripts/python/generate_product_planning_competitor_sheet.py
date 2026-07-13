#!/usr/bin/env python3
"""Render Product Planning V1's competitor sheet from validated MCP evidence.

This tool intentionally uses only the Python standard library.  MCP calls and
Amazon-front-end collection happen before this script runs; it refuses to turn
unverified or unrelated ASINs into report content.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")

ET.register_namespace("", MAIN_NS)
ET.register_namespace("r", REL_NS)


@dataclass
class Competitor:
    asin: str
    brand: str
    title: str
    price: float | None
    rating: float | None
    rating_count: int | None
    fulfillment: str
    available_date: str
    node_id_path: str
    source: str
    features: list[str]
    positive_reviews: list[str]
    low_star_pain_points: list[str]
    product_manager_action: str
    optimization_strategy: str
    priority: str
    relevance_score: float
    system_added: bool = False
    role: str = ""

    @classmethod
    def from_mapping(cls, value: dict[str, Any], *, system_added: bool = False) -> "Competitor":
        asin = str(value.get("asin", "")).upper().strip()
        if not ASIN_RE.fullmatch(asin):
            raise ValueError(f"Invalid ASIN: {asin or '<empty>'}")
        if value.get("validated") is not True:
            raise ValueError(f"ASIN {asin} is not validated by asin_detail")
        if value.get("relevant") is not True:
            raise ValueError(f"ASIN {asin} is not relevant to the product direction")
        source = str(value.get("detailSource", ""))
        if source != "asin_detail":
            raise ValueError(f"ASIN {asin} must cite asin_detail as detailSource")
        return cls(
            asin=asin,
            brand=str(value.get("brand") or "N/A"),
            title=str(value.get("title") or "N/A"),
            price=number_or_none(value.get("price")),
            rating=number_or_none(value.get("rating")),
            rating_count=int(number_or_none(value.get("ratingCount")) or 0) or None,
            fulfillment=str(value.get("fulfillment") or "N/A"),
            available_date=str(value.get("availableDate") or "N/A"),
            node_id_path=str(value.get("nodeIdPath") or "N/A"),
            source=source,
            features=text_list(value.get("features")),
            positive_reviews=text_list(value.get("positiveReviews")),
            low_star_pain_points=text_list(value.get("lowStarPainPoints")),
            product_manager_action=str(value.get("productManagerAction") or "N/A"),
            optimization_strategy=str(value.get("optimizationStrategy") or "N/A"),
            priority=valid_priority(value.get("priority")),
            relevance_score=float(number_or_none(value.get("relevanceScore")) or 0),
            system_added=system_added,
        )


def number_or_none(value: Any) -> float | None:
    if value in (None, "", "N/A"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def text_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, "", "N/A"):
        return []
    return [str(value).strip()]


def valid_priority(value: Any) -> str:
    priority = str(value or "P1").upper()
    return priority if priority in {"P0", "P1", "P2"} else "P1"


def parse_user_asins(raw: str) -> list[str]:
    values = [part.upper() for part in re.split(r"[\s,;，；]+", raw.strip()) if part]
    if len(values) != 3:
        raise ValueError("请输入恰好 3 个 ASIN，以英文逗号、中文逗号或换行分隔。")
    if len(set(values)) != 3:
        raise ValueError("3 个 ASIN 不能重复。")
    invalid = [asin for asin in values if not ASIN_RE.fullmatch(asin)]
    if invalid:
        raise ValueError(f"ASIN 格式无效：{', '.join(invalid)}")
    return values


def percentile(values: Iterable[float], fraction: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0
    index = int(round((len(ordered) - 1) * fraction))
    return ordered[index]


def market_role(item: Competitor, pool: list[Competitor]) -> str:
    prices = [candidate.price for candidate in pool if candidate.price is not None]
    counts = [float(candidate.rating_count or 0) for candidate in pool]
    if item.rating_count and item.rating_count >= percentile(counts, 0.75):
        return "头部评价壁垒"
    if item.price is not None and prices and item.price <= percentile(prices, 0.25):
        return "低价冲击"
    if item.price is not None and prices and item.price >= percentile(prices, 0.75):
        return "高配功能差异化"
    return "主流对标"


def select_fourth(user_items: list[Competitor], candidates: list[Competitor]) -> Competitor | None:
    existing = {item.asin for item in user_items}
    remaining = [item for item in candidates if item.asin not in existing]
    if not remaining:
        return None
    all_items = user_items + remaining
    covered = {market_role(item, all_items) for item in user_items}
    for desired in ("头部评价壁垒", "低价冲击", "高配功能差异化"):
        choices = [item for item in remaining if market_role(item, all_items) == desired]
        if choices and desired not in covered:
            selected = max(choices, key=lambda item: (item.relevance_score, item.rating_count or 0))
            selected.system_added = True
            selected.role = f"系统补充：{desired}"
            return selected
    selected = max(remaining, key=lambda item: (item.relevance_score, item.rating_count or 0))
    selected.system_added = True
    selected.role = "系统补充：直接相关样本"
    return selected


def resolve_competitors(data: dict[str, Any], user_asins: list[str]) -> tuple[list[Competitor], list[dict[str, str]]]:
    section = data.get("competitorSheet") or {}
    selected_raw = section.get("selectedCompetitors") or []
    candidates_raw = section.get("candidateCompetitors") or []
    selected_by_asin = {str(item.get("asin", "")).upper(): item for item in selected_raw if isinstance(item, dict)}
    missing = [asin for asin in user_asins if asin not in selected_by_asin]
    if missing:
        raise ValueError("以下用户 ASIN 缺少 MCP asin_detail 验证结果：" + ", ".join(missing))

    user_items = [Competitor.from_mapping(selected_by_asin[asin]) for asin in user_asins]
    candidates = [Competitor.from_mapping(item) for item in candidates_raw if isinstance(item, dict)]
    for item in user_items:
        item.role = "用户指定代表竞品"
    fourth = select_fourth(user_items, candidates)
    gaps: list[dict[str, str]] = []
    if fourth is None:
        gaps.append({
            "tool": "competitor_lookup/product_research",
            "gap": "未找到可通过相关性与 asin_detail 校验的第 4 个补充竞品",
            "handling": "第 4 行显示 N/A；不虚构竞品、VOC 或结论。",
        })
        return user_items, gaps
    return user_items + [fourth], gaps


def xml_cell(column: str, row: int, value: Any, style: int, numeric: bool = False) -> str:
    ref = f"{column}{row}"
    if value in (None, ""):
        return f'<c r="{ref}" s="{style}"/>'
    if numeric and isinstance(value, (int, float)):
        return f'<c r="{ref}" s="{style}"><v>{value}</v></c>'
    return f'<c r="{ref}" s="{style}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'


def xml_row(row: int, cells: list[tuple[str, Any, int, bool]], height: int | None = None) -> str:
    attrs = f' r="{row}" spans="1:12"'
    if height:
        attrs += f' ht="{height}" customHeight="1"'
    return "<row" + attrs + ">" + "".join(xml_cell(*cell[:2], cell[2], cell[3]) for cell in cells) + "</row>"


def competitor_sheet_xml(product_idea: str, competitors: list[Competitor], gaps: list[dict[str, str]], conclusions: list[str]) -> str:
    headers = ["ASIN", "品牌", "标题", "售价$", "评分", "评分数", "履约", "上架时间", "角色", "产品经理动作"]
    rows: list[str] = []
    rows.append(xml_row(1, [("A", f"{product_idea} 竞品分析与优化策略", 18, False)] + [(col, "", 18, False) for col in "BCDEFGHIJKL"], 20))
    rows.append(xml_row(2, [("A", "口径：用户指定 3 个 ASIN，经 asin_detail 校验；系统用 competitor_lookup/product_research 补充 1 个必要竞品。卖点仅来自前端/asin_detail.features/4-5 星评论，痛点仅来自 1-3 星评论。", 10, False)] + [(col, "", 10, False) for col in "BCDEFGHIJKL"], 36))
    rows.append(xml_row(4, [(chr(65 + index), value, 5, False) for index, value in enumerate(headers)]))
    for index in range(4):
        row = 5 + index
        if index < len(competitors):
            item = competitors[index]
            values = [item.asin, item.brand, item.title, item.price, item.rating, item.rating_count, item.fulfillment, item.available_date, item.role, item.product_manager_action]
            cells = []
            for col_index, value in enumerate(values):
                cells.append((chr(65 + col_index), value if value is not None else "N/A", 6, col_index in {3, 4, 5}))
        else:
            cells = [("A", "N/A", 6, False), ("B", "N/A", 6, False), ("C", "无合格补充竞品", 6, False), ("D", "N/A", 6, False), ("E", "N/A", 6, False), ("F", "N/A", 6, False), ("G", "N/A", 6, False), ("H", "N/A", 6, False), ("I", "数据缺口", 6, False), ("J", "补抓候选池后再评估", 6, False)]
        rows.append(xml_row(row, cells, 52))

    matrix_headers = ["竞品类型", "已验证卖点", "低星痛点", "优化策略", "优先级"]
    rows.append(xml_row(30, [(chr(65 + index), value, 13, False) for index, value in enumerate(matrix_headers)]))
    for index in range(4):
        row = 31 + index
        if index < len(competitors):
            item = competitors[index]
            selling_points = "；".join(item.features + item.positive_reviews) or "N/A（缺少前端/高星证据）"
            pain_points = "；".join(item.low_star_pain_points) or "N/A（缺少低星评论证据）"
            values = [item.role, selling_points, pain_points, item.optimization_strategy, item.priority]
        else:
            values = ["数据缺口", "N/A", "N/A", "补抓合格竞品与评论数据", "P1"]
        rows.append(xml_row(row, [(chr(65 + col), value, 6, False) for col, value in enumerate(values)], 54))

    supplied = conclusions[:3]
    if not supplied:
        supplied = ["N/A（未提供有 MCP 证据支撑的样品验证、Listing 表达或定价/投放结论）"]
    if gaps:
        supplied.append("数据缺口：第 4 个直接竞品未满足校验要求，补抓前不输出新增对标结论。")
    conclusion_text = "产品经理结论：\n" + "\n".join(f"{index + 1}、{line}" for index, line in enumerate(supplied[:3]))
    rows.append(xml_row(38, [("A", conclusion_text, 12, False)] + [(col, "", 12, False) for col in "BCDEFGHIJKL"], 70))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="{MAIN_NS}" xmlns:r="{REL_NS}">
  <dimension ref="A1:L42"/>
  <sheetViews><sheetView workbookViewId="0"><selection sqref="A1"/></sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="16.5"/>
  <cols><col min="1" max="2" width="15.625" style="2" customWidth="1"/><col min="3" max="3" width="42.625" style="2" customWidth="1"/><col min="4" max="10" width="15.625" style="2" customWidth="1"/><col min="11" max="12" width="32.625" style="2" customWidth="1"/></cols>
  <sheetData>{''.join(rows)}</sheetData>
  <mergeCells count="3"><mergeCell ref="A1:L1"/><mergeCell ref="A2:L2"/><mergeCell ref="A38:L42"/></mergeCells>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
  <drawing r:id="rId1"/>
</worksheet>'''


def chart_xml(sheet_name: str, competitors: list[Competitor]) -> str:
    labels = [f"{item.brand} / {item.asin}" for item in competitors] + ["N/A"] * (4 - len(competitors))
    prices = [item.price or 0 for item in competitors] + [0] * (4 - len(competitors))
    ratings = [item.rating_count or 0 for item in competitors] + [0] * (4 - len(competitors))
    label_cache = "".join(f'<c:pt idx="{index}"><c:v>{escape(label)}</c:v></c:pt>' for index, label in enumerate(labels))
    price_cache = "".join(f'<c:pt idx="{index}"><c:v>{value}</c:v></c:pt>' for index, value in enumerate(prices))
    rating_cache = "".join(f'<c:pt idx="{index}"><c:v>{value}</c:v></c:pt>' for index, value in enumerate(ratings))
    safe_name = escape(sheet_name)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <c:lang val="zh-CN"/><c:chart><c:title><c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p><a:r><a:t>代表竞品：售价/评分数</a:t></a:r></a:p></c:rich></c:tx></c:title>
  <c:plotArea><c:layout/>
    <c:barChart><c:barDir val="col"/><c:grouping val="clustered"/><c:ser><c:idx val="0"/><c:order val="0"/><c:tx><c:v>售价$</c:v></c:tx><c:cat><c:strRef><c:f>{safe_name}!$A$5:$A$8</c:f><c:strCache><c:ptCount val="4"/>{label_cache}</c:strCache></c:strRef></c:cat><c:val><c:numRef><c:f>{safe_name}!$D$5:$D$8</c:f><c:numCache><c:formatCode>General</c:formatCode><c:ptCount val="4"/>{price_cache}</c:numCache></c:numRef></c:val></c:ser><c:axId val="100"/><c:axId val="101"/></c:barChart>
    <c:lineChart><c:grouping val="standard"/><c:ser><c:idx val="1"/><c:order val="1"/><c:tx><c:v>评分数</c:v></c:tx><c:cat><c:strRef><c:f>{safe_name}!$A$5:$A$8</c:f><c:strCache><c:ptCount val="4"/>{label_cache}</c:strCache></c:strRef></c:cat><c:val><c:numRef><c:f>{safe_name}!$F$5:$F$8</c:f><c:numCache><c:formatCode>General</c:formatCode><c:ptCount val="4"/>{rating_cache}</c:numCache></c:numRef></c:val></c:ser><c:axId val="102"/><c:axId val="103"/></c:lineChart>
    <c:catAx><c:axId val="100"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:axPos val="b"/><c:crossAx val="101"/></c:catAx>
    <c:valAx><c:axId val="101"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:axPos val="l"/><c:crossAx val="100"/></c:valAx>
    <c:valAx><c:axId val="103"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:axPos val="r"/><c:crossAx val="102"/></c:valAx>
    <c:catAx><c:axId val="102"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="1"/><c:axPos val="b"/><c:crossAx val="103"/></c:catAx>
  </c:plotArea><c:legend><c:legendPos val="r"/></c:legend><c:plotVisOnly val="1"/><c:dispBlanksAs val="gap"/></c:chart>
</c:chartSpace>'''


def plain_sheet_xml(title: str, headers: list[str], rows: list[list[str]]) -> str:
    body = [xml_row(1, [("A", title, 18, False)] + [(col, "", 18, False) for col in "BCDEFGH"])]
    body.append(xml_row(3, [(chr(65 + index), value, 5, False) for index, value in enumerate(headers)]))
    for index, values in enumerate(rows, start=4):
        body.append(xml_row(index, [(chr(65 + col), value, 6, False) for col, value in enumerate(values)]))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="{MAIN_NS}"><dimension ref="A1:H{max(4, len(rows) + 3)}"/><sheetViews><sheetView workbookViewId="0"/></sheetViews><sheetFormatPr defaultRowHeight="16.5"/><sheetData>{''.join(body)}</sheetData><mergeCells count="1"><mergeCell ref="A1:H1"/></mergeCells></worksheet>'''


def worksheet_targets(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    target_by_id = {item.attrib["Id"]: item.attrib["Target"] for item in rels}
    targets: dict[str, str] = {}
    sheets = workbook.find(f"{{{MAIN_NS}}}sheets")
    for sheet in list(sheets) if sheets is not None else []:
        rel_id = sheet.attrib[f"{{{REL_NS}}}id"]
        target = target_by_id[rel_id].replace("\\", "/")
        if target.startswith("/"):
            normalized = target.lstrip("/")
        elif target.startswith("xl/"):
            normalized = target
        else:
            normalized = "xl/" + target
        targets[sheet.attrib["name"]] = normalized
    return targets


def chart_target(archive: zipfile.ZipFile, sheet_target: str) -> str | None:
    rel_path = sheet_target.replace("xl/worksheets/", "xl/worksheets/_rels/") + ".rels"
    if rel_path not in archive.namelist():
        return None
    rels = ET.fromstring(archive.read(rel_path))
    drawing = next((item.attrib["Target"] for item in rels if item.attrib.get("Type", "").endswith("/drawing")), None)
    if not drawing:
        return None
    drawing_path = "xl/drawings/" + Path(drawing).name
    drawing_rel_path = "xl/drawings/_rels/" + Path(drawing_path).name + ".rels"
    if drawing_rel_path not in archive.namelist():
        return None
    drawing_rels = ET.fromstring(archive.read(drawing_rel_path))
    target = next((item.attrib["Target"] for item in drawing_rels if item.attrib.get("Type", "").endswith("/chart")), None)
    return "xl/charts/" + Path(target or "").name if target else None


def clean_workbook_xml(xml: bytes) -> bytes:
    text = xml.decode("utf-8")
    text = re.sub(r"<mc:AlternateContent[^>]*>.*?</mc:AlternateContent>", "", text, flags=re.DOTALL)
    return text.encode("utf-8")


def render_workbook(template: Path, output: Path, data: dict[str, Any], competitors: list[Competitor], gaps: list[dict[str, str]]) -> None:
    product_idea = str(data.get("productIdea") or data.get("meta", {}).get("productIdea") or "{{PRODUCT_IDEA}}")
    conclusions = text_list((data.get("competitorSheet") or {}).get("conclusions"))
    with zipfile.ZipFile(template) as source:
        targets = worksheet_targets(source)
        required = {"竞品分析与优化策略", "MCP原始数据", "数据来源"}
        missing = required.difference(targets)
        if missing:
            raise ValueError("模板缺少 Sheet：" + "、".join(sorted(missing)))
        replacements: dict[str, bytes] = {
            targets["竞品分析与优化策略"]: competitor_sheet_xml(product_idea, competitors, gaps, conclusions).encode("utf-8"),
            "xl/workbook.xml": clean_workbook_xml(source.read("xl/workbook.xml")),
        }
        chart = chart_target(source, targets["竞品分析与优化策略"])
        if chart:
            replacements[chart] = chart_xml("竞品分析与优化策略", competitors).encode("utf-8")

        audit_rows = [[item.asin, item.source, item.node_id_path, "用户指定" if not item.system_added else "系统补充", "已通过 asin_detail 与相关性校验"] for item in competitors]
        if gaps:
            audit_rows.extend([["N/A", gap["tool"], "N/A", "数据缺口", gap["handling"]] for gap in gaps])
        replacements[targets["MCP原始数据"]] = plain_sheet_xml("MCP 原始数据（竞品 Sheet 摘要）", ["ASIN", "详情来源", "类目节点", "样本来源", "处理结果"], audit_rows).encode("utf-8")
        source_rows = [["asin_detail", "用户 3 个 ASIN + 系统补充 ASIN", "可用", "用于竞品详情、前端卖点与相关性校验"], ["review", "4 个代表竞品，1-3 / 4-5 星", "按返回字段填写", "用于 VOC 优化矩阵；无内容时显示 N/A"], ["competitor_lookup/product_research", "产品方向 + 站点", "可用或数据缺口", "用于补充第 4 个必要竞品"]]
        source_rows.extend([[gap["tool"], "N/A", "数据缺口", gap["handling"]] for gap in gaps])
        replacements[targets["数据来源"]] = plain_sheet_xml("数据来源与缺口（竞品 Sheet）", ["工具", "入参摘要", "状态", "使用方式"], source_rows).encode("utf-8")

        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx", dir=output.parent) as temp_file:
            temp_path = Path(temp_file.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as destination:
                for entry in source.infolist():
                    destination.writestr(entry, replacements.get(entry.filename, source.read(entry.filename)))
            shutil.move(temp_path, output)
        finally:
            temp_path.unlink(missing_ok=True)


def render_blank_competitor_template(template: Path, output: Path) -> None:
    """Reset only Sheet 3 to the reusable four-row competitor layout."""
    gaps = [{
        "tool": "competitor_lookup/product_research",
        "gap": "模板不包含真实竞品数据",
        "handling": "运行时由用户指定 3 个 ASIN，并由 MCP 补充第 4 个样本。",
    }]
    with zipfile.ZipFile(template) as source:
        targets = worksheet_targets(source)
        sheet_target = targets.get("竞品分析与优化策略")
        if not sheet_target:
            raise ValueError("模板缺少 Sheet：竞品分析与优化策略")
        replacements: dict[str, bytes] = {
            sheet_target: competitor_sheet_xml("{{PRODUCT_IDEA}}", [], gaps, []).encode("utf-8"),
            "xl/workbook.xml": clean_workbook_xml(source.read("xl/workbook.xml")),
        }
        chart = chart_target(source, sheet_target)
        if chart:
            replacements[chart] = chart_xml("竞品分析与优化策略", []).encode("utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx", dir=output.parent) as temp_file:
            temp_path = Path(temp_file.name)
        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as destination:
                for entry in source.infolist():
                    destination.writestr(entry, replacements.get(entry.filename, source.read(entry.filename)))
            shutil.move(temp_path, output)
        finally:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Product Planning V1 competitor sheet from validated MCP evidence.")
    parser.add_argument("--evidence", type=Path, help="JSON evidence with competitorSheet.selectedCompetitors and candidateCompetitors.")
    parser.add_argument("--user-asins", help="Exactly three user-selected ASINs, comma/newline separated.")
    parser.add_argument("--template", type=Path, default=Path("templates/product_planning_standard_template_V1_beautified.xlsx"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--blank-template", action="store_true", help="Reset only Sheet 3 to reusable placeholders; does not use MCP evidence.")
    args = parser.parse_args()
    try:
        if args.blank_template:
            render_blank_competitor_template(args.template, args.output)
            print(f"Created reusable Sheet 3 template: {args.output}")
            return 0
        if args.evidence is None or args.user_asins is None:
            raise ValueError("--evidence and --user-asins are required unless --blank-template is used.")
        user_asins = parse_user_asins(args.user_asins)
        data = json.loads(args.evidence.read_text(encoding="utf-8"))
        competitors, gaps = resolve_competitors(data, user_asins)
        render_workbook(args.template, args.output, data, competitors, gaps)
        print(f"Generated {args.output}")
        print("Competitors: " + ", ".join(item.asin for item in competitors))
        if gaps:
            print("Data gaps: " + str(len(gaps)))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
