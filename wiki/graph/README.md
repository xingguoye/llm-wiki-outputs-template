# Wiki Graph Layer

Compiled knowledge graph derived from the markdown wiki. **Markdown is canonical.** Everything here except `ontology.yaml` can be deleted and rebuilt.

```bash
# requires the `llm-wiki` skill — these tools are not bundled with this template
python scripts/wiki_graph_lint.py wiki/          # validate typed edges against the ontology
python scripts/wiki_graph_extract.py wiki/ --out wiki/graph
python scripts/wiki_graph_query.py wiki/ neighbors --node position:fullstack-acme
```

Nothing here is load-bearing: without the skill, the ontology stays a written convention you follow by hand, and the graph layer simply isn't compiled.

## Files

| File | Purpose | Tracking |
|---|---|---|
| `ontology.yaml` | Node types and predicates the graph recognises. The contract `wiki_graph_lint.py` validates against. | **Tracked. Edit by hand.** |
| `nodes.jsonl` | One JSON object per node, sorted by id. | Generated; ignored by default. |
| `edges.jsonl` | One JSON object per edge, sorted by id. Includes typed edges, `mentions`, `sourced_from`, `summarizes_raw`. | Generated; ignored by default. |
| `graph.sqlite` | Queryable index for `wiki_graph_query.py`. | Generated; ignored. |
| `graph.graphml` | Export for Gephi / yEd. | Generated; ignored. |

## When to use it

A career wiki is small. The graph earns its place at one specific question: **what touches what** — which clients sit under which position, which positions ran sequentially, which stack evidence backs which claim. That is a traversal question, and `grep` answers it badly once there are more than ~50 pages.

Do not use it as evidence. Edges accelerate navigation; the citation for a claim is the wiki page and, behind it, `raw/`.

## Workflow

1. Write the page and its facts first. Facts are markdown; the graph is downstream.
2. Add `graph.relationships` to frontmatter only when a source supports the edge.
3. `wiki_graph_lint.py` — catches unknown predicates, broken object references, missing evidence, alias collisions.
4. `wiki_graph_extract.py` — regenerate artifacts.
5. `wiki_graph_query.py` — `neighbors`, `edges`, `path`, `facts`.

## Anti-patterns

- **Hand-editing generated files.** Edit the markdown; regenerate.
- **Typed edges without evidence.** If the source doesn't say it, use a plain wikilink — `mentions` records the connection without overclaiming.
- **Encoding a timeline only in edges.** The period belongs in the page text too; the graph is an index of what the text says, not a second source of truth.
