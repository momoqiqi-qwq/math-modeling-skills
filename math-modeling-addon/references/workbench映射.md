# workbench 映射（我方 5 门禁 ↔ Lucasuiii/modeling-workbench 0.6.0）

本文件解决一件事：两套状态机不能同时当权威。**结论：我方门禁（M1/P1/P2/W1/W2）是唯一判定权威；workbench 只作为「证据/运行时留痕层」旁挂。**

- 来源仓库：https://github.com/Lucasuiii/modeling-workbench （MIT，pushed 2026-09-23，无 release）
- 安装名：`math-modeling-workbench`（放在 skill 库的 `skills/math-modeling-workbench/`）
- 运行环境：独立 venv，需 `jsonschema` + `pypdf`（缺 jsonschema 会 `ModuleNotFoundError`；勿往基础环境塞）
- 我方状态文件：`<PROJECT_ROOT>/.math-modeling/state.json`（version 6）

## 1. 阶段对齐

| workbench stage | 我方对应 | 谁判 |
|---|---|---|
| `intake` | `mm_project_init` + 题目与附件清单（建模手 工作流程 一） | **技术完成**，workbench 可自行 passed（实测：不传 `--confirm-human` 也能过） |
| `problem-analysis` | 建模手「先理解再选模型」→ `题目分析报告.md` 的 1–4 节 | 我方 M1 管，workbench 只查 `analysis/*.json` 是否齐 |
| `model-design` | 建模手 模型合同（`前置合同.md` 八项）+ `术语表格.md` | **双闸**：我方 M1 PASS + workbench 人工停顿（需 `--confirm-human`） |
| `computation` | 编程手 P1 → 全量计算 | 我方 P1；workbench 要求 `record_run.py` 留痕 |
| `validation` | 编程手 P2（复现/哈希/种子/量纲） | 双闸：我方 P2 + workbench 人工停顿 |
| `paper` | 论文手 W1 → 正文 → W2 | 我方 W1/W2；workbench 要求 `paper-plan` / `claim-ledger` / 可见文本检查 |
| `delivery` | 论文手 W2 终检 + 交付协议 | 双闸：我方 W2 + workbench 人工停顿 |

## 2. 状态字段映射（`.math-modeling/state.json` ↔ `.cumcm/state.json`）

| 我方字段 | workbench 字段 | 说明 |
|---|---|---|
| `version: 6` | `schema_version: "0.6.0"` / `workflow_version` | 各自版本号，**不得互写** |
| `project.projectRoot` | 项目目录本身 | workbench 用 `--project` 传，不落字段 |
| `currentPhase: modeling\|programming\|paper` | `current_stage`: 7 档 | 我方 3 相 × 门禁，workbench 7 段线性；**粒度不同，按门禁映射而非按名字** |
| `phases.modeling.gateM1` | `stages.model-design` + `.cumcm/decisions/DEC-00x` | 我方存回执摘要；workbench 存 decision + snapshot |
| `phases.programming.gateP1` | `stages.computation` + `runs/` manifest | workbench 的 run manifest 比我们细（哈希/命令/退出码） |
| `phases.programming.gateP2` | `stages.validation` | 对应 |
| `phases.paper.gateW1/gateW2` | `stages.paper` / `stages.delivery` | W1≈paper 前段，W2≈delivery 前 |
| `phases.*.skillMdRead` | 无 | 我方要求「读了角色 SKILL.md 才算进场」，workbench 无此字段 |
| `phases.*.tasks[]` | 无 | 我方任务清单 |
| `ledger[]`（最多 500 条） | `.cumcm/decisions/` + `.cumcm/runs/` | workbench 事件是**文件**，可 diff、可外审；我方是内嵌数组 |
| `deliverables` / `completed` | `stages.delivery` + `.cumcm/delivery-manifest.json` | 对应 |
| 无 | `mode: working\|finalizing` | **我方缺这个概念**：workbench 明确「探索期允许不全，冻结期才全查」 |
| 无 | `implementation: {preferred, fallback, selection}` | 我方靠 编程手 MATLAB规范 暗示，未落状态 |
| 无 | `.cumcm/validation-report.json` | 每次 preflight 覆盖写，可当快照比对 |

