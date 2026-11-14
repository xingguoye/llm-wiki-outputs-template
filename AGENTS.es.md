<!-- translation: es · canonical: AGENTS.md · synced: 2026-11-14 -->

# Instrucciones para el agente

Mantienes una base de conocimiento con tres capas. Lee este archivo y después `wiki/SCHEMA.md`. Esos dos archivos anulan cualquier convención genérica de wiki que hayas aprendido.

## Orden de lectura

1. `AGENTS.md` (este archivo): reglas de operación y playbooks.
2. `wiki/SCHEMA.md`: tipos de página, frontmatter, etiquetas, nomenclatura, cadencia de lint.
3. `outputs/SPEC.md`: el contrato de una especificación de destino.
4. `wiki/index.md` y `wiki/log.md`: estado actual e historial.
5. `METHOD.md`: solo cuando el porqué de una regla no esté claro o estés a punto de incumplirla.

## El límite que no puedes cruzar

| Capa | Puedes | No puedes |
|---|---|---|
| `raw/` | leer | escribir, renombrar, "arreglar" ni versionar |
| `wiki/` | crear, reescribir, fusionar, borrar | guardar reglas de canal, PII ni copias de borradores |
| `outputs/` | crear borradores, actualizar state/SPEC | introducir un hecho ni ser citado como fuente |

Cuatro leyes, por orden de prioridad:

1. Una sola fuente de verdad por hecho. Los totales viven en una página; el resto enlaza.
2. Los destinos renderizan hechos; nunca los redactan.
3. Nada de `outputs/` puede aparecer en un campo `sources:` ni tratarse como evidencia.
4. Cuando un hecho está mal, corrige `wiki/` primero y vuelve a renderizar. Nunca parchees un borrador para corregir un hecho.

## Playbooks

### Ingerir una fuente

1. Confirma que el archivo está en `raw/` (cópialo allí si no lo está; nunca lo edites).
2. Escribe `wiki/sources/<slug>.md`: qué es, para qué sirve, qué resulta poco fiable, qué páginas alimenta.
3. Actualiza cada página de entidad o concepto afectada. Un hecho por línea, el periodo primero cuando exista periodo.
4. Si contradice una página existente, resuélvelo en la página que **posee** el hecho y anota la resolución en `log.md`.
5. Añade las páginas nuevas a `index.md`; añade una entrada `ingest` a `log.md`.
6. Ejecuta `python scripts/wiki_lint.py wiki/`. Los enlaces rotos y las huérfanas son tuyos: arréglalos antes de dar nada por terminado.

### Responder una pregunta sobre el wiki

1. Primero `python scripts/wiki_lint.py wiki/` (barato) y después busca: lee `wiki/index.md` y sigue sus resúmenes de una línea; `grep -rn "<term>" wiki/` suele bastar. Si la skill `llm-wiki` está instalada, su `wiki_search.py` ofrece recuperación por secciones con ranking.
2. Lee las páginas que devuelva; sigue los enlaces hasta las páginas que poseen los hechos relevantes.
3. Responde solo con texto del wiki. Si la respuesta exige un hecho que el wiki no tiene, dilo y propón la ingesta que lo aportaría. No rellenes el hueco con conocimiento general y lo presentes como contenido del wiki.
4. Si la respuesta es reutilizable (una comparación, una decisión), archívala como página `synthesis` y regístrala.

### Renderizar un canal

1. Lee `outputs/<channel>/SPEC.md` y las páginas del wiki que aparecen en su mapeo de hechos.
2. Redacta en `outputs/<channel>/drafts/<YYYY-MM>/`, un archivo por idioma.
3. Mide los límites con un script (`len()`), no a ojo. Si te pasas, corrige el borrador —nunca el wiki, salvo que el hecho esté mal.
4. Recorre la lista de aceptación y la lista de prohibiciones de la especificación.
5. Actualiza `outputs/<channel>/state.md`: versión, fecha, valores medidos, desviaciones.
6. Añade una entrada `output` a `wiki/log.md` que enlace a la entrada de estado.

### Lint

```bash
python scripts/wiki_lint.py wiki/          # enlaces rotos, huérfanas, frontmatter, fugas de capa, PII
python scripts/wiki_lint.py wiki/ --strict # los avisos también fallan (úsalo en CI)
```

Ese script es toda la cadena de herramientas del repositorio: solo biblioteca estándar. La búsqueda semántica y la capa de grafo son opcionales y viven en la skill `llm-wiki` (`wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py`); instálala si las quieres.

Informa los hallazgos como lista con file:line. Arregla lo mecánico (enlaces rotos, frontmatter ausente); propón los cambios de contenido en vez de hacerlos en silencio.

## Reglas de estilo

- Hechos, no adjetivos. Nada de "passionate", "innovative" ni "results-driven" en las páginas del wiki.
- El periodo primero: `2021-01 → 2024-02 · Hybrid · Madrid — Role name`.
- Nunca repitas un total que posee otra página; enlaza.
- Los números llevan su base: "9+ years (as of 2026-11)", no "9+ years".
- La PII nunca entra en `wiki/`: ni teléfono, ni dirección, ni documento, ni fecha de nacimiento, ni URL privada. Si un borrador necesita alguno, lo aporta el usuario al renderizar.

## Cuando dudes

- Una restricción (límite de caracteres, número de páginas, nivel de idioma) → pertenece a un `outputs/*/SPEC.md`. Ponla allí.
- Un hecho (fecha, periodo, tecnología, cliente) → pertenece a `wiki/`. Ponlo allí, con su página de origen.
- Ambas cosas a la vez → escribe primero el hecho y después la regla de canal que lo renderiza.
