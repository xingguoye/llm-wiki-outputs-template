<!-- translation: es · canonical: README.md · synced: 2026-11-14 -->
# LLM Wiki + Outputs

Una plantilla para una base de conocimiento personal que alimenta **varios destinos** — un CV, un perfil de LinkedIn, una página de portafolio, respuestas de entrevista — desde **un solo** cuerpo de hechos.

Es el patrón "LLM Wiki" (fuentes inmutables → wiki en markdown mantenida por el LLM → bucle de lint y consulta) con una diferencia estructural: una **capa de salidas** aparte que guarda las reglas de cada destino, para que esas reglas nunca se filtren a los hechos.

La wiki la escribe y la mantiene un agente. Mete un CV nuevo, la transcripción de una llamada o una oferta en `raw/`, pídele que lo ingeste y editará solo las páginas que ese hecho nuevo toca: tú revisas el diff, él teclea.

- [English](README.md) · [中文](README.zh.md) · [Español](README.es.md) · [Método](METHOD.md)

[![lint](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml/badge.svg)](https://github.com/xingguoye/llm-wiki-outputs-template/actions/workflows/lint.yml)

## El problema que resuelve

Una wiki que además guarda el texto de tu CV se pudre en dos direcciones:

1. **Las reglas del canal se filtran a los hechos.** "Headline ≤ 220 caracteres" acaba copiado en seis páginas de entidad. La plataforma cambia el límite y tú editas nueve archivos.
2. **Los entregables se citan como fuentes.** El borrador de LinkedIn pasa a ser la "fuente" de las fechas que cita. El hecho se queda sin origen y la wiki se cita a sí misma.

La solución no es más disciplina, sino un límite: los hechos viven en `wiki/`, las reglas de cada destino viven en `outputs/<canal>/SPEC.md`, y el flujo va en un solo sentido.

## Inicio rápido

```bash
# 1. Usa esta plantilla, o: git clone https://github.com/xingguoye/llm-wiki-outputs-template my-wiki && cd my-wiki
# 2. Mete tus fuentes en raw/            — PDF, docx, transcripciones, borradores viejos
# 3. Señala el esquema al agente:
#      "Read wiki/SCHEMA.md, then ingest raw/<your-file>"
# 4. Escribe las reglas del destino:
#      "Fill outputs/linkedin/SPEC.md for my case"
# 5. Comprueba la estructura:
python scripts/wiki_lint.py wiki/
```

Funciona con cualquier agente que pueda leer archivos y ejecutar una shell (Claude Code, Codex, Cursor, DSH, un chat normal con acceso a archivos). `wiki/SCHEMA.md` es el contrato de entrada: cada convención que el agente necesita está ahí o a un enlace de distancia.

## Estructura

```
AGENTS.md             reglas de operación + playbooks para el agente (lee esto primero)
raw/                  fuentes inmutables. Nunca se editan, nunca se commitean (PII).
wiki/                 hechos. Esta capa la posee el LLM.
  SCHEMA.md           convenciones: tipos de página, frontmatter, tags, leyes
  index.md            índice plano de todas las páginas
  log.md              historial de solo añadir: ingestas, arreglos, refactorizaciones
  entities/           personas, empleadores, puestos, clientes, proyectos
  concepts/           habilidades, stacks, métodos
  sources/            una página de resumen por fuente ingerida
  synthesis/          páginas transversales: registros de decisiones, comparaciones
  graph/              grafo compilado opcional (ontology.yaml sí se versiona)
outputs/              capa de salidas. Especificaciones, registro de estado, borradores.
  SPEC.md             qué debe contener una especificación de canal válida
  _template/          cópiala por cada canal nuevo
  linkedin/           SPEC.md + state.md
  cv/                 SPEC.md + state.md
docs/                 ejemplo completo (ficticio) — se lee en su sitio, fuera del lint
scripts/              wiki_lint.py + build_index.py + check_translations.py — solo librería estándar, sin instalar nada
.translations         lista opcional: qué documentos van también en otro idioma (hoy: este README)
```

**La documentación está en inglés, y las traducciones son opcionales; este README es el ejemplo vivo.** Sus dos traducciones hermanas (`README.zh.md`, `README.es.md`) están declaradas en `.translations`, una por línea, y cada una empieza con una línea de procedencia:

```
<!-- translation: es · canonical: README.md · synced: 2026-11-14 -->
```

El archivo sin sufijo es el canónico y gana cuando los dos discrepan; `python scripts/check_translations.py` falla si falta una traducción, está mal etiquetada o es más vieja que el archivo que traduce. El resto del repositorio se queda en inglés hasta que haya un lector que de verdad necesite otra cosa: traducir es una promesa de releer, y una traducción que nadie relee es la mentira más vieja de un repositorio.

¿Quieres ver las convenciones en uso antes de escribir nada? Lee [`docs/career/`](docs/career/README.md) en su sitio: siete páginas ficticias, en orden de lectura. Están deliberadamente fuera de `wiki/` para no afectar al lint ni a la búsqueda.

**Este repositorio no incluye ninguna instancia real, y no se debe añadir una.** `docs/career/` es inventado: la persona, el empleador, los clientes y las fechas son ficticios. Una wiki en uso es dato privado — un nombre, un empleador, unos clientes y cuatro fechas bastan para identificar a una persona — así que una instancia terminada se queda donde se escribió y nunca se copia a este repositorio ni se publica con la misma licencia. El escaneo de PII detecta correos, teléfonos y rutas absolutas; no reconoce un nombre ni una empresa, así que ese juicio sigue siendo manual.

## Qué va dónde

| Pregunta | Capa | Ejemplo |
|---|---|---|
| ¿Qué pasó? | `raw/` | `raw/cv-2026.docx`, la transcripción de una llamada |
| ¿Qué es verdad, dicho una sola vez? | `wiki/entities/*` | "Empleador: Acme, 2020-01 → 2024-02, híbrido" |
| ¿Cómo debe presentarlo este destino? | `outputs/*/SPEC.md` | "Headline ≤ 220; bloque Projects ≤ 2.000" |
| ¿Qué publiqué de verdad? | `outputs/*/state.md` + `drafts/` | "v1 publicada el 2026-11-10; pendiente: foto" |

## Comandos

```bash
python scripts/wiki_lint.py wiki/            # comprueba: wiki/SCHEMA.md § Lint cadence
python scripts/wiki_lint.py wiki/ --json     # igual, legible por máquina (lo usa CI)
python scripts/wiki_lint.py wiki/ --strict   # los avisos también fallan; úsalo en CI
python scripts/wiki_lint.py wiki/ --no-pii   # salta el escaneo de PII (los nombres no son patrones)
python scripts/wiki_lint.py --self-test      # pasa el comprobador por sus propios casos malos
python scripts/build_index.py wiki/          # reescribe wiki/index.md desde las páginas (--check para verificar)
python scripts/check_translations.py         # cobertura y frescura de las traducciones que declaraste
git ls-files raw/                            # debe estar vacío salvo raw/README.md
```

Sin dependencias, sin instalación. Python 3.9+. Devuelve 1 si hay errores, así que entra directo en CI: mira [.github/workflows/lint.yml](.github/workflows/lint.yml), que además hace cumplir la regla de privacidad de `raw/` y la ley 3.

Más allá de la estructura, las comprobaciones que aún necesitan a una persona son las que van de significado: dos páginas que afirman la misma fecha de forma distinta, un claim cuya fuente desapareció, un hecho que cambió mientras el borrador conservaba el valor viejo. El script cubre la mitad mecánica —la lista exacta está en `wiki/SCHEMA.md` § Lint cadence— y se detiene ahí. El significado es trabajo del LLM.

Opcional: si quieres búsqueda semántica o la capa de grafo, viven en la skill de agente `llm-wiki`, de la que esta plantilla toma sus convenciones (`wiki_search.py`, `wiki_stats.py`, `wiki_graph_*.py`). Instálala y apunta los scripts a tu `wiki/`. La plantilla funciona sin ellos: el markdown es lo canónico.

## Las cuatro leyes

1. **Un solo origen por hecho.** Un número, una fecha, un tramo aparecen en exactamente una página de la wiki; el resto de páginas enlazan a ella.
2. **Los destinos presentan, no crean.** `outputs/` puede citar hechos, nunca introducirlos.
3. **Los entregables nunca son fuentes.** Ninguna página puede citar `outputs/` en su campo `sources:`.
4. **Primero cambia el hecho.** Edita `wiki/` y luego regenera los borradores. Nunca parchees un borrador y dejes la wiki atrás.

Razonamiento completo, taxonomía de fallos y pasos de migración: [METHOD.md](METHOD.md).

## Antes de publicar tu propia copia

- [ ] `raw/` solo contiene lo que tienes derecho a publicar; está en gitignore por defecto — déjalo así.
- [ ] Ningún nombre real de empleador, cliente o colega fuera de `raw/`, salvo que quieras que sea público.
- [ ] Ni teléfonos, ni direcciones, ni fechas de nacimiento, ni números de documento, ni enlaces a perfiles privados.
- [ ] `outputs/**/drafts/` revisado: los borradores filtran PII con más frecuencia que las páginas de la wiki.
- [ ] `outputs/*/SPEC.md` generalizado: los límites de plataforma son públicos, tus cifras personales ("75 caracteres medidos") no.
- [ ] `wiki_lint.py` limpio: marca correos, teléfonos y rutas absolutas de inicio en páginas y borradores.
- [ ] Después `grep -ri "<tu apellido>" . --exclude-dir=.git` y lo mismo con cada empresa y cliente: los nombres y las direcciones no se detectan con patrones.

## Créditos

El patrón wiki sigue el gist "LLM Wiki" de Andrej Karpathy (abril de 2026). Las convenciones de `SCHEMA.md` y el vocabulario de páginas y grafo se adaptan de la skill de agente `llm-wiki`, que construye sobre ese gist: la skill es dueña de `wiki_search.py`, `wiki_stats.py` y las herramientas `wiki_graph_*`, que este repositorio no redistribuye. La separación en tres capas de hechos y salidas, el contrato de especificación de canal, `scripts/wiki_lint.py` y `METHOD.md` son originales de esta plantilla. Detalles en [CREDITS.md](CREDITS.md).

## Licencia

MIT — ver [LICENSE](LICENSE).
