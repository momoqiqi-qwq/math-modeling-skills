"""冒烟测试: mathmodel-scoring-gate 能完成一次真实评分判定。

用法:
    python tests/smoke_test.py

覆盖:
1. 合法 critique (cumcm stage 1) -> exit 0, decision_log 落盘并记录 verdict
2. 故意写错 dim key        -> 非 0 退出, decision_log 不被污染
3. stage 5 per-Qi 聚合     -> exit 0, stages.5.aggregate 落地
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "score_artifact.py"
TEMPLATE = ROOT / "references" / "decision_log.template.json"

STAGE1_DIMS = [
    "1_three_options_depth",
    "2_team_strength_match",
    "3_risk_identification",
    "4_time_feasibility",
    "5_decision_record_quality",
]


def run(args, cwd):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT), *args],
        cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def critique(stage, dims, values, iteration=0, issues=None, verdict="refine"):
    scores = {d: {"score": v, "evidence": f"冒烟测试证据: {d} 实测 {v}/10"} for d, v in zip(dims, values)}
    return {
        "stage_id": stage,
        "iteration": iteration,
        "scores": scores,
        "min_score": min(values),
        "mean_score": sum(values) / len(values),
        "issues": issues or [],
        "verdict": verdict,
    }


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        state = tmp / "state"
        state.mkdir()
        log = state / "decision_log.json"
        log.write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")

        # --- case 1: 合法 stage 1, 分数够 pass ---
        c1 = tmp / "critique_ok.json"
        c1.write_text(json.dumps(critique(1, STAGE1_DIMS, [8, 8, 8, 9, 8], verdict="pass")), encoding="utf-8")
        r1 = run(["--stage", "1", "--critique", str(c1), "--decision-log", str(log),
                  "--competition", "cumcm"], tmp)
        assert r1.returncode == 0, f"case1 应通过, 实际退出 {r1.returncode}\nSTDOUT:\n{r1.stdout}\nSTDERR:\n{r1.stderr}"
        data = json.loads(log.read_text(encoding="utf-8"))
        entry = data["scores"]["1"][-1]
        assert entry["verdict"] in {"pass", "pass_early"}, entry
        assert entry["min"] == 8, entry
        print(f"[1/3] 合法评分 OK verdict={entry['verdict']} min={entry['min']} mean={entry['mean']}")

        # --- case 2: 错 dim key 必须被拦 ---
        bad_dims = STAGE1_DIMS[:4] + ["5_wrong_key"]
        c2 = tmp / "critique_bad.json"
        c2.write_text(json.dumps(critique(1, bad_dims, [8, 8, 8, 8, 8], verdict="pass")), encoding="utf-8")
        before = len(json.loads(log.read_text(encoding="utf-8"))["scores"]["1"])
        r2 = run(["--stage", "1", "--critique", str(c2), "--decision-log", str(log),
                  "--competition", "cumcm"], tmp)
        assert r2.returncode != 0, f"case2 应失败, 实际退出 {r2.returncode}\n{r2.stdout}"
        after = len(json.loads(log.read_text(encoding="utf-8"))["scores"]["1"])
        assert before == after, "失败的评分不应写入 decision_log"
        print(f"[2/3] 错 dim key 被拦 OK (exit={r2.returncode})")

        # --- case 3: stage 5 per-Qi 聚合 ---
        qi_results = {
            "qi_results": [
                {"qi": "Q1", "min": 8, "mean": 8.4, "issues": []},
                {"qi": "Q2", "min": 7, "mean": 8.0,
                 "issues": [{"severity": "medium", "where": "4.2 灵敏度", "fix": "补 ±10% 扰动表"}]},
            ],
            "qi_weights": [1.0, 1.2],
        }
        c3 = tmp / "qi_results.json"
        c3.write_text(json.dumps(qi_results), encoding="utf-8")
        r3 = run(["--stage", "5", "--mode", "aggregate_qi", "--qi-results", str(c3),
                  "--decision-log", str(log)], tmp)
        assert r3.returncode == 0, f"case3 应通过, 实际退出 {r3.returncode}\nSTDOUT:\n{r3.stdout}\nSTDERR:\n{r3.stderr}"
        data = json.loads(log.read_text(encoding="utf-8"))
        agg = data["stages"]["5"]["aggregate"]
        assert agg["method"] == "per_qi_weighted", agg
        assert len(data["stages"]["5"]["qi_weights"]) == 2, data["stages"]["5"]
        print(f"[3/3] per-Qi 聚合 OK verdict={agg['verdict']} weighted_mean={agg['weighted_mean']}")

    print("SMOKE OK")


if __name__ == "__main__":
    main()
