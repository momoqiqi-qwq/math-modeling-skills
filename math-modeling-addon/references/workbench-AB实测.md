# A/B 实测：同一道题，stage 1–3 两侧怎么判

题：2024 高教社杯 C 题「农作物的种植策略」（`tmp/problem-backup.md`，3630 B，**附件 1–3 不在本机**）
A 侧：`math-modeling-workbench` @ `tmp/ab-test/w-project`
B 侧：`math-modeling`（建模手）@ `tmp/ab-test/m-side`

## 判了什么

| 阶段 | A（workbench）实际判据 | 结果 | B（我方）实际判据 | 结果 |
|---|---|---|---|---|
| 输入/intake | `problem/SOURCE_MANIFEST.json` 存在 + sha256/size/media_type/origin 齐 | **自动 passed**，DEC-001 落盘，不等人工 | 无闸门（M1 才是第一道） | 无判定 |
| 审题/problem-analysis | `analysis/PROBLEM_FACTS.json` + `analysis/TASK_CAPABILITIES.json` 逐字段校验 | 未填 → `blocked (preflight)`，2 个 structural error | 报告是否讲清 9 节、假设是否分级 | 报告 4586 字 / 86 行表格 / 34 公式块 / 10 条假设（3 关键 + 7 可放宽）；无一条机器可判 |
| 建模/model-design | `model/MODEL_CONTRACT.json` + 每组件 ≥2 候选 + 收口到 1 + `--confirm-human` | 合同齐后 `awaiting_review`；仍有 gate-only ERROR `MODEL-E016`；`record_decision.py` 硬拒代签 | 前置合同八项写进正文、每子问题 ≤2 个独立模型体系 | §0 八项总表；Q1 只 1 族并写明理由，Q2/Q3 各 2 族；靠 M1 独立 Subagent 判 |

## A 侧被 schema 逼出来的量

- `PROBLEM_FACTS`：24 条 fact（每条 `source_id` + `location`）、3 子问题、7 definitions、6 ambiguities、8 assumptions
- `TASK_CAPABILITIES`：4 条能力 × 17 条 `acceptance_check`（每条 `check_id`/`assertion`/`judge`；`judge=recorded` 必须带 `assertion_name`）
- `MODEL_CONTRACT`：3 组件 × 3 候选 = 9 候选，每个候选要 `discriminating_evidence`
- 合计约 **380 个字段值 / 570 行 JSON**，两轮才压到 0 blocking

## 三条真正的判定差异

1. **同一个词，两种判法**：A 说「必须收口到一个被选中的候选」（`MODEL-E013 … must end with exactly one selected candidate; found 0`），B 说「不许为凑数编第二族」。合起来才是完整纪律——**先摆够候选，再收口，收口要留谁被展示过**（`selection_check.presented_candidate_ids`）。B 那句「Q1 只有一个模型族，因为其余都是等价改写」在 A 里没有位置可写。
2. **人工签字不可互替**：A 要 `--confirm-human` + 用户回合引用，拒签原文 `model-design awaits the user's explicit decision; model self-review cannot approve it`（防 agent 自己盖章）；B 要未参与编写的 Subagent 回执 PASS（防作者自审）。**两道闸防的是两件事，都要。**
3. **缺附件时谁更狠**：两边都零编造。B 写 `§3.4 D1–D8 待确认`（散文表）；A 把「缺什么、谁补、补了改哪一行」变成 fact/capability 的必填字段（JSON，可查询）。A 更贵，但缺项会自己浮出来；B 更省，代价是缺项只在人会去读的地方。

## B 侧 A 侧都没有的东西

- 术语表：20 行符号，一符一义、`$...$` 渲染、0 个可见下划线（机械核查：`\underline` 0 次）。A 的 schemas 里**没有符号表契约**。
- 算法百科 / 绘图模板 / DOCX 流水线：A 全无。

## 成本

同等深度：A ≈ 570 行 JSON + 两轮返工；B ≈ 241 行报告 + 37 行术语表。A 的录入成本约 1.5–2×，换来「三个月后能复算、能外审」。

## 结论

**不是谁更严，是判不同东西**：A 判「该写的字段在不在」（结构），B 判「写出来的东西站不站得住」（内容质量）。

所以接法只能是旁挂：A 的 `gate status` 当缺件提示，B 的 M1/P1/P2/W1/W2 当放行权威。要 A 的三样东西——`mode working|finalizing`、输入 SHA-256 manifest、run 留痕——就照 `references/workbench映射.md` §6 补进我方。
