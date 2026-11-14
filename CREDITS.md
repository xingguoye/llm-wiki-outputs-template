# Credits & provenance

## What came from where

| Component | Origin | Status |
|---|---|---|
| The "LLM Wiki" pattern (raw → curated markdown wiki → query/lint loop) | Andrej Karpathy's *LLM Wiki* gist, April 2026 | Idea, public |
| `wiki/SCHEMA.md` page types, slug rules, tag vocabulary, graph ontology conventions | Adapted from the author's `llm-wiki` agent skill, itself built on that gist | Adapted text, MIT here |
| Three-layer facts/outputs split, `outputs/SPEC.md` contract, channel-spec anatomy, `state.md` ledger | This template | MIT, original |
| `scripts/wiki_lint.py` | This template, written for the three-layer layout | MIT, original |
| `METHOD.md`, `METHOD.zh.md` | This template | MIT, original |
| `wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py` | The `llm-wiki` agent skill — **not included here** | Not redistributed; install the skill |

## Why the search and graph tools are not bundled

They live in the `llm-wiki` skill and carry no license header of their own. Rather than guess at redistribution rights, this repo ships only what it wrote: `scripts/wiki_lint.py`, which is dependency-free and covers the structural checks. If you want semantic search or the compiled graph, install the skill and point its scripts at your `wiki/`. Markdown stays canonical either way.

Importing them into your own fork is fine for private use. If you republish them, check the skill's provenance first — that is your call to make, not this repo's to make for you.

## Attribution line

If you reuse the method, a link back is enough:

> Structure adapted from *LLM Wiki + Outputs*, itself following Andrej Karpathy's LLM Wiki pattern.
