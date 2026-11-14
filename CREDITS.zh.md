<!-- translation: zh · canonical: CREDITS.md · synced: 2026-11-14 -->

# 致谢与来源

## 各部分从哪来

| 组成 | 来源 | 状态 |
|---|---|---|
| "LLM Wiki" 模式（原件 → 由 LLM 整理的 markdown wiki → 查询/lint 循环） | Andrej Karpathy 的 *LLM Wiki* gist，2026 年 4 月 | 理念，公开 |
| `wiki/SCHEMA.md` 的页面类型、slug 规则、tag 词表、图本体约定 | 改编自作者的 `llm-wiki` agent 技能，该技能本身建立在那份 gist 上 | 改编文本，此处以 MIT 授权 |
| 三层事实/产出拆分、`outputs/SPEC.md` 契约、渠道规格解剖、`state.md` 台账 | 本模板 | MIT，原创 |
| `scripts/wiki_lint.py` | 本模板，为三层布局而写 | MIT，原创 |
| `METHOD.md`、`METHOD.zh.md` | 本模板 | MIT，原创 |
| `wiki_search.py`、`wiki_stats.py`、`wiki_graph_*.py` | `llm-wiki` agent 技能——**未包含在本仓库** | 不转发；请安装该技能 |

## 为什么不打包检索与图工具

它们属于 `llm-wiki` 技能，且自身没有许可证声明。与其猜测转发权限，本仓库只收录自己写的东西：`scripts/wiki_lint.py`，零依赖，覆盖结构类检查。想要语义检索或编译图层，就安装该技能，把它的脚本指向你的 `wiki/`。无论哪种方式，markdown 始终是正本。

把它们导入你自己的 fork 用于私人用途没问题。若你要转发，请先核实该技能的来源——那是你的决定，不是本仓库替你做的决定。

## 署名行

若你复用这套方法，附一个回链就够了：

> 结构改编自 *LLM Wiki + Outputs*，其本身遵循 Andrej Karpathy 的 LLM Wiki 模式。
