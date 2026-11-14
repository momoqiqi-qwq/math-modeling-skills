---
name: mathmodel-scoring-gate
description: 数学建模的可复算评分门禁。把一份 5 维 critic JSON 变成加权分与七档 verdict（block/pass_early/pass/pass_with_review/refine/refine_partial/carryover），写进 state/decision_log.json，供 M1/P1/P2/W1/W2 门禁与 CUMCM/MCM/电工杯阶段放行使用。触发词：评分、打分、verdict、门禁判定、加权评分、够不够格、是否放行、critic 回执、per-Qi 聚合、子问合并。
---

# 数学建模评分门禁 · mathmodel-scoring-gate

把「这东西能不能过」从口头一致变成**可复算、可留痕、两次判定可比**的判定：5 维 critic → 加权分 → 七档 verdict → 写进 `state/decision_log.json`。

## 什么时候用 / 什么时候别用

| 用 | 别用（去做别的） |
|---|---|
| 要给一段产物下放行/返工判定，且必须留痕复算 | 只是想把文字改顺（本地 math-modeling 论文手） |
| 两个 AI 评审团意见不一，需要一个裁判尺 | 要挑算法（assets/01-07 算法说明） |
| 同一产物改了两轮，要比较「有没有真的变好」 | 只查格式合规（bzd-paper-format-checker） |
| 多子问题要合并成一个总判定（per-Qi 聚合） | 要生成论文/图表（本地 math-modeling 三角色） |
| 赛场推进阶段，要给下一步动作 | 要查竞赛规则原文（mathmodel-competition-suite） |

## 三步上手

**第 0 步 · 初始化状态（只做一次）**

```bash
mkdir -p state
cp references/decision_log.template.json state/decision_log.json
# PowerShell: New-Item -ItemType Directory -Force state | Out-Null; Copy-Item references/decision_log.template.json state/decision_log.json
```

状态文件不存在时脚本会硬报 `FileNotFoundError`（故意如此：不许隐式建状态）。

**第 1 步 · 单阶段评分**

```bash
python scripts/score_artifact.py --stage 3 --critique critique_v0.json \
  --competition cumcm --task-type A_optimization
```

**第 2 步 · stage 5（建模主循环）每个子问先分别评，再聚合**

```bash
python scripts/score_artifact.py --stage 5 --variant per_qi --qi-id Q1 --critique critique_q1.json
python scripts/score_artifact.py --stage 5 --mode aggregate_qi --qi-results qi_results.json
```

`qi_results.json` 形状：

```json
{"qi_results": [
  {"qi": "Q1", "min": 7, "mean": 8.2, "issues": [{"severity": "medium", "where": "3.2 约束", "fix": "补一阶必要条件推导"}]},
  {"qi": "Q2", "min": 8, "mean": 8.6, "issues": []}
], "qi_weights": [1.0, 1.2]}
```

## critique JSON 契约（少一个字段、错一个 key 就是 FAIL）

```json
{
  "stage_id": 3,
  "iteration": 0,
  "scores": {
    "1_candidate_diversity": {"score": 8, "evidence": "列出 4 类候选模型并给淘汰理由"},
    "2_selection_rationale": {"score": 7, "evidence": "按数据规模与求解时间二选一"},
    "3_naming_variant": {"score": 8, "evidence": "模型名与题设术语对齐"},
    "4_solver_feasibility": {"score": 7, "evidence": "2 万变量内可用内点法 30 秒解出"},
    "5_literature_support": {"score": 6, "evidence": "仅 1 篇支撑，需补"}
  },
  "min_score": 6,
  "mean_score": 7.2,
  "issues": [
    {"severity": "medium", "where": "3.1 选型表", "fix": "补第 5 个候选并说明剔除原因", "anti_pattern_id": "A3"}
  ],
  "verdict": "refine"
}
```

硬规则：

