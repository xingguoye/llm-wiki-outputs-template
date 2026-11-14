<!-- translation: es · canonical: wiki/SCHEMA.md · synced: 2026-11-14 -->

# Esquema del wiki

Este archivo es el contrato del wiki. Léelo antes de ingerir o editar nada. Cuando contradiga cualquier valor por defecto de una plantilla o de una skill, **manda este archivo**.

## Las tres capas

| Capa | Ruta | Regla |
|---|---|---|
| Fuentes | `raw/` | Inmutables, privadas, nunca versionadas. Solo evidencia. |
| Hechos | `wiki/` | El único lugar donde puede nacer un hecho. Lo mantiene el LLM. |
| Destinos | `outputs/` | Orden de campos, límites, idioma, afirmaciones prohibidas, texto publicado. |

El flujo es unidireccional: `raw/` → `wiki/` → `outputs/`. Nada vuelve atrás.

## Las cuatro leyes

1. **Una fuente de verdad por hecho.** Un número, una fecha o un periodo aparecen en exactamente una página. Las demás enlazan a ella por slug.
2. **Los destinos renderizan, no redactan.** `outputs/` puede citar, comprimir, traducir y reordenar. No puede introducir un hecho.
3. **Los entregables nunca son fuentes.** Ningún campo `sources:` puede referenciar `outputs/`. Si un borrador sabe algo que el wiki no sabe, promuévelo al wiki con una fuente real o bórralo.
4. **Primero cambia el hecho.** Edita la página del wiki y después vuelve a renderizar los borradores.

## Tipos de página

| Tipo | Directorio | Contiene |
|---|---|---|
| `source` | `wiki/sources/` | Una página resumen por cada archivo ingerido de `raw/`. |
| `entity` | `wiki/entities/` | Algo concreto: una persona, un empleador, un puesto, un cliente, un proyecto, una formación. |
| `concept` | `wiki/concepts/` | Un stack, un grupo de habilidades, un método, una idea recurrente. |
| `synthesis` | `wiki/synthesis/` | Páginas transversales: registros de decisiones, comparaciones, respuestas archivadas. |

Usa `kind:` en el frontmatter para subdividir entidades: `person`, `company`, `position`, `client`, `project`, `education`.

## Nomenclatura

- Los slugs van en minúsculas, ASCII y con guiones: `position-fullstack-acme`, `stack-dotnet`.
- Una página por entidad; si la misma entidad aparece dos veces, fusiónalas y conserva una lista `aliases:`.
- Pon prefijo por tipo cuando ayude a escanear: `position-*`, `client-*`, `stack-*`, `source-*`.

## Frontmatter

Todas las páginas:

```yaml
---
title: "Título legible para personas"
created: 2026-01-31
type: entity            # source | entity | concept | synthesis
kind: position          # solo entidades
tags: [position, timeline]
sources: [source-cv-2026]   # slugs de páginas de wiki/sources/; nunca outputs/
updated: 2026-01-31
---
```

Las páginas de fuente llevan además `raw:` (la ruta del archivo), `ingested:` y, opcionalmente, `authors:` / `url:`.

Reglas que mantienen el lint en verde:

- `title`, `created`, `type`, `tags` y `updated` en todas las páginas. Sin excepciones.
- `sources:` apunta solo a slugs de páginas de `wiki/sources/`.
- Escribe el frontmatter una vez, encima de los `---`; nunca repitas claves en el cuerpo.

## Anatomía de una página

1. Una definición de una línea (qué es esto, con las palabras más llanas).
2. Hechos, cada uno con su fecha o periodo cuando lo tenga.
3. Enlaces salientes a las páginas que poseen los hechos relacionados.
4. Una nota de "fuentes" solo cuando la procedencia no sea obvia.

Mantén los hechos atómicos. "9 años 6 meses a fecha de 2026-11" pertenece a la página de la persona; la página del puesto dice "2020-01 → 2024-02" y enlaza a la de la persona para el total. Dos páginas nunca deben declarar el mismo total por separado.

## Tamaño

- Límite blando: 400 líneas / ~2.000 palabras. Más allá, divide.
- Límite duro: 800 líneas.
- Si una página tiene más de ~12 hechos en una sección, son dos páginas.

## Etiquetas

Mantén la lista corta; un wiki con 200 etiquetas no tiene ninguna. Vocabulario actual:

| Etiqueta | Significado |
|---|---|
| `timeline` | fechas, periodos, orden |
| `claim` | una afirmación que alguien podría discutir |
| `decision` | una resolución que el trabajo futuro debe respetar |
| `skill` | tecnologías y capacidades |
| `client` | para quién se entregó el trabajo |
| `gap` | incógnita conocida; necesita una fuente |

Registra la etiqueta aquí antes de usarla en una página.

## Salidas

Cada destino recibe un directorio dentro de `outputs/` que contiene exactamente:

```
outputs/<channel>/
  SPEC.md      reglas del destino (las secciones obligatorias están en outputs/SPEC.md)
  state.md     qué está publicado ahora mismo, más una tabla de versiones
  drafts/      un subdirectorio por publicación
```

Registra cada canal aquí cuando añadas uno:

| Canal | Especificación | Estado |
|---|---|---|
| `linkedin` | `outputs/linkedin/SPEC.md` | plantilla inicial rellenada |
| `cv` | `outputs/cv/SPEC.md` | plantilla inicial rellenada |

Una especificación de canal no debe contener hechos. Apunta a slugs del wiki y declara restricciones.

## Flujo de ingesta

1. Copia el archivo a `raw/`; no lo edites nunca después.
2. Escribe `wiki/sources/<slug>.md`: qué es, para qué sirve, qué resulta poco fiable, qué páginas alimenta.
3. Actualiza cada página de entidad o concepto que toque. Si contradice una página existente, resuelve la contradicción en la página que *posee* el hecho y anótalo en `log.md`.
4. Añade las páginas nuevas a `index.md`.
5. Añade una entrada a `log.md`.
6. Ejecuta `python scripts/wiki_lint.py wiki/`.

## Disciplina del log

`log.md` es de solo adición, lo más reciente al final. Una entrada por sesión que haya cambiado el wiki. Cada entrada: fecha, tipo (ingest / fix / refactor / lint), 2–6 viñetas y el resultado de la verificación. Nunca reescribas el historial; si algo estuvo mal, dilo en una entrada nueva.

## Cadencia de lint

- Lint estructural tras cada ingesta: `python scripts/wiki_lint.py wiki/` (añade `--strict` en CI).
- Lectura completa en busca de contradicciones cada 5 ingestas.
- Opcional, si la skill `llm-wiki` está instalada: `wiki_stats.py` una vez al mes para la deriva y `wiki_graph_lint.py` antes de reconstruir el grafo.

## Preferencias del usuario

(Vacío. Cuando surja una preferencia de estilo —"di siempre el periodo antes de las responsabilidades", "nunca uses adjetivos de marketing en páginas de hechos"— anótala aquí para que sobreviva a las sesiones.)
