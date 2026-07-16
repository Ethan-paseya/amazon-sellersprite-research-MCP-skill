#!/usr/bin/env python3
"""Validate Product-Planning V1 normalized evidence before rendering outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
MONTH_RE = re.compile(r"^\d{6}$")
PLACEHOLDER_RE = re.compile(r"\{\{.*?\}\}|\b(?:TODO|PLACEHOLDER)\b", re.IGNORECASE)
SECRET_RE = re.compile(
    r"(?:github_pat_[A-Za-z0-9_]+|AIza[0-9A-Za-z_-]{20,}|secret-key=[^&\s\"]+|"
    r"(?:api[_-]?key|token|secret)\s*[:=]\s*[\"']?[A-Za-z0-9._-]{16,})",
    re.IGNORECASE,
)
ABSOLUTE_PATH_RE = re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)", re.IGNORECASE)
EXPECTED_SHEETS = [
    "意向产品",
    "市场分析",
    "竞品分析与优化策略",
    "SWOT分析",
    "ABA排名【季度】",
    "MCP原始数据",
    "数据来源",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="Normalized evidence JSON")
    parser.add_argument("--output", type=Path, help="Write QA result JSON")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow single-brace public template placeholders and placeholder ASINs",
    )
    return parser.parse_args()


class QA:
    def __init__(self) -> None:
        self.errors: list[dict[str, str]] = []
        self.warnings: list[dict[str, str]] = []
        self.checks: list[dict[str, str]] = []

    def error(self, code: str, message: str) -> None:
        self.errors.append({"code": code, "message": message})

    def warn(self, code: str, message: str) -> None:
        self.warnings.append({"code": code, "message": message})

    def pass_(self, code: str, message: str) -> None:
        self.checks.append({"code": code, "status": "PASS", "message": message})

    def result(self, source: Path) -> dict[str, Any]:
        status = "FAIL" if self.errors else ("WARN" if self.warnings else "PASS")
        return {
            "status": status,
            "source": source.name,
            "checkedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
            "summary": {
                "passed": len(self.checks),
                "warnings": len(self.warnings),
                "errors": len(self.errors),
            },
            "checks": self.checks,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("{") and value.endswith("}")


def valid_asin(value: Any, allow_placeholders: bool) -> bool:
    if allow_placeholders and is_placeholder(value):
        return True
    return isinstance(value, str) and bool(ASIN_RE.fullmatch(value.upper()))


def month_key(value: str) -> tuple[int, int]:
    return int(value[:4]), int(value[4:])


def validate_root(data: dict[str, Any], qa: QA) -> None:
    required = [
        "schemaVersion",
        "command",
        "queryManifest",
        "productDirection",
        "competitors",
        "categorySelection",
        "market",
        "keywords",
        "voc",
        "dataSources",
        "dataGaps",
        "decision",
        "render",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        qa.error("ROOT_REQUIRED", f"缺少根字段: {', '.join(missing)}")
    else:
        qa.pass_("ROOT_REQUIRED", "统一证据对象根字段完整")


def validate_command(data: dict[str, Any], qa: QA, allow_placeholders: bool) -> None:
    command = data.get("command", {})
    site = command.get("site")
    seeds = command.get("seedAsins", [])
    if not isinstance(site, str) or not site.strip():
        qa.error("COMMAND_SITE", "command.site 不能为空")
    if not isinstance(seeds, list) or len(seeds) != 3:
        qa.error("COMMAND_SEEDS", "命令必须包含恰好 3 个种子 ASIN")
        return
    normalized = [str(item).upper() for item in seeds]
    if len(set(normalized)) != 3:
        qa.error("COMMAND_SEEDS_UNIQUE", "3 个种子 ASIN 必须唯一")
    invalid = [str(item) for item in seeds if not valid_asin(item, allow_placeholders)]
    if invalid:
        qa.error("COMMAND_SEEDS_FORMAT", f"ASIN 格式无效: {', '.join(invalid)}")
    if not invalid and len(set(normalized)) == 3:
        qa.pass_("COMMAND_SEEDS", "3 个种子 ASIN 的数量、格式和唯一性通过")


def validate_competitors(data: dict[str, Any], qa: QA, allow_placeholders: bool) -> None:
    competitors = data.get("competitors", [])
    if not isinstance(competitors, list) or len(competitors) != 4:
        qa.error("COMPETITOR_COUNT", "最终竞品表必须固定为 4 行")
        return
    user_items = [item for item in competitors if item.get("source") == "user"]
    system_items = [item for item in competitors if item.get("source") == "system"]
    if len(user_items) != 3 or len(system_items) != 1:
        qa.error("COMPETITOR_SOURCE", "竞品必须由 3 个用户样本和 1 个系统补充样本组成")
    for index, item in enumerate(competitors, start=1):
        asin = item.get("asin")
        if asin == "N/A" and item.get("source") == "system":
            if not item.get("gapReason"):
                qa.warn("COMPETITOR_NA_REASON", "第四竞品为 N/A 时应记录 gapReason")
            continue
        if not valid_asin(asin, allow_placeholders):
            qa.error("COMPETITOR_ASIN", f"第 {index} 个竞品 ASIN 无效")
        if item.get("validation") != "PASS":
            qa.error("COMPETITOR_VALIDATION", f"第 {index} 个竞品未通过 asin_detail 校验")
        if not item.get("evidenceIds"):
            qa.error("COMPETITOR_EVIDENCE", f"第 {index} 个竞品缺少 evidenceIds")
    if not any(error["code"].startswith("COMPETITOR_") for error in qa.errors):
        qa.pass_("COMPETITORS", "三款用户竞品和一款系统补充竞品结构通过")


def validate_manifest(data: dict[str, Any], qa: QA) -> None:
    manifest = data.get("queryManifest", {})
    required = [
        "marketplace",
        "analysisMonth",
        "lastCompleteMonth",
        "trendMonths",
        "topN",
        "newProductMonths",
        "selectedNodeIdPath",
    ]
    missing = [key for key in required if manifest.get(key) in (None, "", [])]
    if missing:
        qa.error("MANIFEST_REQUIRED", f"查询口径缺少字段: {', '.join(missing)}")
        return
    analysis = str(manifest["analysisMonth"])
    complete = str(manifest["lastCompleteMonth"])
    months = [str(value) for value in manifest.get("trendMonths", [])]
    if not MONTH_RE.fullmatch(analysis) or not MONTH_RE.fullmatch(complete):
        qa.error("MANIFEST_MONTH_FORMAT", "analysisMonth 和 lastCompleteMonth 必须为 YYYYMM")
    elif month_key(complete) > month_key(analysis):
        qa.error("MANIFEST_MONTH_ORDER", "lastCompleteMonth 不能晚于 analysisMonth")
    if len(months) != 12 or len(set(months)) != 12 or any(not MONTH_RE.fullmatch(item) for item in months):
        qa.error("MANIFEST_TREND_MONTHS", "trendMonths 必须包含 12 个唯一 YYYYMM 月份")
    elif months != sorted(months, key=month_key):
        qa.error("MANIFEST_TREND_ORDER", "trendMonths 必须按升序排列")
    if not isinstance(manifest.get("topN"), int) or manifest["topN"] <= 0:
        qa.error("MANIFEST_TOPN", "topN 必须是正整数")
    if not isinstance(manifest.get("newProductMonths"), int) or manifest["newProductMonths"] <= 0:
        qa.error("MANIFEST_NEW_PRODUCT", "newProductMonths 必须是正整数")
    if not any(error["code"].startswith("MANIFEST_") for error in qa.errors):
        qa.pass_("QUERY_MANIFEST", "市场、月份、样本和新品定义口径已锁定")


def validate_category(data: dict[str, Any], qa: QA) -> None:
    selection = data.get("categorySelection", {})
    selected = selection.get("selected", {})
    required = ["nodeIdPath", "labelPath", "coverage", "relevance", "reason", "evidenceIds"]
    missing = [key for key in required if selected.get(key) in (None, "", [])]
    if missing:
        qa.error("CATEGORY_SELECTED", f"目标类目节点缺少字段: {', '.join(missing)}")
        return
    coverage = selected.get("coverage")
    if not isinstance(coverage, (int, float)) or not 0 <= coverage <= 1:
        qa.error("CATEGORY_COVERAGE", "类目覆盖率必须在 0 到 1 之间")
    elif coverage < 0.5 and not selected.get("overrideReason"):
        qa.error("CATEGORY_COVERAGE", "类目覆盖率低于 50% 时必须记录 overrideReason")
    if selected.get("relevance") not in {"PASS", "WARN"}:
        qa.error("CATEGORY_RELEVANCE", "目标节点相关性必须为 PASS 或 WARN")
    if not selection.get("candidates"):
        qa.warn("CATEGORY_CANDIDATES", "未保存类目候选池，无法复核节点选择")
    if not any(error["code"].startswith("CATEGORY_") for error in qa.errors):
        qa.pass_("CATEGORY_SELECTION", "目标类目节点具备覆盖率、相关性和选择证据")


def validate_market(data: dict[str, Any], qa: QA) -> None:
    market = data.get("market", {})
    rows = market.get("monthlyTrend", [])
    manifest_months = [str(value) for value in data.get("queryManifest", {}).get("trendMonths", [])]
    if not isinstance(rows, list) or len(rows) != 12:
        qa.error("MARKET_TREND_COUNT", "monthlyTrend 必须包含 12 行类目月度数据")
    else:
        row_months = [str(item.get("month", "")) for item in rows]
        if row_months != manifest_months:
            qa.error("MARKET_TREND_MONTHS", "monthlyTrend 月份必须与 queryManifest.trendMonths 一致")
        trend_metrics = {str(row.get("trendMetric", "sales")) for row in rows}
        uses_glance_views = trend_metrics == {"glanceViews"}
        for row in rows:
            fields = ("glanceViews",) if uses_glance_views else ("avgUnits", "avgRevenue", "avgBsr")
            for field in fields:
                if not isinstance(row.get(field), (int, float)):
                    qa.error("MARKET_TREND_VALUE", f"{row.get('month', '未知月份')} 的 {field} 不是数值")
            if not row.get("evidenceId"):
                qa.error("MARKET_TREND_EVIDENCE", f"{row.get('month', '未知月份')} 缺少 evidenceId")
        if not any(error["code"].startswith("MARKET_TREND_") for error in qa.errors):
            if uses_glance_views:
                qa.warn("MARKET_TREND_PROXY", "连续 12 个月销量趋势缺失，当前使用 MCP Glance Views 作为需求趋势代理")
            else:
                qa.pass_("MARKET_TREND", "12 个月类目趋势完整且可追溯")

    distributions = market.get("distributions", {})
    for name, distribution in distributions.items():
        items = distribution.get("items", []) if isinstance(distribution, dict) else []
        shares = [item.get("share") for item in items if isinstance(item.get("share"), (int, float))]
        if not items:
            qa.warn("MARKET_DISTRIBUTION_EMPTY", f"{name} 分布为空")
            continue
        if len(shares) != len(items):
            qa.warn("MARKET_DISTRIBUTION_SHARE", f"{name} 分布存在缺失 share")
        elif not 0.97 <= sum(shares) <= 1.03:
            qa.warn("MARKET_DISTRIBUTION_TOTAL", f"{name} 分布占比合计为 {sum(shares):.4f}")
    listing_age = distributions.get("listingAge", {})
    analysis = data.get("queryManifest", {}).get("analysisMonth")
    if listing_age and listing_age.get("month") != analysis and not listing_age.get("fallbackReason"):
        qa.error("LISTING_AGE_FALLBACK", "上架时间分布改用其他月份时必须记录 fallbackReason")


def validate_keywords(data: dict[str, Any], qa: QA) -> None:
    keywords = data.get("keywords", {})
    requested = keywords.get("requestedCount")
    returned = keywords.get("returnedCount")
    items = keywords.get("items", [])
    missing = keywords.get("missing", [])
    if not isinstance(requested, int) or requested < 0 or not isinstance(returned, int) or returned < 0:
        qa.error("KEYWORD_COUNTS", "关键词 requestedCount/returnedCount 必须是非负整数")
        return
    if returned != len(items):
        qa.error("KEYWORD_RETURNED", "returnedCount 与 items 行数不一致")
    if requested != returned + len(missing):
        qa.error("KEYWORD_COVERAGE", "requestedCount 必须等于 returnedCount 加 missing 数量")
    for item in items:
        if not item.get("keyword") or not item.get("evidenceId"):
            qa.error("KEYWORD_EVIDENCE", "关键词行必须包含 keyword 和 evidenceId")
        for field in ("searches", "purchases", "ppc", "products"):
            if not isinstance(item.get(field), (int, float)):
                qa.warn("KEYWORD_FIELD", f"关键词 {item.get('keyword', 'N/A')} 缺少数值字段 {field}")
    if not any(error["code"].startswith("KEYWORD_") for error in qa.errors):
        qa.pass_("KEYWORDS", "关键词请求、返回与缺失口径一致")


def validate_voc(data: dict[str, Any], qa: QA) -> None:
    voc = data.get("voc", {})
    min_positive = voc.get("minimumPositiveSamples", 0)
    min_negative = voc.get("minimumNegativeSamples", 0)
    for item in voc.get("competitors", []):
        positive = item.get("positiveCount", 0)
        negative = item.get("negativeCount", 0)
        if positive < min_positive and item.get("positiveInterpretation") != "sample_insufficient":
            qa.warn("VOC_POSITIVE_SAMPLE", f"{item.get('asin', 'N/A')} 正向样本不足但未标记")
        if negative < min_negative and item.get("negativeInterpretation") != "sample_insufficient":
            qa.warn("VOC_NEGATIVE_SAMPLE", f"{item.get('asin', 'N/A')} 负向样本不足但未标记")
        if not item.get("evidenceIds"):
            qa.error("VOC_EVIDENCE", f"{item.get('asin', 'N/A')} VOC 缺少 evidenceIds")


def collect_evidence_ids(data: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for source in data.get("dataSources", []):
        value = source.get("evidenceId")
        if value:
            result.add(str(value))
    for competitor in data.get("competitors", []):
        result.update(str(value) for value in competitor.get("evidenceIds", []))
    for row in data.get("market", {}).get("monthlyTrend", []):
        if row.get("evidenceId"):
            result.add(str(row["evidenceId"]))
    for item in data.get("keywords", {}).get("items", []):
        if item.get("evidenceId"):
            result.add(str(item["evidenceId"]))
    for item in data.get("voc", {}).get("competitors", []):
        result.update(str(value) for value in item.get("evidenceIds", []))
    return result


def validate_decision(data: dict[str, Any], qa: QA) -> None:
    decision = data.get("decision", {})
    if decision.get("status") not in {"进入", "观察", "放弃"}:
        qa.error("DECISION_STATUS", "最终决策必须为 进入、观察 或 放弃")
    known_ids = collect_evidence_ids(data)
    for section in ("gates", "actions"):
        for item in decision.get(section, []):
            references = [str(value) for value in item.get("evidenceIds", [])]
            if not references:
                qa.error("DECISION_EVIDENCE", f"decision.{section} 存在无证据项")
            unknown = [value for value in references if value not in known_ids]
            if unknown:
                qa.warn("DECISION_UNKNOWN_EVIDENCE", f"decision.{section} 引用未登记证据: {', '.join(unknown)}")
    actions = decision.get("actions", [])
    if len(actions) > 3:
        qa.error("DECISION_ACTION_COUNT", "产品经理行动不得超过 3 条")
    if not any(error["code"].startswith("DECISION_") for error in qa.errors):
        qa.pass_("DECISION", "决策、门禁和行动均具备证据引用")


def validate_render(data: dict[str, Any], qa: QA) -> None:
    render = data.get("render", {})
    if render.get("sheetOrder") != EXPECTED_SHEETS:
        qa.error("RENDER_SHEETS", "Sheet 顺序必须与 Product-Planning V1 标准一致")
    if not render.get("markdownTitle") or render.get("markdownTitle") != render.get("workbookTitle"):
        qa.error("RENDER_TITLE", "Markdown 与 Excel 标题必须非空且一致")
    if not any(error["code"].startswith("RENDER_") for error in qa.errors):
        qa.pass_("RENDER", "双格式标题与 V1 Sheet 顺序一致")


def validate_safety(data: dict[str, Any], qa: QA, allow_placeholders: bool) -> None:
    serialized = json.dumps(data, ensure_ascii=False)
    if SECRET_RE.search(serialized):
        qa.error("SAFETY_SECRET", "证据对象疑似包含 API key、token 或 secret-key URL")
    if ABSOLUTE_PATH_RE.search(serialized):
        qa.error("SAFETY_PATH", "证据对象包含绝对本地路径")
    if PLACEHOLDER_RE.search(serialized):
        qa.error("SAFETY_TEMPLATE_TOKEN", "证据对象包含双花括号、TODO 或 PLACEHOLDER 模板标记")
    if not allow_placeholders and re.search(r"\{[A-Z][A-Z0-9_]+\}", serialized):
        qa.error("SAFETY_PUBLIC_PLACEHOLDER", "正式证据对象仍包含公开示例占位符")
    if not any(error["code"].startswith("SAFETY_") for error in qa.errors):
        qa.pass_("SAFETY", "未发现密钥、绝对路径或正式输出占位符")


def validate_document(
    data: dict[str, Any], source: Path, allow_placeholders: bool = False
) -> dict[str, Any]:
    """Run all Product-Planning evidence checks and return a QA result."""
    qa = QA()
    validate_root(data, qa)
    validate_command(data, qa, allow_placeholders)
    validate_competitors(data, qa, allow_placeholders)
    validate_manifest(data, qa)
    validate_category(data, qa)
    validate_market(data, qa)
    validate_keywords(data, qa)
    validate_voc(data, qa)
    validate_decision(data, qa)
    validate_render(data, qa)
    validate_safety(data, qa, allow_placeholders)
    return qa.result(source)


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"无法读取证据文件: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("证据文件根节点必须是 JSON object", file=sys.stderr)
        return 2

    result = validate_document(data, args.evidence, args.allow_placeholders)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
