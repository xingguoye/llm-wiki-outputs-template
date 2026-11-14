<!-- translation: zh · canonical: wiki/graph/README.md · synced: 2026-11-14 -->

# Wiki 图层

由 markdown wiki 编译出的知识图谱。**markdown 是正本。** 除 `ontology.yaml` 外，这里的一切都可以删掉重建。

```bash
# 需要 `llm-wiki` 技能——这些工具不随本模板分发
python scripts/wiki_graph_lint.py wiki/          # 按本体校验带类型的边
python scripts/wiki_graph_extract.py wiki/ --out wiki/graph
python scripts/wiki_graph_query.py wiki/ neighbors --node position:fullstack-acme
```

这里没有任何东西是承重的：不装技能时，本体只是一份你手动遵守的书面约定，图层干脆不编译。

## 文件

| 文件 | 用途 | 版本控制 |
|---|---|---|
| `ontology.yaml` | 图谱承认的节点类型与谓词。`wiki_graph_lint.py` 依据它校验。 | **入库。手工编辑。** |
| `nodes.jsonl` | 每个节点一个 JSON 对象，按 id 排序。 | 生成物；默认忽略。 |
| `edges.jsonl` | 每条边一个 JSON 对象，按 id 排序。包含带类型的边、`mentions`、`sourced_from`、`summarizes_raw`。 | 生成物；默认忽略。 |
| `graph.sqlite` | 供 `wiki_graph_query.py` 查询的索引。 | 生成物；忽略。 |
| `graph.graphml` | 供 Gephi / yEd 导出的文件。 | 生成物；忽略。 |

## 什么时候用它

职业 wiki 很小。图层只对一个问题真正有价值：**什么连着什么**——哪些客户挂在哪个职位下、哪些职位是先后接续的、哪段技术栈证据支撑哪条断言。这是个遍历问题，一旦超过约 50 页，`grep` 就答得很差。

不要把它当证据。边只是加速导航；一条断言的引用是 wiki 页，以及它背后的 `raw/`。

## 工作流

1. 先写页面和事实。事实在 markdown 里；图层在下游。
2. 只有当来源支持某条边时，才在 frontmatter 里写 `graph.relationships`。
3. `wiki_graph_lint.py`——抓未知谓词、断裂的对象引用、缺失证据、别名冲突。
4. `wiki_graph_extract.py`——重新生成产物。
5. `wiki_graph_query.py`——`neighbors`、`edges`、`path`、`facts`。

## 反模式

- **手改生成物。** 改 markdown，然后重新生成。
- **没有证据的带类型边。** 来源没说的，就用普通 wikilink——`mentions` 记录连接但不过度断言。
- **只在边里编码时间线。** 时间段也要写进页面正文；图层是正文的索引，不是第二个事实出处。
