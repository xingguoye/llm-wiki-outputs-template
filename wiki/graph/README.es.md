<!-- translation: es · canonical: wiki/graph/README.md · synced: 2026-11-14 -->

# Capa de grafo del wiki

Grafo de conocimiento compilado a partir del wiki en markdown. **El markdown es el canónico.** Todo lo que hay aquí salvo `ontology.yaml` puede borrarse y regenerarse.

```bash
# requiere la skill `llm-wiki`: estas herramientas no se incluyen en la plantilla
python scripts/wiki_graph_lint.py wiki/          # valida las aristas tipadas contra la ontología
python scripts/wiki_graph_extract.py wiki/ --out wiki/graph
python scripts/wiki_graph_query.py wiki/ neighbors --node position:fullstack-acme
```

Nada de esto es imprescindible: sin la skill, la ontología sigue siendo una convención escrita que aplicas a mano y la capa de grafo simplemente no se compila.

## Archivos

| Archivo | Para qué | Versionado |
|---|---|---|
| `ontology.yaml` | Tipos de nodo y predicados que el grafo reconoce. El contrato contra el que valida `wiki_graph_lint.py`. | **Versionado. Se edita a mano.** |
| `nodes.jsonl` | Un objeto JSON por nodo, ordenado por id. | Generado; ignorado por defecto. |
| `edges.jsonl` | Un objeto JSON por arista, ordenado por id. Incluye aristas tipadas, `mentions`, `sourced_from` y `summarizes_raw`. | Generado; ignorado por defecto. |
| `graph.sqlite` | Índice consultable para `wiki_graph_query.py`. | Generado; ignorado. |
| `graph.graphml` | Exportación para Gephi / yEd. | Generado; ignorado. |

## Cuándo usarla

Un wiki de carrera es pequeño. El grafo se gana su sitio con una pregunta concreta: **qué toca qué** — qué clientes cuelgan de qué puesto, qué puestos fueron consecutivos y qué evidencia de stack respalda qué afirmación. Es una pregunta de recorrido, y `grep` la responde mal a partir de unas ~50 páginas.

No lo uses como evidencia. Las aristas aceleran la navegación; la cita de una afirmación es la página del wiki y, detrás, `raw/`.

## Flujo de trabajo

1. Escribe primero la página y sus hechos. Los hechos son markdown; el grafo va después.
2. Añade `graph.relationships` al frontmatter solo cuando una fuente respalde la arista.
3. `wiki_graph_lint.py`: detecta predicados desconocidos, referencias de objeto rotas, evidencia ausente y colisiones de alias.
4. `wiki_graph_extract.py`: regenera los artefactos.
5. `wiki_graph_query.py`: `neighbors`, `edges`, `path`, `facts`.

## Antipatrones

- **Editar a mano los archivos generados.** Edita el markdown; regenera.
- **Aristas tipadas sin evidencia.** Si la fuente no lo dice, usa un wikilink normal: `mentions` registra la conexión sin exagerar la afirmación.
- **Codificar la cronología solo en las aristas.** El periodo también va en el texto de la página; el grafo es un índice de lo que dice el texto, no una segunda fuente de verdad.
