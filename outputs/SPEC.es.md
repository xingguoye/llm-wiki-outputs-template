<!-- translation: es · canonical: outputs/SPEC.md · synced: 2026-11-14 -->

# Salidas: el contrato de un canal

`outputs/` contiene todo lo relativo a los *destinos*: cómo debe escribirse un canal, qué está publicado ahora mismo y el texto en sí. No contiene hechos. Los hechos viven en `wiki/` y se traen por slug.

Este archivo es el contrato. Cualquier `outputs/<channel>/SPEC.md` debe cumplirlo.

## Forma del directorio

```
outputs/<channel>/
  SPEC.md      las reglas (las secciones exigidas por este contrato, rellenadas)
  state.md     lo que está en vivo ahora + tabla de versiones
  drafts/      un subdirectorio por publicación: drafts/2026-11/
```

`_template/` es el esqueleto que se copia para un canal nuevo. No lo edites in situ.

## Secciones obligatorias de una especificación de canal

| # | Sección | Debe responder |
|---|---|---|
| 1 | Audiencia y objetivo | Quién lo lee y qué decisión toma |
| 2 | Estructura | Orden fijo de campos, una fila por campo |
| 3 | Límites duros | Tabla: campo, límite de la plataforma, último valor medido |
| 4 | Prioridad de recorte | Lista ordenada: qué cortar primero, segundo y tercero al pasarse |
| 5 | Mapeo de hechos | Campo → slug del wiki. Esta tabla es la razón de que la especificación no contenga hechos |
| 6 | Nomenclatura | Títulos, etiquetas y traducciones que el canal muestra tal cual |
| 7 | Prohibiciones | Afirmaciones que nunca harás aquí, cada una con su razón en una línea |
| 8 | Lista de aceptación | Elementos comprobables que se recorren antes de publicar |
| 9 | Procedimiento de publicación | Cómo un borrador pasa a estar en vivo y qué queda registrado |

Una especificación sin las secciones 3, 4, 5 y 7 es una guía de estilo, no una especificación.

## Qué no puede contener una SPEC

- **Hechos.** Nada de fechas, periodos, recuentos ni nombres. Se quedan obsoletos; el slug no.
- **Mediciones personales que no publicarías.** "El límite del titular es 220" es público. "La última vez llegué a 75 caracteres" no lo es: anótalo en `state.md`.
- **Texto de borrador.** El texto pertenece a `drafts/`; una especificación que cita un párrafo acabará divergiendo de la versión en vivo.

## Forma de state.md

```
## Current
- versión, fecha, dónde está en vivo, quién lo confirmó

## Known deviations
- qué está mal ahora mismo y si se va a corregir

## Versions
| versión | fecha | cambio |

## Next action
- la única siguiente cosa que hay que hacer
```

## Procedimiento de publicación

1. Lee `outputs/<channel>/SPEC.md` y las páginas del wiki de su mapeo de hechos.
2. Renderiza el borrador en `outputs/<channel>/drafts/<YYYY-MM>/`.
3. Comprueba los límites de forma mecánica (los recuentos de caracteres se *miden*, no se estiman).
4. Recorre la lista de aceptación; corrige el borrador, no la especificación.
5. Si un hecho estaba mal, detente: corrige `wiki/` primero (ley 4) y vuelve a renderizar.
6. Actualiza `state.md` (versión, fecha, desviaciones) y añade una entrada a `wiki/log.md`.

## Coherencia entre canales

Cuando un mismo hecho se renderiza en varios canales:

- El hecho viene de una sola página del wiki; si dos canales discrepan, el canal con el borrador más antiguo es el equivocado por defecto.
- Cambiar un hecho obliga a re-renderizar **todos** los canales que lo citan. Si son más de dos, enumera los canales afectados en la nota "rendered by" de la página del wiki.
- Las variantes de idioma son borradores distintos de la misma especificación, no especificaciones distintas.
