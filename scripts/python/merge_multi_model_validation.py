"""Merge successful judge results from multi-model validation retries."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


VERDICT_RANK = {"FAIL": 0, "NEEDS_HUMAN_REVIEW": 1, "WARN": 2, "PASS": 3}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    successful: dict[str, dict] = {}
    attempted: list[dict] = []
    for path in args.inputs:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for judge in payload.get("judges", []):
            attempted.append({
                "provider": judge.get("provider"),
                "model": judge.get("model"),
                "ok": bool(judge.get("ok")),
                "error": judge.get("error"),
            })
            if judge.get("ok") and judge.get("parsed"):
                successful[str(judge.get("provider"))] = judge

    judges = [successful[key] for key in ("gemini", "glm") if key in successful]
    if not judges:
        consensus = {
            "verdict": "NEEDS_HUMAN_REVIEW",
            "score_0_to_5": 0,
            "rationale": "No model returned a parseable judgment.",
        }
        status = "NOT_COMPLETED"
    else:
        verdicts = [str(item["parsed"].get("verdict", "NEEDS_HUMAN_REVIEW")).upper() for item in judges]
        scores = [float(item["parsed"].get("score_0_to_5", 0)) for item in judges]
        strict = min(verdicts, key=lambda item: VERDICT_RANK.get(item, 1))
        consensus = {
            "verdict": strict,
            "score_0_to_5": round(sum(scores) / len(scores), 2),
            "rationale": "采用成功裁判中的更严格结论，并对评分取平均。",
            "modelVerdicts": [
                {
                    "provider": item["provider"],
                    "model": item["model"],
                    "verdict": str(item["parsed"].get("verdict", "NEEDS_HUMAN_REVIEW")).upper(),
                    "score_0_to_5": item["parsed"].get("score_0_to_5", 0),
                }
                for item in judges
            ],
        }
        status = "COMPLETED" if {item["provider"] for item in judges} == {"gemini", "glm"} else "PARTIAL"

    output = {
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "mode": "redacted_multi_model_judge",
        "status": status,
        "input": "redacted_eval_input_compact.md",
        "judges": judges,
        "attemptedCalls": attempted,
        "consensus": consensus,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "consensus": consensus}, ensure_ascii=False, indent=2))
    return 0 if status == "COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