- `stage_id` 必须**等于** `--stage`。
- `iteration` 非负整数，第 0 次写 0。
- `scores` 恰好 5 个 dim，key 必须与阶段白名单**完全一致**（多一个、少一个、大小写不同都报错）。白名单见 `references/rubrics.md` 对应阶段；竞赛 overlay 见 `competitions/<comp>/rubric_overlay.json`。
- 每个 dim = `{"score": 1..10 的数值, "evidence": 非空字符串}`；evidence 写实测/位置，不写「较好」「较完善」。
- `min_score` 必须等于 5 个分的最小值（精确相等，不是约等于）。
- `mean_score` 必须等于 5 个分的算术平均，误差 ≤ 0.02。
- `issues` 数组，**最多 5 条**。超过 5 条意味着该重做整个阶段，不是精修。
- 每条 issue：`severity ∈ {high, medium, low}`、`where` 非空（定位到章节/公式/文件行）、`fix` 非空（可执行动作）、`anti_pattern_id` 形如 `A3` 或不填。
- `verdict` 字段照写，但脚本会**重算并覆盖**它（防自评放水）。重算结果以脚本输出为准。

## verdict 七档（唯一真源，别自己记别处版本）

单阶段（`compute_verdict`，优先级从高到低）：

1. 任一 issue `severity=high` → `block`
2. raw_min ≥ 9 且 weighted_mean ≥ 9 → `pass_early`
3. raw_min ≥ 7 且 weighted_mean ≥ 8 → `pass`
4. 其余 → `refine`

stage 5 聚合（`compute_stage5_verdict`）：每个 Qi 先判内部状态（有 high → block；min≥7 且 mean≥8 → pass；min≥7 → mark_for_review；否则 refine），然后：

- 有 block Qi → `block`
- 有 refine Qi：部分挂 → `refine_partial`；全挂 → `refine`
- 只有 mark_for_review：weighted_min≥7 且 weighted_mean≥8 → `pass_with_review`，否则 `refine`
- 全 pass：weighted_min≥9 且 weighted_mean≥9 → `pass_early`；≥7/≥8 → `pass`

`carryover`：迭代次数达到 `--max-iter`（默认 3）仍未达标 → 标记 carryover，停止在门里磨，交给跨阶段回检。

## 传给本地 math-modeling 五道门的映射

本地 `math-modeling` 的 M1/P1/P2/W1/W2 只认三态回执（PASS / FAIL / BLOCKED）。评分是给它加一个**数字骨架**，不替代回执：

| verdict | 门禁回执 | 回执里必须写 |
|---|---|---|
| block | BLOCKED | 全部 high-severity issue，等人工介入 |
| refine / refine_partial / carryover | FAIL | 本轮 issue 清单 + 下一轮 iteration |
| pass_with_review | PASS（附条件） | review_qis 原样抄进「返工」段，不许省 |
| pass / pass_early | PASS | min、weighted_mean、所用 competition/task_type |

| 本地门禁 | 用哪个 stage 评分 | 判定重点 |
|---|---|---|
| M1 建模终检 | 3 + 4 | 选型依据、求解可行性、假设可支撑、符号唯一 |
| P1 最小可运行结果 | 5（per_qi，单子问） | 该子问跑通、结果可追溯 |
| P2 编程终检 | 5（per_qi）+ 6 | 代码与模型一致、灵敏度真做了 |
| W1 证据大纲 | 7 + 8 | 结论有出处、章节齐、图表引用闭合 |
| W2 论文终检 | 8 + 9 | 摘要信息链、去占位、提交合规 |

## 加权怎么算

`weighted_mean = Σ(score_i × w_i) / Σ(w_i)`，`raw_min` **不加权**，仍负责触发「某一维太低」。

- 权重表：`config/dim_weights.json` → `[competition][task_type][stage][dim]`
- 未列出的 dim = 1.0；权重被 clamp 到 `[0.7, 1.5]`
- `task_type=default` = 全 1.0 = 与不加权等价（老逻辑兼容）
- 题型代码不确定就留 `default`，并把实际题型写进 `decision_log.task_type` 而不是猜

## empirical 分位的诚实度（会被问到的坑）

- **CUMCM**：59 份可提取样本（来源清单 91 份），p25/p50/p75 只用来提示「异常」，不是获奖线、不是官方阈值。
- **MCM / 电工杯**：样本量 n=0。禁止推断任何数值门槛、禁止把占位值当基准。
- 任何情况下都不许说「到这条线就能拿奖」。

## 常见 FAIL 与改法

