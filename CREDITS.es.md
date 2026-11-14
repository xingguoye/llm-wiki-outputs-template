<!-- translation: es · canonical: CREDITS.md · synced: 2026-11-14 -->

# Créditos y procedencia

## De dónde viene cada pieza

| Componente | Origen | Estado |
|---|---|---|
| El patrón "LLM Wiki" (fuentes → wiki markdown curada por el LLM → ciclo de consulta y lint) | El gist *LLM Wiki* de Andrej Karpathy, abril de 2026 | Idea, pública |
| Tipos de página, reglas de slug, vocabulario de etiquetas y convenciones de ontología de `wiki/SCHEMA.md` | Adaptado de la skill de agente `llm-wiki` del autor, que a su vez se basa en ese gist | Texto adaptado, aquí con licencia MIT |
| La separación en tres capas, el contrato `outputs/SPEC.md`, la anatomía de una especificación de canal y el registro `state.md` | Esta plantilla | MIT, original |
| `scripts/wiki_lint.py` | Esta plantilla, escrito para el diseño de tres capas | MIT, original |
| `METHOD.md`, `METHOD.zh.md` | Esta plantilla | MIT, original |
| `wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py` | La skill de agente `llm-wiki` — **no se incluyen aquí** | No se redistribuyen; instala la skill |

## Por qué no se empaquetan las herramientas de búsqueda y grafo

Viven en la skill `llm-wiki` y no llevan cabecera de licencia propia. En lugar de adivinar los derechos de redistribución, este repositorio incluye solo lo que ha escrito: `scripts/wiki_lint.py`, sin dependencias y con las comprobaciones estructurales cubiertas. Si quieres búsqueda semántica o el grafo compilado, instala la skill y apunta sus scripts a tu `wiki/`. En cualquier caso, el markdown sigue siendo el canónico.

Importarlas en tu propio fork para uso privado es perfectamente válido. Si las republicas, comprueba antes la procedencia de la skill: esa decisión es tuya, no de este repositorio.

## Línea de atribución

Si reutilizas el método, basta con un enlace de vuelta:

> Estructura adaptada de *LLM Wiki + Outputs*, que a su vez sigue el patrón LLM Wiki de Andrej Karpathy.
