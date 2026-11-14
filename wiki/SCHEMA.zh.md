<!-- translation: zh · canonical: wiki/SCHEMA.md · synced: 2026-11-14 -->

# Wiki 规范

这份文件是本 wiki 的契约。在摄入或编辑任何内容之前先读它。当它与任何模板或技能的默认做法冲突时，**以本文件为准**。

## 三层

| 层 | 路径 | 规则 |
|---|---|---|
| 原件 | `raw/` | 不可变、私有、永不提交。只作证据。 |
| 事实 | `wiki/` | 事实唯一的诞生地，由 LLM 维护。 |
| 去处 | `outputs/` | 字段顺序、上限、语言、禁写断言、已发布文案。 |

流向是单向的：`raw/` → `wiki/` → `outputs/`。不回写。

## 四条铁律

1. **一个事实只有一个出处。** 一个数字、日期或时间段只出现在一页里，其他页面按 slug 链接过去。
2. **去处是渲染器，不是作者。** `outputs/` 可以引用、压缩、翻译、重排；不得引入事实。
3. **交付物永远不是来源。** 任何 `sources:` 字段都不得引用 `outputs/`。若某草稿知道 wiki 不知道的事，要么带着真实来源把它提升进 wiki，要么删掉。
4. **先改事实。** 先编辑 wiki 页，再重新渲染草稿。

## 页面类型

| 类型 | 目录 | 存放 |
|---|---|---|
| `source` | `wiki/sources/` | `raw/` 里每份被摄入文件对应一个摘要页。 |
| `entity` | `wiki/entities/` | 一个具体对象：一个人、一家雇主、一个职位、一个客户、一个项目、一段教育经历。 |
| `concept` | `wiki/concepts/` | 一个技术栈、一组技能、一种方法、一个反复出现的想法。 |
| `synthesis` | `wiki/synthesis/` | 跨页页面：决定登记簿、对比、归档的问答。 |

用 frontmatter 里的 `kind:` 细分实体：`person`、`company`、`position`、`client`、`project`、`education`。

## 命名

- slug 一律小写、ASCII、用连字符：`position-fullstack-acme`、`stack-dotnet`。
- 一个实体一页；同一实体出现两次就合并，保留 `aliases:` 列表。
- 便于扫读时按类型加前缀：`position-*`、`client-*`、`stack-*`、`source-*`。

## Frontmatter

每页都要有：

```yaml
---
title: "人类可读的标题"
created: 2026-01-31
type: entity            # source | entity | concept | synthesis
kind: position          # 仅实体页
tags: [position, timeline]
sources: [source-cv-2026]   # source 摘要页的 slug；绝不写 outputs/
updated: 2026-01-31
---
```

原件页额外带 `raw:`（文件路径）、`ingested:`，可选 `authors:` / `url:`。

让 lint 保持绿的规则：

- 每页都有 `title`、`created`、`type`、`tags`、`updated`。没有例外。
- `sources:` 只指向 `wiki/sources/` 下页面的 slug。
- frontmatter 只写在 `---` 之上一次；正文里绝不重复键。

## 页面解剖

1. 一行定义（用最朴素的话说这是什么）。
2. 事实，每条在有时点时带上日期或时间段。
3. 链接出去，指向拥有相关事实的页面。
4. 只在来源不显然时写一条 "sources" 说明。

事实要原子化。"截至 2026-11 共 9 年 6 个月"属于人物页；职位页写 "2020-01 → 2024-02"，总数链接到人物页。两页绝不可各自独立地写出同一个总数。

## 篇幅

- 软上限：400 行 / 约 2,000 词。超过就拆。
- 硬上限：800 行。
- 若某页某一节的事实超过约 12 条，那是两页。

## Tag

这份清单要短；一个有 200 个 tag 的 wiki 等于没有 tag。当前词表：

| Tag | 含义 |
|---|---|
| `timeline` | 日期、时间段、先后顺序 |
| `claim` | 可能被人质疑的断言 |
| `decision` | 后续工作必须遵守的裁定 |
| `skill` | 技术与能力 |
| `client` | 工作为谁交付 |
| `gap` | 已知的未知；需要一份来源 |

先在本文登记，再在页面上使用。

## 产出层

每个去处都在 `outputs/` 下有一个目录，恰好包含：

```
outputs/<channel>/
  SPEC.md      该去处的规则（必需章节见 outputs/SPEC.md）
  state.md     当前已发布的是什么，外加版本表
  drafts/      每次发布一个子目录
```

新增渠道时在此登记：

| 渠道 | 规格 | 状态 |
|---|---|---|
| `linkedin` | `outputs/linkedin/SPEC.md` | 起手版已填写 |
| `cv` | `outputs/cv/SPEC.md` | 起手版已填写 |

渠道规格不得包含事实。它指向 wiki slug 并陈述约束。

## 摄入流程

1. 把文件复制进 `raw/`；之后永不编辑它。
2. 写 `wiki/sources/<slug>.md`：它是什么、哪里有用、哪里不可靠、喂养哪些页面。
3. 更新它触及的每个实体/概念页。若与其他页矛盾，在*拥有*该事实的页面里解决，并在 `log.md` 记录。
4. 把新页加入 `index.md`。
5. 追加到 `log.md`。
6. 跑 `python scripts/wiki_lint.py wiki/`。

## Log 纪律

`log.md` 只追加，最新的在最后。每次改动 wiki 的会话记一条。每条包含：日期、类型（ingest / fix / refactor / lint）、2–6 条要点、验证结果。永远不要重写其中的历史；若之前写错了，在新条目里说明。

## Lint 节奏

- 每次摄入后做结构 lint：`python scripts/wiki_lint.py wiki/`（CI 里加 `--strict`）。
- 每 5 次摄入做一次通读，找矛盾。
- 可选，若装了 `llm-wiki` 技能：每月用 `wiki_stats.py` 看漂移，重建图层前用 `wiki_graph_lint.py`。

## 用户偏好

（空。当某种风格偏好浮现时——"先写时间段再写职责"、"事实页绝不用营销形容词"——记在这里，让它在跨会话后仍留存。）
