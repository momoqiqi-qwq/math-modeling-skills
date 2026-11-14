# Stage 1 选题与路线双层判据

> 本文件是 stage 1（选题）在 5 维 rubric **之外**的前置量化层：回答「这笔押注值不值得下」，不替代 `references/rubrics.md` 的 `1_three_options_depth / 2_team_strength_match / 3_risk_identification / 4_time_feasibility / 5_decision_record_quality`，也不新增 verdict 档位。
>
> 判据结构借鉴 [y3519712124-ui/math-modeling-contest-route-selection](https://github.com/y3519712124-ui/math-modeling-contest-route-selection)（MIT）：双层骨架、路线优先、反驳式选型与反同质化清单来自该仓库。权重、判定线、证据字段约束与落盘形状按本 skill 既有口径重写，凡与原文数值不同处均在正文注明。

## 0. 一句话口径

选题层判「这题做不做得出来」，路线层判「做出来赢不赢」，子问题链判「四问连不连成一条推理线」。三层各自 0–5 分，再用三组固定权重混成一个 `selection_score`。

## 1. 三层判据

全部 0–5 分，允许 0.1 步长。分数只在**同一轮、同一张表**内可比，跨轮比较必须重读上一轮的表。

### 1.1 选题层（7 条，Σw = 1.00）

| 判据 | 权重 | 判什么 | 5 分信号 |
|---|---:|---|---|
| `feasibility` | 0.18 | 72 小时内能否交出模型、代码、图表、论文 | 第一天能出基线结果 |
| `data_or_parameter_access` | 0.14 | 数据/参数可得，或可被有依据地估计 | 每个输入都有来源或边界 |
| `differentiation` | 0.18 | 是否只可能交出一份"通用 AI 答案" | 有一个只有本题才成立的切入角 |
| `validation_strength` | 0.16 | 结果能否被比较、扰动、外校 | 存在能推翻结论的测试 |
| `method_fit` | 0.12 | 方法是否天然回答所问，而非装饰 | 换掉方法，交付物形式就要变 |
| `narrative_power` | 0.10 | 能否从变量讲到决策 | 摘要一段话能说清主线 |
| `risk_control` | 0.12 | 有没有触发条件明确的退路 | 退路带 trigger/action/deadline |

### 1.2 路线层（8 条，Σw = 1.00）

| 判据 | 权重 | 判什么 |
|---|---:|---|
| `route_problem_fit` | 0.16 | 路线是否直接产出题目要的那个决策/数值/排序 |
| `engineering_solvability` | 0.16 | 队伍能否在赛程内写完、调通、重跑 |
| `data_parameter_control` | 0.14 | 输入是否可控，失控是否有界 |
| `validation_design` | 0.14 | 是否指名了基线/消融/灵敏度/极限情形中的哪一个 |
| `route_differentiation` | 0.14 | 相对大众解法，差异是否看得见 |
| `paper_explainability` | 0.10 | 方程、步骤、结果能否被写清 |
| `implementation_cost_control` | 0.08 | 运行时间与调试成本是否封顶 |
| `fallback_robustness` | 0.08 | 主路线崩了，纸是否仍然完整 |

### 1.3 子问题链层（6 条，Σw = 1.00，仅当题面 ≥2 问时启用）

| 判据 | 权重 | 判什么 |
|---|---:|---|
| `role_alignment` | 0.18 | 每个子问是否被指派成 first/main/extend/final，而不是套 Q1–Q4 模板 |
| `deliverable_clarity` | 0.18 | 每个子问有可测的交付物（数值、排序、规则、阈值、建议） |
| `baseline_to_upgrade_logic` | 0.22 | 是否从第一天的基线走到一个针对性的升级，而不是直接上方法名 |
| `dependency_structure` | 0.14 | 上一问的输出是否真的喂给下一问 |
| `validation_opportunity` | 0.16 | 链上每一环是否留了可执行的检验 |
| `fallback_completeness` | 0.12 | 主升级失败时链是否仍闭合 |

### 1.4 三组混合权重

```
route_core      = 0.70 × 路线分          + 0.30 × 子问题链分
route_final     = 0.85 × route_core      + 0.15 × 队伍匹配分
selection_score = 0.45 × 选题分          + 0.55 × route_final
```

展开：`S = 0.45·T + 0.55·(0.85·(0.70·R + 0.30·C) + 0.15·M)`，`T/R/C/M` 分别为选题、路线、子问题链、队伍匹配（0–5）。

三组的理由：

- **0.45 : 0.55** —— 好题不等于好路线。选题层再漂亮，路线做不出来就是零，所以路线侧拿多数权重（本 skill 沿用原仓库的比例，但把判定线从原仓库的 4.2 上调到 4.4，见 §2）。
- **0.70 : 0.30** —— 路线是主体，子问题链是体检。链层只在题面多问时给 30%，防止"每问都对、连起来没结论"。
- **0.85 : 0.15** —— 模型选择占压倒性多数，队伍匹配只做修正项。理由与本 skill stage 1 的 `2_team_strength_match` 同源：队伍强项不该救一条站不住的路线，但值得在两条几乎等分的路线间做裁决。

## 2. 判定线与 0.02 边界缓冲

| 区间（S 为 selection_score） | band | 动作 |
|---|---|---|
| `S ≥ 4.42` | `primary` | 可定为主选（仍受 §4 的 5 维闸约束） |
| `4.38 ≤ S < 4.42` | `borderline_high` | **压线**：不许直接定为主选，走 §8 tie-break，verdict 记 `pass_with_review` 语义 |
| `3.52 ≤ S < 4.38` | `viable` | 备选；缺哪条证据补哪条，不换题 |
| `3.48 ≤ S < 3.52` | `borderline_low` | **压线**：判进或判出都必须写一条书面理由，否则按 `fallback` 处理 |
| `S < 3.48` | `fallback` | 只在队伍有特殊积累时才选；否则淘汰 |

- 缓冲 ±0.02 与本 skill 唯一的数值容差同源：`score_artifact.py` 对 `mean_score` 的复核容差就是 0.02。同一把尺子，避免这里精确到小数点后三位、那里允许误差。
- 判定线 4.4 / 3.5 是**本地校准值**，与原仓库的 4.2 / 3.6 不同：本 skill 的 verdict 已是七档、且 stage 1 出口要求「全维 ≥7」，把主选线抬到 4.4 是为了让 selection 层不轻易放行；把淘汰线压到 3.5 是为了不误杀数据题与工程题（原仓库 3.6 会把"路线强、题面普通"的题直接判成备选）。
- 两条压线区间互不重叠，且区间端点是闭的：`4.38` 与 `4.42` 都算压线，`3.48` 与 `3.52` 都算压线。

## 3. 必填证据字段

分数只是索引，下面六个字段才是被审的东西。缺字段不算"分低"，算**形式不合规**。

| 字段 | 必须回答 | 不合格样例 |
|---|---|---|
| `evidence` | 这条判据**凭什么**给这个分：数据位置、已算过的量、已跑过的小例 | 「较可行」「比较匹配」 |
| `flip_condition` | 什么**可测**条件会让这条判据翻转：时间点、残差阈值、运行时间、秩相关下界 | 「如果结果不好就换」 |
| `rejected_alternatives` | 被否掉的更简单或更时髦的做法，以及否掉它的那次比较 | 只列一个"没用 LSTM" |
| `refutation_tests` | 能推翻本路线的那一个测试，写清判据与预期值 | 「做灵敏度分析」（这是动作，不是测试） |
| `crowd_escape_mechanism` | 大众题上，凭什么和别人的答案不像 | 空着，或写"我们的模型更先进" |
| `model_choice_rationale` | 为什么是这个模型族，而不是同族的另一个 | 「因为常用」 |

**强制规则**：权重 ≥0.14 的判据，或任何 ≥4 分的判据，必须同时带 `evidence` 与 `flip_condition`；每条候选路线必须带 `rejected_alternatives`、`refutation_tests`、`model_choice_rationale`；当选题层 `differentiation ≤ 3` 时 `crowd_escape_mechanism` 强制，空着即把 `route_differentiation` 压到 ≤3。

## 4. 与 verdict 七档的映射（不自造档位）

| 情况 | verdict | 说明 |
|---|---|---|
| 任一必填字段缺失 / 为空 | `block` | 记为 high-severity issue，分数不可解释即停 |
| `S ≥ 4.4` 但 stage 1 五维 `raw_min < 7` 或 `weighted_mean < 8` | `refine` | 选题好、记录差，补 decision_log，不换题 |
| `S ≥ 4.4` 且五维达标 | `pass` | 与既有出口条件一致（全维 ≥7） |
| `3.5 ≤ S < 4.4` | `refine` | 补证据或降级路线 |
| 全部候选 `S < 3.5` | `refine`；`iter == 3` 时 `carryover` | 交 L2，不在门里磨 |
| 压线区间 | `pass_with_review` 语义 | 进，但 review 项必须原样抄进返工段 |

七档中 `pass_early` 在选题层不启用（选题没有"提前收工"的意义），`refine_partial` 只在 stage 5 的双轨聚合里有定义，这里不借用。

## 5. 落盘形状（decision_log.stages["1"]）

既有字段 `candidates_assessed / selected / rationale / rejected_alternatives / risks_identified` 一个字不动，新增一个 `selection` 子对象：

```json
"selection": {
  "scale": "0-5",
  "candidates": [
    {
      "id": "A",
      "topic": {"feasibility": 4.0, "data_or_parameter_access": 3.5, "differentiation": 4.0,
                "validation_strength": 4.5, "method_fit": 4.0, "narrative_power": 3.5, "risk_control": 4.0},
      "route": {"route_problem_fit": 4.5, "engineering_solvability": 4.0, "data_parameter_control": 3.5,
                "validation_design": 4.5, "route_differentiation": 4.0, "paper_explainability": 4.0,
                "implementation_cost_control": 4.0, "fallback_robustness": 3.5},
      "chain": {"role_alignment": 4.0, "deliverable_clarity": 4.5, "baseline_to_upgrade_logic": 4.0,
                "dependency_structure": 3.5, "validation_opportunity": 4.0, "fallback_completeness": 3.5},
      "team_fit": 4.0,
      "blend": {"topic_route": 4.00, "route_core": 4.02, "route_final": 4.01},
      "selection_score": 3.99,
      "band": "viable",
      "fields": {
        "evidence": ["附件 2 给出 3 年逐日数据", "small-case MILP 12 分钟解出"],
        "flip_condition": "若全量 MILP 超 10 分钟 → 换贪心+局部搜索",
        "rejected_alternatives": ["线性规划松弛：无法表达地块轮作整数约束"],
        "refutation_tests": ["小例精确解与启发式解相对间隙 ≤5%"],
        "crowd_escape_mechanism": "把轮作年限作为状态变量而非约束惩罚项",
        "model_choice_rationale": "决策含整数地块-作物配对，天然属 MILP；同族的网络流无法表达轮作"
      }
    }
  ],
  "selected": "A",
  "borderline_hits": [],
  "near_tie": false
}
```

## 6. 局限：分数是自报的，脚本只查字段填没填

必须写明、不许含糊：

- `selection_score` 与三层子分**全部由 agent 自己填**。`scripts/score_artifact.py` 不读 `stages["1"].selection`，不校验 0–5 分是否与 `evidence` 对得上，也不校验 `flip_condition` 是否可测。
- 脚本能做的只有一件事：`validate_critique` 检查 stage 1 critique 的 5 维 key 是否在白名单、`score` 是否在 `[1,10]`、`evidence` 是否非空、`min_score`/`mean_score` 是否与分数重算一致、`issues` 是否 ≤5 条。**它拦不住编造的证据，只拦得住空字段。**
- 因此 §3 的六个字段是**人工审查的抓手**，不是机器保证。谁填的表，谁对「证据是不是真的」负责；闸门只保证「你没偷懒」，不保证「你没撒谎」。

## 7. 与论文 `weighted_mean` 相互独立

三条硬声明：

1. **不换算。** `selection_score` 是 0–5 的"下注价值"，`weighted_mean` 是 1–10 的"产物合格度"，两者没有线性或分位对应关系，禁止写成「4.4 ≈ 8.8 分」这类折算。
2. **不合并。** `selection_score` 不进 `scores["1"]` 的 5 维数组，不参与 `Σ(s_i·w_i)/Σ(w_i)`，也不受 `config/dim_weights.json` 的 clamp 影响（clamp 是 `[0.7, 1.5]`，只作用于 5 维权重）。
3. **不改 verdict。** 论文与各阶段产物的 verdict 只由 `compute_verdict` / `compute_stage5_verdict` 按 `raw_min` 与 `weighted_mean` 判定。`selection_score` 高不能让一个 `refine` 变 `pass`，低也不能把已 `pass` 的阶段打回。

冲突时的优先序：**verdict 优先**（它是门禁语义），`selection_score` 只影响「要不要换题 / 换路线」的建议，且换题动作必须重新走 stage 1 全流程，不许只改一个数字。

## 8. 校准纪律（不守就会翻车）

1. 两个候选的 `selection_score` 差 ≤0.20 时，不许用「显著领先」；差 ≤0.02 记为 `near_tie`，按下面顺序裁决。
2. 压线与 near_tie 的 tie-break 顺序：① 第一问能否在第一天出可信基线 → ② 主问是否有问题特异的升级（而非通用方法） → ③ 验证是否强于"看起来合理" → ④ 结果能否变成图/表/决策 → ⑤ 队伍编码与领域强项。
3. 只有方法名、没有基线比较的路线，`route_problem_fit` 与 `route_differentiation` 都不得给到 4 分以上。
4. 大众题 `differentiation` 低不等于该弃题：先把一条非通用路线试着写出来再扣分，且必须给 `crowd_escape_mechanism`。
5. 任何一条 ≥4 分的判据若没有 `flip_condition`，视为未完成评审，按 §4 记 `block`。
## 9. 适用边界与接线

- **只在 stage 1 用**。stage 2 之后不再重打 selection 分；若中途换题或换主路线，必须回 stage 1 重开一份 `selection.candidates`，不能在原表上改数字。
- **题面只有一问时**，子问题链层不启用，`route_final = 0.85 × 路线分 + 0.15 × 队伍匹配分`，`selection_score = 0.45 × 选题分 + 0.55 × route_final`，其余不变。
- **与其它文件的接线**：`references/rubrics.md` Stage 1 的 5 维判"记录写得好不好"，本文件判"这个选择值不值"；`references/award_patterns_notes.md` 提供填表用的套路清单；`references/decision_log.template.json` 的 `stages["1"]` 是唯一落盘处。
- **不适用**：已经开赛且题号不可更改时，不要用本表否决既定选题，只用它做路线层面的降级决策（换主路线、加退路）。