| 报错 | 真因 | 改法 |
|---|---|---|
| `缺少 keys` / `dim key 不匹配` | key 自造或抄了别的阶段 | 去 `references/rubrics.md` 抄该阶段 5 个 key，一字不改 |
| `min_score 与 scores 不一致` | 手抄分数 | 用脚本算，别手写 |
| `mean_score 与 scores 不一致` | 同上 | 同上 |
| `issues 长度 6 > 5` | 问题太多 | 回整个阶段重做，别硬塞 |
| `decision_log.json 不存在` | 没初始化状态 | 先 copy 模板 |
| 输出 verdict 比预期低 | 权重/分数不够 | 改产物，不是改 JSON |
| `verdict 必须 ∈ {...}` | 写了中文或自创档位 | 用七档英文原词 |

## 文件

| 路径 | 作用 |
|---|---|
| `scripts/score_artifact.py` | 全部逻辑（校验 → 加权 → verdict → 写状态） |
| `config/dim_weights.json` | competition × task_type × stage × dim 权重表 |
| `references/rubrics.md` | 各阶段 5 维定义与打分锚点（写 critique 前读对应段落） |
| `references/stage1_selection.md` | stage 1 选题/路线双层判据：0–5 分、三组混合权重（0.45:0.55、0.70:0.30、0.85:0.15）、判定线 4.4/3.5 与 0.02 缓冲；`selection_score` 独立于论文 `weighted_mean` |
| `references/award_patterns_notes.md` | 获奖论文拆解清单：子问角色链、题型模式库、反驳式选型、风险分级；填 stage1_selection 时配读 |
| `references/feedback_layer1_critic.md` | L1 critic 的角色纪律与输出格式 |
| `references/decision_log.template.json` | 状态文件模板（复制到 `state/decision_log.json`） |
| `competitions/<comp>/{rubric_overlay,topic_specs,empirical}.json` | 三竞赛的维度覆盖、题型表、观察分位 |
| `tests/smoke_test.py` | 冒烟测试：正常评分通过 + 错 key 被拦 |

自检：`python tests/smoke_test.py`（期望最后一行 `SMOKE OK`）。


## 独立使用（本 skill 自包含）

不需要任何其它 skill 在场：`scripts/score_artifact.py` 只读你传给它的产物路径与 `state/decision_log.json`，不联网、不调用模型、不依赖外部规范文件。

三条最容易被忽略的：**score 高 ≠ 合规**（verdict 只是放行判据，页数/匿名/AI 声明仍要独立核）；**门禁 PASS 后产物再变，PASS 立即失效**；**`--stage` 一次只传一个**，别把两个阶段塞进一次评分。

## 可选组合（装了才用，不装不影响）

如果同一台机器上还有 `mathmodel-competition-suite`（规则与写法标准）和 `math-modeling`（三角色生产线），三者关系是：竞赛包给标准、本 skill 给裁判尺、math-modeling 给生产线，**互不替代**。接线方式由使用方决定，本 skill 不读取它们的任何文件；跨 skill 引用一律写全 `<skill>/references/...` 相对路径，不写本机绝对路径。

## 来源与许可

判定内核与配置取自 [handsomeZR-netizen/mathmodel-skill](https://github.com/handsomeZR-netizen/mathmodel-skill)（MIT，见 `LICENSE-mathmodel-skill.txt` 与 `THIRD_PARTY_NOTICES.md`）：`score_artifact.py`、`config/dim_weights.json`、`references/rubrics.md`、`references/feedback_layer1_critic.md`、`templates/shared/decision_log.json`、三竞赛 config JSON。**脚本逻辑未改动**，仅重排目录；本 SKILL.md、tests 与目录说明为本 skill 新增。

**SOT 记录（本机新增）** · 2026-11-14 · 新增 `references/stage1_selection.md`（stage 1 选题/路线双层判据，含三组混合权重、4.4/3.5 判定线与 0.02 缓冲、六个必填证据字段）与 `references/award_patterns_notes.md`（获奖论文拆解的中文可执行清单），判据结构借鉴 [y3519712124-ui/math-modeling-contest-route-selection](https://github.com/y3519712124-ui/math-modeling-contest-route-selection)（MIT）；同日仅在 SKILL.md 文件表加两行指针，`score_artifact.py`、`config/dim_weights.json` 与既有 rubrics 未改动。
