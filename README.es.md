<!-- translation: es · canonical: README.md · synced: 2026-11-14 -->

# LLM Wiki + Outputs

Una plantilla para una base de conocimiento personal que alimenta **varios destinos** — un CV, un perfil de LinkedIn, una página de portafolio, respuestas de entrevista — desde **un solo** cuerpo de hechos.

Es el patrón "LLM Wiki" (fuentes inmutables → wiki en markdown mantenida por el LLM → ciclo de consulta y lint) con una incorporación estructural: una **capa de salidas** separada que contiene las reglas de cada destino, para que esas reglas nunca contaminen los hechos.

- [English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [Método](METHOD.es.md) · [Method (EN)](METHOD.md) · [方法论 (ZH)](METHOD.zh.md)

## El problema que resuelve

Un wiki que además guarda el texto de tu CV se pudre en dos direcciones:

1. **Las reglas de cada canal se filtran en los hechos.** "Titular ≤ 220 caracteres" acaba copiado en seis páginas de entidad. La plataforma cambia el límite y tú editas nueve archivos.
2. **Los entregables se citan como fuentes.** El borrador de LinkedIn pasa a ser la "fuente" de las fechas que cita. El hecho se queda sin origen y el wiki se cita a sí mismo.

La solución no es más disciplina. Es un límite: los hechos viven en `wiki/`, las reglas de destino viven en `outputs/<canal>/SPEC.md`, y el flujo va en un solo sentido.

## Inicio rápido

```bash
# 1. Usa esta plantilla (o: git clone <este repo> mi-wiki && cd mi-wiki)
# 2. Mete tus fuentes en raw/            — PDFs, docx, transcripciones, borradores viejos
# 3. Apunta tu agente al esquema:
#      "Lee wiki/SCHEMA.md y luego ingiere raw/<tu-archivo>"
# 4. Escribe las reglas del destino:
#      "Rellena outputs/linkedin/SPEC.md para mi caso"
# 5. Comprueba la estructura:
python scripts/wiki_lint.py wiki/
```

Funciona con cualquier agente que pueda leer archivos y ejecutar una shell (Claude Code, Codex, Cursor, DSH, un chat con acceso a archivos). `wiki/SCHEMA.md` es el contrato de entrada: toda convención que el agente necesita está ahí o a un enlace de distancia.

## Estructura

```
AGENTS.md             reglas de operación + guías para el agente (léelo primero)
raw/                  fuentes inmutables. Nunca se editan, nunca se commitean (PII).
wiki/                 hechos. El LLM es dueño de esta capa.
  SCHEMA.md           convenciones: tipos de página, frontmatter, etiquetas, leyes
  index.md            índice plano de todas las páginas
  log.md              historial solo-añadir de ingestas, correcciones, refactors
  entities/           personas, empleadores, puestos, clientes, proyectos
  concepts/           habilidades, stacks, métodos
  sources/            una página resumen por fuente ingerida
  synthesis/          páginas transversales: registros de decisiones, comparaciones
  graph/              grafo compilado opcional (ontology.yaml sí se versiona)
outputs/              capa de destino. Especificaciones, estado, borradores.
  SPEC.md             qué debe contener una especificación de canal válida
  _template/          cópiala por cada canal nuevo
  linkedin/           SPEC.md + state.md
  cv/                 SPEC.md + state.md
docs/                 ejemplo resuelto (ficticio) — se lee in situ, fuera del lint
scripts/              wiki_lint.py + build_index.py + check_translations.py — solo biblioteca estándar, sin instalación
```

¿Quieres ver las convenciones en uso antes de escribir nada? Lee [`docs/career/`](docs/career/README.md) in situ: cinco páginas ficticias, en orden de lectura. Están deliberadamente fuera de `wiki/` para que no afecten al lint ni a la búsqueda.

La documentación viene en tres idiomas allí donde una persona realmente lo necesita: `README.md`, `METHOD.md`, `AGENTS.md`, `CREDITS.md`, `wiki/SCHEMA.md`, `wiki/graph/README.md`, cada `SPEC.md` y todo el ejemplo de `docs/career/` tienen junto a ellos sus versiones `.zh.md` (chino) y `.es.md` (español), y el archivo sin sufijo es el canónico. Cada traducción abre con una línea de procedencia —`<!-- translation: es · canonical: wiki/SCHEMA.md · synced: 2026-11-14 -->`— y `python scripts/check_translations.py` falla cuando falta una traducción, está mal etiquetada o es más antigua que el archivo que traduce.

Ocho archivos se quedan en un solo idioma a propósito, y la lista de exenciones la lleva el script: `wiki/index.md` (un índice que se reescribe en cada ingesta), `wiki/log.md` (historial de solo adición; cada entrada conserva su idioma), los registros `state.md` (cambian en cada publicación), `wiki/.page-template.md` (un fragmento), `CLAUDE.md` (un puntero de tres líneas) y `raw/README.md` (se lee una vez, antes de que exista nada). Traducir un registro no aporta nada y garantiza la deriva. Las traducciones son para las personas; si una discrepa de su canónico, gana el canónico.

## Qué va dónde

| Pregunta | Capa | Ejemplo |
|---|---|---|
| ¿Qué pasó? | `raw/` | `raw/cv-2026.docx`, la transcripción de una llamada |
| ¿Qué es verdad, dicho una sola vez? | `wiki/entities/*` | "Empleador: Acme, 2020-01 → 2024-02, híbrido" |
| ¿Cómo debe renderizarlo este destino? | `outputs/*/SPEC.md` | "Titular ≤ 220; bloque de proyectos ≤ 2.000" |
| ¿Qué publiqué realmente? | `outputs/*/state.md` + `drafts/` | "v1 publicado el 2026-11-10; pendiente: foto" |

## Comandos

```bash
python scripts/wiki_lint.py wiki/            # enlaces, huérfanas, frontmatter, fugas de capa, claim IDs, forma de state, PII
python scripts/wiki_lint.py wiki/ --json     # igual, legible por máquina (lo usa el CI)
python scripts/wiki_lint.py wiki/ --strict   # los avisos también fallan; úsalo en CI
python scripts/wiki_lint.py wiki/ --no-pii   # omite el escaneo de PII (lo demás son nombres, no patrones)
python scripts/wiki_lint.py --self-test      # comprueba el comprobador contra nueve casos malos conocidos
python scripts/build_index.py wiki/          # regenera wiki/index.md desde las páginas (--check solo verifica)
python scripts/check_translations.py         # traducciones completas y al día
git ls-files raw/                            # debe estar vacío salvo raw/README.md
```

Sin dependencias, sin instalación. Python 3.9+. Devuelve 1 cuando hay errores, así que entra directo en CI — ver [.github/workflows/lint.yml](.github/workflows/lint.yml), que además hace cumplir la privacidad de `raw/` y la ley 3.

Más allá de la estructura, las comprobaciones que siguen necesitando a una persona son las del significado: dos páginas afirmando la misma fecha de forma distinta, una afirmación cuya fuente desapareció, un hecho que cambió mientras un borrador conservaba el valor viejo. El script ya cubre la mitad mecánica —IDs de claim duplicados, un borrador que cita un claim no definido, un `state.md` al que le falta una sección del contrato, patrones de PII— y ahí se detiene. El significado es trabajo del LLM.

Opcional, si quieres búsqueda semántica o la capa de grafo: viven en la skill de agente `llm-wiki`, de la que esta plantilla toma sus convenciones (`wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py`). Instálala y apunta sus scripts a tu `wiki/`. La plantilla funciona sin ellas: el markdown es la fuente canónica.

## Las cuatro leyes

1. **Una sola fuente de verdad por hecho.** Un número, una fecha o un periodo aparece en exactamente una página del wiki; todas las demás enlazan a ella.
2. **Los destinos son renderizadores, no autores.** `outputs/` puede citar hechos, nunca introducirlos.
3. **Los entregables nunca son fuentes.** Ninguna página puede citar `outputs/` en su campo `sources:`.
4. **Primero cambia el hecho.** Edita `wiki/` y luego regenera los borradores. Nunca parchees un borrador dejando el wiki atrás.

Razonamiento completo, taxonomía de fallos y pasos de migración: [METHOD.es.md](METHOD.es.md).

## Antes de publicar tu propia copia

- [ ] `raw/` contiene solo lo que tienes derecho a publicar; está en `.gitignore` por defecto — déjalo así.
- [ ] Ningún nombre real de empleador, cliente o colega fuera de `raw/`, salvo que quieras que sea público.
- [ ] Sin teléfonos, direcciones, fechas de nacimiento, números de documento ni enlaces a perfiles privados.
- [ ] `outputs/**/drafts/` revisado: los borradores filtran PII más a menudo que las páginas del wiki.
- [ ] `outputs/*/SPEC.md` generalizado: los límites de plataforma son públicos, tus métricas personales ("75 caracteres medidos") no.
- [ ] `wiki_lint.py` limpio: marca correos, teléfonos y rutas absolutas en páginas y borradores.
- [ ] Después ejecuta `grep -ri "<tu apellido>" . --exclude-dir=.git` y lo mismo con cada empleador y cliente: los nombres y las direcciones no se detectan por patrón.

## Créditos

El patrón del wiki sigue el gist "LLM Wiki" de Andrej Karpathy (abril de 2026). Las convenciones de `SCHEMA.md` y el vocabulario de páginas y grafo están adaptados de la skill `llm-wiki`, que se basa en ese gist; la skill es dueña de `wiki_search.py`, `wiki_stats.py` y las herramientas `wiki_graph_*`, que este repositorio no redistribuye. La separación en tres capas, el contrato de especificación de canal, `scripts/wiki_lint.py` y `METHOD.md` son originales de esta plantilla. Detalles en [CREDITS.md](CREDITS.md).

## Licencia

MIT — ver [LICENSE](LICENSE).
