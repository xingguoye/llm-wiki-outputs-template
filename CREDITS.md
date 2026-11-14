# Credits & provenance

## What came from where

| Component | Origin | Status |
|---|---|---|
| The "LLM Wiki" pattern (raw → curated markdown wiki → query/lint loop) | Andrej Karpathy's *LLM Wiki* gist, April 2026 | Idea, public |
| `scripts/*.py` (`wiki_lint`, `wiki_search`, `wiki_stats`, `wiki_graph_*`, `setup_wiki`) | The author's local `llm-wiki` agent skill, built on that gist | **Check before republishing** — see below |
| `wiki/SCHEMA.md` structure, page types, graph ontology conventions | Same skill's `assets/*.template` | Adapted |
| Three-layer facts/outputs split, `outputs/SPEC.md` contract, channel-spec anatomy, `state.md` ledger | This template | MIT, original |
| `METHOD.md`, `METHOD.zh.md` | This template | MIT, original |

## Before you publish a public copy

If you fork this template to share publicly, confirm you have the right to redistribute the files in `scripts/`:

- They were created for the `llm-wiki` skill and carry no explicit license header. If you wrote them, publish them under your chosen license and say so here. If you did not, either (a) obtain permission, (b) replace them with your own implementations, or (c) ship the repo without `scripts/` and link to the skill instead.
- The pattern itself is not restricted — ideas aren't licensed — but the code is a separate question from the idea.

The MIT license in [LICENSE](LICENSE) covers the template's own text. It cannot grant rights to code you did not write.

## Attribution line

If you reuse the method, a link back is enough:

> Structure adapted from *LLM Wiki + Outputs* (this repo), itself following Andrej Karpathy's LLM Wiki pattern.
