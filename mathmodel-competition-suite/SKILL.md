---
name: mathmodel-competition-suite
description: CUMCM 国赛 / MCM-ICM 美赛 / 电工杯 三套竞赛包：当届规则基线、评分细则 overlay、题型表、获奖写法、反模式、短语库、摘要与论文章节骨架、LaTeX 主文件。用于赛前确认该写什么、赛中逐段对照怎么写、交稿前扫反模式。触发词：国赛、美赛、MCM、ICM、电工杯、数学建模竞赛、竞赛规则、摘要模板、论文骨架、反模式、获奖论文怎么写、LaTeX 论文模板。
---

# 三竞赛规则与写作包 · mathmodel-competition-suite

一个 skill，三套竞赛资料。**只解决「这个比赛要什么、怎么写才像样」，不做评分、不出算法。**

- 要判定「够不够格、能不能放行」→ `mathmodel-scoring-gate`
- 要真刀真枪产出论文/图/代码 → 本地 `math-modeling`（建模手/编程手/论文手三角色 + Word/LaTeX 双产物）

## 一分钟 dispatch

| 你手上是什么 | 先读哪一个 |
|---|---|
| 还没选题，想知道这比赛考什么、什么写法吃香 | `competitions/<c>/README.md` → `winning_patterns.md` |
| 要核对页数/字号/匿名/AI 声明/文件大小 | `competitions/<c>/current_rules.md`（**然后必须去官网复核，见硬纪律 1**） |
| 要写摘要 | `competitions/<c>/abstract_template.md` |
| 要搭整篇骨架 / 章节目录 | `competitions/<c>/paper_skeleton.md` |
| 要把段落写「像获奖论文」 | `phrase_bank.md`（中文还可读 `distilled_phrases.md`） |
| 交稿前自检 | `anti_patterns.md` 逐条扫 |
| 要给论文打分 / 定分权重 | `rubric_overlay.json` + `topic_specs.json`（或直接用 scoring-gate） |
| 想拿「别人一般写多少字/几张图」当参考 | `empirical.json` + `empirical_notes.md`（**先看硬纪律 2**） |
| 要 LaTeX 起稿 | `templates/latex/<c>/main.tex` |

`<c>` ∈ `cumcm` | `mcm` | `diangong`

## 三条硬纪律（违反就是事故）

1. **`current_rules.md` 只是基线快照，不是当届规则。** 任何写进交付物的硬数字（页数上限、字号、摘要字数、AI 使用声明格式、文件命名、提交入口）在赛前必须去当届官方通知/官网页逐条核对，并把核对结果写进 `state/decision_log.json` 的 `compliance.ruleset`（`verified_at` + `official_urls`）。规则冲突时以官方为准，本 skill 让位。
2. **`empirical.json` 的样本量决定它能说什么。** CUMCM 有 59 份可提取样本（来源 91 份），只能当「异常提示」；**MCM 与电工杯 n=0**，里面没有可用分位，任何「一般写 X 字/图 Y 张才够」的说法在这两个比赛上都是编的。永远不许把分位翻译成获奖门槛。
3. **不许编条文、不许编引用。** 规则、赛程、评审口径没查到的，写「未核实」；参考文献没读过的，不进列表。宁可空着让用户补，也不要造一个看似合理的 URL 或标准号。

## 文件清单（每套竞赛同构）

| 文件 | 内容 | 什么时候读 |
|---|---|---|
| `README.md` | 该竞赛的赛制、时间线、赛道/题号习惯 | 开工第一份 |
| `current_rules.md` | 规则基线快照（页数/格式/匿名/AI/提交） | 赛前 + 交稿前，且必须复核 |
| `winning_patterns.md` | 获奖论文的共同结构特征 | 选题后、定骨架前 |
| `anti_patterns.md` | 高频扣分点（含 anti_pattern_id，如 A3） | 每次自检、交稿前必扫 |
| `phrase_bank.md` | 学术表达句式库（中/英按竞赛分） | 写正文卡壳时 |
| `abstract_template.md` | 摘要骨架（信息链顺序，不是填空模板） | 写摘要、改摘要 |
| `paper_skeleton.md` | 章节骨架与每节该交代什么 | 搭初稿 |
| `rubric_overlay.json` | 该竞赛的评分维度覆盖与描述 | 自评 / 交给 scoring-gate |
| `topic_specs.json` | 题型代码表（A/B/C… 各考什么、适合什么模型族） | 选型阶段 |
| `empirical.json` | 观察分位（**看清 n**） | 只想判断「是不是明显偏少」时 |
| `empirical_notes.md` | 分位怎么来的、能怎么用、不能怎么用 | 用 empirical 之前必读 |

CUMCM 另有四份蒸馏本（只有国赛有，因为样本足够）：

| 文件 | 内容 |
|---|---|
| `distilled_structures.md` | 获奖论文的章节结构统计与骨架变体 |
| `distilled_phrases.md` | 中文摘要/正文高频学术句式（27KB，最长的一份） |
| `distilled_naming.md` | 模型命名与符号命名习惯 |
| `distilled_formats.md` | 公式、图表、编号、参考文献的排版惯例 |

## 懒加载纪律

一次只读 1–2 个文件，读完就用，别把整套 `competitions/` 灌进上下文（合计 ~180KB）。

- 写摘要：只读 `abstract_template.md` + `anti_patterns.md` 摘要相关段
- 搭骨架：只读 `paper_skeleton.md` + `winning_patterns.md`
- 交稿自检：只读 `anti_patterns.md` + `current_rules.md`
- 需要句式：`grep` 关键词定位到 `phrase_bank.md` 的具体段落，别整篇读

## LaTeX 起稿

```bash
cp templates/latex/cumcm/main.tex .        # mcm / diangong 同理
```

三份 `main.tex` 只提供版式与章节骨架（含中文支持、图表/公式/参考文献环境）。**里面的题目、队号、控制号、关键词全是占位**——交稿前必须替换成真值，占位符残留是硬伤（`XXXX`、`TITLE OF YOUR PAPER`、`keyword1`）。
本地 `math-modeling` 若要用它的 `latex_paper.py`，先 `init` 再 `doctor`，别把两套模板混用。

## 和另外两个 skill 的接力

```
选题 ──(topic_specs / winning_patterns)──> 建模 ──(本地 math-modeling: 建模手/编程手)
   │
   ├─ 每阶段产物 ──(mathmodel-scoring-gate: 5 维 critique → verdict)──> 放行 / 返工
   │
   └─ 成稿 ──(paper_skeleton / phrase_bank / abstract_template)──> 论文
                                    └─(anti_patterns + current_rules)──> 交稿自检
```

竞赛包给「标准」，scoring-gate 给「裁判尺」，math-modeling 给「生产线」。三者不要互相替代。

本包自包含（规则 / 写法 / 分位数据 / LaTeX 模板），**不依赖任何其它 skill**，也不需要联网。与上两者同时使用时的接线由使用方决定，本包不引用它们的文件；跨 skill 引用一律写全 `<skill>/references/...` 相对路径，不写本机绝对路径。

## 来源与许可

全部内容取自 [handsomeZR-netizen/mathmodel-skill](https://github.com/handsomeZR-netizen/mathmodel-skill)（MIT，见 `LICENSE-mathmodel-skill.txt` 与 `THIRD_PARTY_NOTICES.md`）：`competitions/{cumcm,mcm,diangong}/` 全量、`templates/latex/` 三份主文件。**原文未改动**（便于与上游 diff），本 SKILL.md 为新增。
