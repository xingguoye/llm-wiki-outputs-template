<!-- translation: zh · canonical: README.md · synced: 2026-11-14 -->
# LLM Wiki + Outputs

一套个人知识库模板：用**一份**事实，喂给**多个去处**——简历、LinkedIn 档案、作品集页面、面试回答。

它是 "LLM Wiki" 模式（不可变来源 → 由 LLM 维护的 markdown wiki → lint / 查询循环），只多了一处结构性差异：一层独立的**产出层**，用来存放每个去处的规则，让这些规则永远不会渗回事实里。

wiki 本身由 agent 撰写和维护。把新的 CV、一次电话的转写或一份职位描述丢进 `raw/`，让它 ingest，它只改这条新事实牵连到的页面——你审 diff，它负责打字。

- [English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [方法](METHOD.md)

[![lint](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml/badge.svg)](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml)

## 它解决什么问题

一个同时存着简历文案的 wiki，会朝两个方向腐烂：

1. **渠道规则渗进事实。** "Headline ≤ 220 字符"被抄进六个实体页；平台一改上限，你得动九个文件。
2. **产出物被当成来源引用。** LinkedIn 草稿成了它自己引用的那些日期的"来源"。于是事实没了出处，wiki 开始引用自己。

解法不是更强的纪律，而是一条边界：事实住在 `wiki/`，去处规则住在 `outputs/<channel>/SPEC.md`，流向只有一个方向。

## 快速开始

```bash
# 1. 使用本模板，或：git clone https://github.com/xingguoye/llm-wiki-outputs-template my-wiki && cd my-wiki
# 2. 把你的来源丢进 raw/            —— PDF、docx、录音转写、旧草稿
# 3. 让 agent 读 schema：
#      "Read wiki/SCHEMA.md, then ingest raw/<your-file>"
# 4. 写去处规则：
#      "Fill outputs/linkedin/SPEC.md for my case"
# 5. 检查结构：
python scripts/wiki_lint.py wiki/
```

能读文件、能跑 shell 的 agent 都能用（Claude Code、Codex、Cursor、DSH、有文件访问权的普通对话）。`wiki/SCHEMA.md` 是入口契约——agent 需要的每条约定都在那里，或者只差一个链接。

## 目录结构

```
AGENTS.md             给 agent 的操作规则 + playbook（先读这个）
raw/                  不可变来源。永不编辑、永不提交（含 PII）。
wiki/                 事实层。由 LLM 维护。
  SCHEMA.md           约定：页面类型、frontmatter、tag、铁律
  index.md            所有页面的平铺索引
  log.md              只追加的历史：ingest、修复、重构
  entities/           人、雇主、职位、客户、项目
  concepts/           技能、技术栈、方法
  sources/            每份被 ingest 的来源一页摘要
  synthesis/          横切页面：决定登记簿、对比
  graph/              可选的编译图（ontology.yaml 入库）
outputs/              产出层。规格、账本、草稿。
  SPEC.md             一份合格的渠道 SPEC 必须包含什么
  _template/          新增渠道时复制这一份
  linkedin/           SPEC.md + state.md
  cv/                 SPEC.md + state.md
docs/                 完整示例（虚构）——就地阅读，不在 lint 路径里
scripts/              wiki_lint.py + build_index.py + check_translations.py——纯标准库，无需安装
.translations         可选清单：哪些文档另有其他语言版本（目前：本 README）
```

**文档以英文为准，翻译是按需加入的；本 README 就是它的示范。** 它的两个侧车（`README.zh.md`、`README.es.md`）在 `.translations` 里各占一行，每份开头是一行来源标记：

```
<!-- translation: es · canonical: README.md · synced: 2026-11-14 -->
```

没有后缀的那份是正本，两者冲突时以它为准；`python scripts/check_translations.py` 在侧车缺失、标记错误或过期时会失败。仓库其余部分保持英文，直到真的出现需要其他语言的读者——翻译是一份"会重读"的承诺，没人读的翻译是仓库里最旧的谎话。

想在动笔之前先看约定在实战中的样子？就地读 [`docs/career/`](docs/career/README.md)——七页虚构示例，按顺序读。它们刻意放在 `wiki/` 之外，因此不影响 lint 和检索。

**本仓库不附带任何真实实例，也不应该加入。** `docs/career/` 全是虚构的：人物、雇主、客户和日期都是编的。一个真正在用的 wiki 是私人数据——一个名字、一个雇主、几个客户名再加四个日期，就足以指认到具体的人——所以完成后的实例留在它被写下的地方，绝不复制进本仓库，也不以同一许可证发布。PII 扫描能抓邮箱、电话和绝对路径；它认不出姓名和公司名，那部分判断留在人工。

## 什么放在哪里

| 问题 | 层 | 例子 |
|---|---|---|
| 发生了什么？ | `raw/` | `raw/cv-2026.docx`、一次电话的转写 |
| 什么是真的，且只写一次？ | `wiki/entities/*` | "雇主：Acme，2020-01 → 2024-02，混合办公" |
| 这个去处必须如何呈现它？ | `outputs/*/SPEC.md` | "Headline ≤ 220；Projects 块 ≤ 2,000" |
| 我实际发布了什么？ | `outputs/*/state.md` + `drafts/` | "v1 于 2026-11-10 上线；待办：照片" |

## 命令

```bash
python scripts/wiki_lint.py wiki/            # 检查项：wiki/SCHEMA.md 的 § Lint cadence
python scripts/wiki_lint.py wiki/ --json     # 同上，机器可读（CI 用这个）
python scripts/wiki_lint.py wiki/ --strict   # 警告也算失败；CI 里用
python scripts/wiki_lint.py wiki/ --no-pii   # 跳过 PII 扫描（姓名不是模式能抓的，仍靠人工）
python scripts/wiki_lint.py --self-test      # 用已知坏样本检验检查器本身
python scripts/build_index.py wiki/          # 由页面重写 wiki/index.md（--check 校验是否过期）
python scripts/check_translations.py         # 你声明的翻译是否齐全、是否过期
git ls-files raw/                            # 除 raw/README.md 外必须为空
```

无依赖、无需安装。Python 3.9+。有错误时退出码 1，可以直接进 CI——见 [.github/workflows/lint.yml](.github/workflows/lint.yml)，它还守着 raw/ 隐私规则与铁律 3。

结构之外的检查仍需人来判断，判断的是**意思**：两页用不同说法写同一个日期、某条 claim 的来源消失了、事实已经改了而草稿还留着旧值。脚本覆盖机械的那一半——确切清单在 `wiki/SCHEMA.md` 的 § Lint cadence——到此为止。意思是 LLM 的活。

可选：如果你想要语义检索或图层，它们在本模板借用了约定的 `llm-wiki` agent skill 里（`wiki_search.py`、`wiki_stats.py`、`wiki_graph_*.py`）。装上，把脚本指向你的 `wiki/`。没有它们模板照样能用——markdown 才是正本。

## 四条铁律

1. **每个事实只有一个来源。** 一个数字、一个日期、一段时间，只出现在一个 wiki 页面里；其他页面链接到它。
2. **去处只负责呈现，不负责创作。** `outputs/` 可以引用事实，永不引入事实。
3. **产出物永远不是来源。** 任何页面都不得在 `sources:` 里引用 `outputs/`。
4. **先改事实。** 先改 `wiki/`，再重新生成草稿。永远不要改草稿而把 wiki 留在原地。

完整论证、失败分类与迁移步骤：[METHOD.md](METHOD.md)。

## 发布你自己的副本之前

- [ ] `raw/` 里只放你有权公开的东西；它默认被 gitignore——保持这样。
- [ ] `raw/` 之外没有雇主、客户或同事的真实姓名，除非你就是要公开。
- [ ] 没有电话、住址、出生日期、证件号、私人主页链接。
- [ ] 检查过 `outputs/**/drafts/`——草稿比 wiki 页更容易泄漏 PII。
- [ ] `outputs/*/SPEC.md` 已泛化：平台上限是公开的，你的个人实测值（"实测 75 字符"）不是。
- [ ] `wiki_lint.py` 干净——它会标出页面与草稿里的邮箱、电话和绝对家目录路径。
- [ ] 然后 `grep -ri "<你的姓>" . --exclude-dir=.git`，对每个雇主名和客户名再做一遍：姓名和街道地址无法靠模式匹配发现。

## 致谢

这个 wiki 模式源自 Andrej Karpathy 的 "LLM Wiki" gist（2026 年 4 月）。`SCHEMA.md` 的约定与页面/图词汇改编自 `llm-wiki` agent skill，后者建立在该 gist 之上——这个 skill 拥有 `wiki_search.py`、`wiki_stats.py` 与 `wiki_graph_*` 工具，本仓库不再分发它们。三层事实/产出的拆分、渠道 SPEC 契约、`scripts/wiki_lint.py` 与 `METHOD.md` 属于本模板原创。细节见 [CREDITS.md](CREDITS.md)。

## 许可证

MIT——见 [LICENSE](LICENSE)。
