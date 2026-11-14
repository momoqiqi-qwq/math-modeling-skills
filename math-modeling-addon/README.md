# math-modeling-addon

上游 [XiaoMaColtAI/math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill)（1.9k star）的**增量补丁包**：一次端到端实跑（两道题，从选题跑到论文终检）之后补进去的东西。

**这里不含上游任何文件。** 上游仓库没有许可证（`license: null`，即保留所有权利），所以不能整份再分发；本目录只放自己写的部分，装法是「先装上游，再把这里的文件放进去」。

## 装法

```bash
# 1. 先装上游本体
git clone https://github.com/XiaoMaColtAI/math-modeling-skill.git ~/.claude/skills/math-modeling

# 2. 再覆盖/新增本目录的文件
cd math-modeling-addon
cp -r references/. ~/.claude/skills/math-modeling/references/
cp -r dsh-plugin/. ~/.claude/skills/math-modeling/dsh-plugin/   # 可选，只有用 DSH 才需要
```

然后按 [references/质检清单-追加两条.md](references/质检清单-追加两条.md) 把两条手工追加进
`references/roles/建模手/references/质检清单.md`（**不用脚本覆盖，避免把你自己的改动冲掉**）。

## 文件清单

| 文件 | 作用 | 与上游的关系 |
|---|---|---|
| `references/门禁执行与评分通道.md` | 五个门禁分别由谁判、回执六段、什么情况下才值得接评分通道；含「段号口径」三条硬要求 | 新增 |
| `references/M1轮次与成本.md` | 实测的轮次成本模型 + 两条轮次闸门 + PASS 边界怎么写 | 新增 |
| `references/四方路由.md` | 可选组合说明：只在另外装了评分门禁 / 竞赛包 / 绘图模板库时才读 | 新增（内容已改为「可选」，不是必需品） |
| `references/workbench映射.md` | 与 Lucasuiii/modeling-workbench 的阶段对齐表；结论「它录，我们判」 | 新增，不含其代码 |
| `references/workbench-AB实测.md` | 同一道题两边各跑 stage 1–3 的实测差异 | 新增 |
| `references/roles/论文手/references/工具隐性约束.md` | `tools/docx` 的 14 条隐性判定（函数名 + 正则原文 + 报错串），违反即阻断保存 | 新增 |
| `references/质检清单-追加两条.md` | 建模手质检清单的第 12、13 条（端点补集、约束不得比题面更紧） | 追加 |
| `dsh-plugin/` | DSH 状态机插件：`mm_project_init` / `mm_phase_enter` / `mm_todo` / `mm_gate` / `mm_check_deliverables` / `mm_complete` / `mm_state`，以及 `mm_mode`（working/finalizing）、`mm_inputs`（输入清单 SHA-256 漂移）、`mm_run`（运行留痕） | 新增（上游无插件） |

`dsh-plugin/` 里**没有**插件自带的 `skills/math-modeling/` 副本——那部分是上游内容，装的时候用你的上游本体。

## 这些补丁解决了什么

按实测顺序：

1. **门禁是流程，评分是通道，别混写**。原先把评分门禁写进路由，实际六道门禁全由独立 subagent 判，`score_artifact.py` 一次没被调用。分开之后，装不装评分门禁都不影响流程跑完。
2. **M1 要跑几轮可以预估**。轮数 ∝「质检者自己算不出、必须外部证据才能判真假的断言数」×「附件缺失度」，与字数页数无关。实测：两变量 LP 1 轮 / 2.6 分钟；附件全缺的 CUMCM 题 6 轮。
3. **两条轮次闸门**：首轮 P1=0 且 BLOCKED=0 ⇒ 这一轮就该 PASS，再跑没有新判定依据；只要还有 BLOCKED，轮数下限由附件何时到位决定。
4. **论文手的坑要写成可核对的条目**。`paper_format.py` 有十几处未写进规范的硬判定（段落以「图N」开头即被当题注、内部术语是硬过滤而非提示、LaTeX 命令白名单、章名必须恰为「参考文献」等），踩一次浪费一轮。
5. **产物不冻结**：耗时、随机种子这类量写进正文，下一轮重跑就变成「文本与产物不符」。正文只写量级并指向产物文件。

## 许可

本目录内容为 MIT（见仓库根 [LICENSE](../LICENSE)）。上游本体不在本仓库内，其许可由上游决定。