## 3. 产物映射

| 我方产物 | workbench 契约 | 差异 |
|---|---|---|
| `题目分析报告.md`（9 节） | `analysis/PROBLEM_FACTS.json` + `analysis/TASK_CAPABILITIES.json` | 我方**散文 + 表格**，靠 M1 人/agent 判；workbench **JSON schema 强校验**，字段缺失直接 error |
| `术语表格.md` | **无对应** | workbench 没有符号表契约；论文符号表由我方产出，这是我们的净优势 |
| 模型合同（前置合同 八项，写进报告骨架） | `model/MODEL_CONTRACT.json` | 我方八项散落在正文；workbench 是机器可读合同（变量/约束/验证/回退分字段） |
| 输入文件哈希（工作流程 一「记录哈希或版本」） | `problem/SOURCE_MANIFEST.json`（sha256/size/media_type/origin/acquisition） | workbench 一初始化就落 `sha256`，我方常靠口头「已记录」 |
| 文献 DOI 可追溯（质检清单） | 无强制 | 我方更严 |
| `完整论文.docx`（默认交付） | **DOCX 未实现**（只走 LaTeX→PDF） | 我方覆盖 Word 流水线，workbench 覆盖 PDF 编译与源码包 |
| 候选图 / 正式图 ≥8 | `figure-manifest.schema.json`，配 `plot-style/cumcm.mplstyle` | workbench 有图清单契约与统一 mplstyle |
| 复现清单 | `run-manifest.schema.json` + `index_result.py` | workbench 强，脚本强制「不许手写 hash」 |

## 4. 闸门映射

| 我方 | workbench | 实测证据 |
|---|---|---|
| M1（未参与编写的 Subagent 回执 PASS） | `model-design` 人工停顿 + `build_independent_review_package.py` 生成审阅包 | workbench 不给 `MODEL_CONTRACT.json` 就直接拒：原文 `error: show the model-design material and wait for the user; missing model/MODEL_CONTRACT.json` |
| M1 回执 6 段（范围/输入快照/状态/证据/发现/返工） | `independent-review-result.schema.json` | 两者同构；workbench 多了 schema 校验 |
| 「被审产物变了 PASS 失效」 | 「reviewed claim/model 变了要重新出示并取新决定」 | 同一条纪律，各自表述 |
| 无需用户原话 | **必须 `--task-turn-ref` 引用户回复；三个停顿点还要 `--confirm-human`** | 实测：`intake` 传 `--confirm-human` 被拒 `--confirm-human applies only to acceptance at the three human checkpoints`；即 intake/analysis 属技术阶段，model-design/validation/delivery 才是人工闸 |
| 我方 gate 无「模式」概念 | `working` 允许不全，`finalizing` 全查 | 建议移植：探索期别让我们自己的门禁把人卡死 |

## 5. 单向数据流（硬规则）

1. **写**：我们的建模手/编程手/论文手写产物到 `PROJECT_ROOT`；workbench 只写 `.cumcm/` 与其 `problem/`、`analysis/`、`model/`、`runs/`。
2. **判**：以我方门禁为准。workbench 的 `gate status: blocked\|working_ready` 只作为「结构性缺件」的提示，不替代 M1/P1/P2/W1/W2。
3. **禁**：不让两边各自拥有「当前阶段」。要跑 workbench，先 `mm_state` 看阶段，再用 `record_decision.py` 把同一阶段推进到对应 stage；**反向不做**（workbench 推进不会改我方 state.json）。
4. **锁**：同一 `PROJECT_ROOT` 下，`state.json` 与 `.cumcm/state.json` 不得由两个进程同时写；批量脚本先停 workbench 侧。

## 6. 已知缺口（要补就补在我方）

- `mode: working/finalizing` → 建议加进 `mm_state`，探索期只提示不阻断。
- 输入哈希 → 建议 `mm_project_init` 时对 `题目/`、`附件/` 落 `manifest.json`（sha256+size+mtime）。
- 运行留痕 → P1/P2 增加「命令 + 退出码 + 输入哈希」三件套登记。
