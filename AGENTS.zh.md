<!-- translation: zh · canonical: AGENTS.md · synced: 2026-11-14 -->

# Agent 指令

你在维护一个三层的知识库。先读这份文件，再读 `wiki/SCHEMA.md`。这两份文件覆盖你学过的任何通用 wiki 惯例。

## 阅读顺序

1. `AGENTS.md`（本文件）——操作规则与 playbook。
2. `wiki/SCHEMA.md`——页面类型、frontmatter、tag、命名、lint 节奏。
3. `outputs/SPEC.md`——渠道规格的契约。
4. `wiki/index.md` 与 `wiki/log.md`——当前状态与历史。
5. `METHOD.md`——只在某条规则的理由不清楚、或你即将破例时才读。

## 不可逾越的边界

| 层 | 你可以 | 你不可 |
|---|---|---|
| `raw/` | 读 | 写、改名、"修正"、提交 |
| `wiki/` | 新建、重写、合并、删除 | 存放渠道规则、PII，或草稿的副本 |
| `outputs/` | 写草稿、更新 state/SPEC | 引入事实，或被引为来源 |

四条铁律，按优先级排列：

1. 一个事实只有一个出处。总数只写在一页，其余页面链接过去。
2. 渠道负责渲染事实，从不创作事实。
3. `outputs/` 里的任何东西都不得出现在 `sources:` 字段里，也不得当作证据。
4. 事实错了，先改 `wiki/`，再重新渲染。永远不要通过改草稿来纠正事实。

## Playbook

### 摄入一份原件

1. 确认文件在 `raw/` 里（不在就复制进去；永不编辑它）。
2. 写 `wiki/sources/<slug>.md`：它是什么、哪里有用、哪里不可靠、喂养哪些页面。
3. 更新每一个受影响的实体/概念页。一行一个事实，有时间段时先写时间段。
4. 若它与其他页面矛盾，在**拥有**该事实的页面里解决，并在 `log.md` 记下结论。
5. 把新页加入 `index.md`；向 `log.md` 追加一条 `ingest` 记录。
6. 跑 `python scripts/wiki_lint.py wiki/`。死链和孤儿页要在报告完成前修掉。

### 回答关于 wiki 的问题

1. 先跑 `python scripts/wiki_lint.py wiki/`（很便宜），再检索：读 `wiki/index.md` 顺着一行摘要走；`grep -rn "<term>" wiki/` 通常就够了。若装了 `llm-wiki` 技能，它的 `wiki_search.py` 提供带排序的段落级检索。
2. 读它返回的页面；顺着链接走到拥有相关事实的页面。
3. 只依据 wiki 文本作答。若答案需要 wiki 里没有的事实，直说，并提议需要哪次摄入来补上。不要用常识填空再把它当作 wiki 内容。
4. 若答案可复用（一次比较、一个决定），存成 `synthesis` 页并记入 log。

### 产出一次渠道发布

1. 读 `outputs/<channel>/SPEC.md` 及其事实映射里的 wiki 页。
2. 草稿写进 `outputs/<channel>/drafts/<YYYY-MM>/`，每种语言一个文件。
3. 用脚本（`len()`）量上限，不要目测。超了就改草稿——不要改 wiki，除非事实确实错了。
4. 走一遍规格里的验收清单与禁写项。
5. 更新 `outputs/<channel>/state.md`：版本、日期、实测值、偏差。
6. 向 `wiki/log.md` 追加一条 `output` 记录，链接到 state 条目。

### Lint

```bash
python scripts/wiki_lint.py wiki/          # 死链、孤儿页、frontmatter、跨层泄漏、PII
python scripts/wiki_lint.py wiki/ --strict # 警告也算失败（CI 用）
```

这个脚本就是本仓库的全部工具链——只用标准库。语义检索与图层是可选项，属于 `llm-wiki` 技能（`wiki_search.py`、`wiki_stats.py`、`wiki_graph_*.py`）；想要就装那个技能。

以 file:line 的列表形式报告发现。机械问题（死链、缺 frontmatter）直接修；内容改动先提议，不要悄悄做。

## 文风规则

- 写事实，不写形容词。wiki 页里没有 "passionate"、"innovative"、"results-driven"。
- 时间段在前：`2021-01 → 2024-02 · Hybrid · Madrid — Role name`。
- 绝不复述别页拥有的总数；链接过去。
- 数字带上依据："9+ years (as of 2026-11)"，不是 "9+ years"。
- PII 永不进入 `wiki/`：没有电话、住址、证件号、生日或私人链接。草稿需要时，在渲染时向用户索取。

## 拿不准时

- 一条约束（字符上限、页数、语言等级）→ 属于某个 `outputs/*/SPEC.md`。写在那里。
- 一个事实（日期、年限、技术、客户）→ 属于 `wiki/`。写在那里，并带上它的来源页。
- 两者都有 → 先写事实，再写渲染它的渠道规则。
