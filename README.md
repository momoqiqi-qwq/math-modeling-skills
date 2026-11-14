# 数学建模 Skill：两个可独立使用的包 + 一份实跑补丁

三样东西，**互不依赖**。前两个可以单独装、单独用；第三个是加法，装在上游本体上。

| | 是什么 | 装不装看什么 | 许可 |
|---|---|---|---|
| [`mathmodel-scoring-gate`](mathmodel-scoring-gate/) | 可复算评分门禁：5 维 critic → 加权分 → 七档 verdict → `state/decision_log.json` | 已有产物，要判「能不能过、两次判定可不可比」 | MIT（上游 handsomeZR-netizen） |
| [`mathmodel-competition-suite`](mathmodel-competition-suite/) | CUMCM / MCM-ICM / 电工杯 三套规则写法包：评分 overlay、题型表、获奖写法、反模式、短语库、摘要与章节骨架、LaTeX 主文件 | 赛前想知道「这个比赛要什么、怎么写才像样」 | MIT（同上） |
| [`math-modeling-addon`](math-modeling-addon/) | 上游 [XiaoMaColtAI/math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill) 的增量补丁：门禁执行规范、M1 轮次成本、工具隐性约束、质检清单追加两条、DSH 状态机插件 | 已经在用那个上游 skill，想把踩过的坑一次性补进去 | MIT（仅本目录自有内容） |

一句话分工：**裁判尺负责判能不能过，规则包负责说标准长什么样，补丁负责让生产线别重复踩坑。**

## 装法

skill 的硬规则：**目录名 = `SKILL.md` 的 `name` = 加载名**。前两个包已对齐，复制到 skills 目录即可。

```bash
git clone https://github.com/momoqiqi-qwq/math-modeling-skills.git

# 只想要裁判尺
cp -r math-modeling-skills/mathmodel-scoring-gate ~/.claude/skills/

# 只想要竞赛规则与写法
cp -r math-modeling-skills/mathmodel-competition-suite ~/.claude/skills/
```

Codex CLI 用 `$CODEX_HOME/skills/`，其它 harness 只要有「按 `SKILL.md` 的 `description` 触发、按需读同目录 references」的机制就能用。纯文件，无编译、无服务、无网络依赖。

`math-modeling-addon` 要**先装上游本体**，再覆盖文件——它不含上游任何内容，原因见下。

## math-modeling 本体在哪

上游 [XiaoMaColtAI/math-modeling-skill](https://github.com/XiaoMaColtAI/math-modeling-skill)（1.9k star）**没有许可证**（GitHub API 返回 `license: null`，即保留所有权利）。本仓库因此不整份再分发它，`math-modeling-addon/` 只装自己写的部分。

本体另外维护了一份只读快照：[momoqiqi-qwq/math-modeling-skill-mirror](https://github.com/momoqiqi-qwq/math-modeling-skill-mirror)（快照 `7117121` / 2026-11-13，除 `MIRROR.md` 外与原快照逐字节一致，**版权仍归原作者，不构成授权**）。拿不到上游或上游变动时用它复现，装法见 [那个目录的 README](math-modeling-addon/README.md)。

这件事本身也值得记住：**「公开可访问」不等于「可以再分发」**。没有 LICENSE 的仓库，fork 可以，另起仓库复制不行。

## truth in advertising：这些数字是实测的

2026-11 用两道题把整条流程从头跑到尾（2024 CUMCM C 题附件全缺；另一道两变量 LP 的工厂排产），结论照实写：

| 环节 | 实测 |
|---|---|
| 建模终检（C 题） | **6 轮**才过，P0 缺陷 4 → 1 → 0 → 0 → 0 → 0 |
| 建模终检（工厂排产，两变量 LP） | **1 轮**过，2.6 分钟，5 份文件 242 行 |
| 编程最小可运行结果 | 一轮通过 |
| 论文证据大纲 | **第 1 轮 FAIL**（2 P0 / 2 P1 / 7 P2） |
| 论文终检 | **第 1 轮 FAIL**（0 P0 / 6 P1 / 10 P2） |
| 论文复验 | PASS（0 P0 / 0 P1 / 5 P2 可选），成稿 30 页 |

沉淀下来的几条，写进 references 里，不是宣传语：

- **宣称完备处就是漏洞处**——三次「已排除伪解 / 已覆盖全部情形 / 模式互斥」的断言，三次都只堵了开关变量的一个端点。
- **过松算错，过紧算少**——约束比题面更紧只丢解、不报错，比写错更难查。
- **P1 与 P2 的分界是「能不能骗过验证」**，不是「看起来多严重」。
- **加随机性也是一种编造**——题面只给点趋势、不给离散幅度时，补一个分布等于发明参数。
- **产物不会冻结**——耗时、随机种子、机器相关量写进正文，下一轮重跑就变成「文本与产物不符」。

## 边界（不承诺的事）

- 不承诺任何数值结论。模型对不对、参数取值合不合理，仍然要人判断。
- **不替代当届官方规则**。规则每年变，`competition-suite` 里的 `current_rules.md` 是基线，必须与官方文件核对后使用。
- 分位数据（`empirical.json`）只在样本足够的竞赛上有意义；样本为 0 的明确标 `n=0`，**不得据此推断数值门槛**。
- 门禁 PASS 只证明「结构完备、参数化写法正确、符号层不自相矛盾、验证项可执行、文献可解析」，不证明论文能获奖。

## 来源与许可

- 本仓库自有内容（`math-modeling-addon/` 全部、两个包里的 `SKILL.md` 与新增 references）：MIT，见 [LICENSE](LICENSE)。
- `mathmodel-scoring-gate` 的判定内核与配置、`mathmodel-competition-suite` 的竞赛包与 LaTeX 模板，取自 [handsomeZR-netizen/mathmodel-skill](https://github.com/handsomeZR-netizen/mathmodel-skill)（MIT）。版权声明保留在各目录的 `LICENSE-mathmodel-skill.txt` 与 `THIRD_PARTY_NOTICES.md`。
- `mathmodel-scoring-gate/references/stage1_selection.md` 的判据结构借鉴 [y3519712124-ui/math-modeling-contest-route-selection](https://github.com/y3519712124-ui/math-modeling-contest-route-selection)（MIT）。
- `math-modeling-addon/references/workbench映射.md` 记录与 [Lucasuiii/modeling-workbench](https://github.com/Lucasuiii/modeling-workbench)（MIT）的阶段对齐，**不含其代码**。
- 竞赛规则、赛题、获奖论文、商标等外部材料不因本仓库的 MIT 许可而重新授权。
