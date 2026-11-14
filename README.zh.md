<!-- translation: zh · canonical: README.md · synced: 2026-11-14 -->

# LLM Wiki + Outputs（中文）

一份把**同一批事实**同时输送到多个去处（简历、LinkedIn、作品集、面试口径）的知识库模板。

它沿用 "LLM Wiki" 模式（不可变原件 → LLM 维护的 markdown wiki → lint/查询循环），只加了一层结构：把**每个渠道的写作规则**放到独立的 `outputs/` 层，让那些规则永远不渗进事实。

- [English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [方法论](METHOD.zh.md) · [Method (EN)](METHOD.md) · [Método (ES)](METHOD.es.md)

## 它修的是什么病

把简历文案和事实塞进同一个 wiki，会朝两个方向烂掉：

1. **渠道规则渗进事实。**「Headline ≤ 220 字符」被抄进六个实体页；平台一改上限，你要改九个文件。
2. **产出物被当成来源。**LinkedIn 草稿成了它自己引用的日期的「来源」。事实失去出处，wiki 开始引用自己。

解法不是更强的自律，而是一条边界：事实住 `wiki/`，渠道规则住 `outputs/<渠道>/SPEC.md`，数据单向流动。

## 五分钟起步

```bash
# 1. 用此模板建仓（或 git clone 后 cd 进去）
# 2. 原件丢进 raw/          —— PDF、docx、录音转写、旧草稿
# 3. 让 agent 读约定：
#      "读 wiki/SCHEMA.md，然后 ingest raw/<你的文件>"
# 4. 写渠道规则：
#      "按我的情况填 outputs/linkedin/SPEC.md"
# 5. 查结构：
python scripts/wiki_lint.py wiki/
```

适用于任何能读文件、能跑命令的 agent（Claude Code、Codex、Cursor、DSH，或能访问文件的对话）。`wiki/SCHEMA.md` 是入口契约：所有约定都在那里，或从那里一跳可达。

## 目录

```
AGENTS.md             给 agent 的操作规则与流程（先读这个）
raw/                  原件，不可变，不入库（PII）
wiki/                 事实层，LLM 独占维护
  SCHEMA.md           约定：页面类型、frontmatter、tag、铁律
  index.md            全站平铺索引
  log.md              只追加的历史：ingest / 修复 / 重构
  entities/           人、雇主、职位、客户、项目
  concepts/           技能、技术栈、方法
  sources/            每份原件一页摘要
  synthesis/          跨页综合：决定登记簿、对比
  graph/              可选编译图层（ontology.yaml 入库）
outputs/              产出层：规格 + 现状 + 草稿
  SPEC.md             一份合格渠道规格应有什么
  _template/          新渠道从这里复制
  linkedin/           SPEC.md + state.md
  cv/                 SPEC.md + state.md
docs/                 脱敏示例（虚构人物）——就地读，不在 lint 扫描路径上
scripts/              wiki_lint.py + build_index.py + check_translations.py——只用标准库，无需安装
```

想在动笔前先看约定怎么落地？就地读 [`docs/career/`](docs/career/README.md)——五个虚构页面，按顺序看。它们刻意放在 `wiki/` 之外，不影响 lint 与检索。

三语覆盖到"人真的需要读"的地方：`README.md`、`METHOD.md`、`AGENTS.md`、`CREDITS.md`、`wiki/SCHEMA.md`、`wiki/graph/README.md`、每一份 `SPEC.md`，以及整个 `docs/career/` 示例，都有 `.zh.md`（中）与 `.es.md`（西）译本，无后缀的那份是正本。每份译本首行写来源——`<!-- translation: es · canonical: wiki/SCHEMA.md · synced: 2026-11-14 -->`——`python scripts/check_translations.py` 会在译本缺失、标错或落后于正本时报错。需要译本的文件由 `.translations` 一行一个列出——不是"所有文件"：你自己的 wiki 页是数据，用你写作时用的语言就好。

有 8 个文件刻意保持单语，免译清单就写在那支脚本里：`wiki/index.md`（每次摄入都重写的目录）、`wiki/log.md`（只追加的历史，条目保留各自原语言）、`state.md` 账本（每次发布都变）、`wiki/.page-template.md`（片段）、`CLAUDE.md`（三行指针）、`raw/README.md`（在任何东西存在之前读一次）。译一本流水账不带来任何好处，却必然漂移。译本供人读；若与正本冲突，以正本为准。

## 什么该放哪一层

| 问题 | 层 | 例子 |
|---|---|---|
| 发生过什么？ | `raw/` | `raw/cv-2026.docx`、一段通话转写 |
| 什么是真的、只写一次？ | `wiki/entities/*` | 「雇主：Acme，2020-01 → 2024-02，混合办公」 |
| 这个渠道该怎么摆？ | `outputs/*/SPEC.md` | 「Headline ≤ 220；Projects 每块 ≤ 2,000」 |
| 我实际发了什么？ | `outputs/*/state.md` + `drafts/` | 「v1 于 2026-11-10 发布；待办：照片」 |

## 命令

```bash
python scripts/wiki_lint.py wiki/            # 死链、孤儿、frontmatter、渠道教条泄漏、claim ID、state 形状、PII
python scripts/wiki_lint.py wiki/ --json     # 同上，机器可读（CI 用这个）
python scripts/wiki_lint.py wiki/ --strict   # 警告也算失败，CI 可用
python scripts/wiki_lint.py wiki/ --no-pii   # 跳过 PII 扫描（剩下的靠名字，不是模式）
python scripts/wiki_lint.py --self-test      # 用九组已知坏样例检查检查器本身
python scripts/build_index.py wiki/          # 从页面重新生成 wiki/index.md（--check 只校验）
python scripts/check_translations.py         # 三语译本是否齐全、是否落后于正本
git ls-files raw/                            # 除 raw/README.md 外必须为空
```

零依赖、免安装，Python 3.9+。有 error 时退出码 1，可直接进 CI——见 [.github/workflows/lint.yml](.github/workflows/lint.yml)，它同时守住 raw/ 不入库与铁律 3。

结构之外，仍需人来判断的都是"意思"层面的检查：两页把同一个日期写岔、某条断言的原件不见了、事实改了而草稿还留着旧值。脚本现在接管了机械的那一半——claim ID 重复、草稿引用了没有页面定义的 claim、`state.md` 少了一节契约、PII 模式——到此为止。意思的活是 LLM 的。

想要语义检索或图层？它们在借来源头的 `llm-wiki` 技能里（`wiki_search.py`、`wiki_stats.py`、`wiki_graph_*.py`）。本模板不带也能用——markdown 才是正本。

## 四条铁律

1. **每个事实一个唯一来源。** 数字、日期、年限只在一个 wiki 页出现，其余页只链接。
2. **渠道是渲染器，不是作者。** `outputs/` 可以引用事实，不得引入事实。
3. **产出物永远不是来源。** 任何页的 `sources:` 不得出现 `outputs/`。
4. **先改事实，再改文案。** 动 `wiki/`，然后重生成草稿；不许只改草稿把 wiki 落在后面。

完整推演、失败分类、从单层 wiki 迁移的步骤见 [METHOD.zh.md](METHOD.zh.md)。

## 公开自己的副本之前

- [ ] `raw/` 只放你有权公开的东西；它默认被 gitignore，保持如此。
- [ ] `raw/` 之外不出现真实雇主、客户、同事姓名（除非你就是要公开）。
- [ ] 无电话、住址、生日、证件号、私人社媒链接。
- [ ] `outputs/**/drafts/` 已复查——草稿泄 PII 比 wiki 页更常见。
- [ ] `outputs/*/SPEC.md` 已通用化：平台上限是公开信息，你的个人实测值（「实测 75 字符」）不是。
- [ ] `wiki_lint.py` 无报错——它会抓页面与草稿里的邮箱、电话、绝对路径。
- [ ] 再跑 `grep -ri "<你的姓>" . --exclude-dir=.git`，以及每个雇主、客户名：姓名和街道地址没法用模式抓。

## 来源与许可

wiki 模式遵循 Andrej Karpathy 2026 年 4 月的 "LLM Wiki" gist。`SCHEMA.md` 的页面类型、slug 规则与图层谓词改编自 `llm-wiki` 技能（同源于那份 gist）；语义检索与图工具（`wiki_search.py`、`wiki_stats.py`、`wiki_graph_*.py`）归该技能所有，本仓库不转发。三层事实/产出拆分、渠道规格契约、`scripts/wiki_lint.py` 与 `METHOD.md` 是本模板原创。详见 [CREDITS.md](CREDITS.md)。

MIT 许可，见 [LICENSE](LICENSE)。
