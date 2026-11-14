<!-- translation: es · canonical: outputs/cv/SPEC.md · synced: 2026-11-14 -->

# SPEC: CV / currículum

Reglas para el destino CV. Aquí no hay hechos: llegan desde `wiki/` a través de la §5.

## 1. Audiencia y objetivo

- Lector: primero el ATS (parseo de palabras clave y estructura), después una persona que lo ojea 30–60 segundos.
- Decisión: si este candidato encaja lo bastante con el puesto publicado como para llamarle.
- Optimiza para: parseabilidad automática, orden adaptado al puesto y densidad de una página por década.

## 2. Estructura

| # | Bloque | Contenido |
|---|---|---|
| 1 | Cabecera | Nombre, ciudad, un canal de contacto, URL del perfil |
| 2 | Resumen | 3–4 líneas: puesto, años, stack, dominio |
| 3 | Experiencia | Orden cronológico inverso; un bloque por puesto, con el empleador nombrado y el cliente mencionado en línea |
| 4 | Formación | Título, institución, campus, años |
| 5 | Aptitudes | Agrupadas por categoría, no en plano |
| 6 | Idiomas | Idioma + nivel |
| 7 | Certificaciones | Nombre, emisor, fecha |

Un CV se adapta a cada candidatura **reordenando y reponderando**, no inventando un resumen nuevo cada vez. Conserva las variantes por puesto en `drafts/` para poder compararlas.

## 3. Límites duros

| Restricción | Valor | Último medido |
|---|---|---|
| Longitud | 1–2 páginas (2 si tienes 8+ años) | <measure> |
| Formato enviado | PDF con texto seleccionable | – |
| ATS | sin cuadros de texto, sin cuerpo a varias columnas, sin tablas como maquetación principal, sin iconos que aporten significado | – |
| Tipografía | una sola familia, cuerpo ≥10 pt | – |
| Foto | <decidir por mercado; dejar la decisión escrita aquí, una vez> | – |
| Nombre del archivo | `<name>-<role>-<year>.pdf` | – |

**Prioridad de recorte** al pasarse de páginas:

1. Los puestos más antiguos → comprimir a una línea cada uno, conservando empleador, título y fechas.
2. Lista de aptitudes → quitar las categorías que el puesto objetivo no menciona.
3. Detalle de formación → solo título + institución.
4. Nunca comprimas el puesto actual: de él vive la entrevista.

## 4. Versiones de idioma

Un CV por idioma, misma estructura y mismos hechos. La frase de seniority del resumen debe coincidir con la del perfil, literalmente cuando sea posible: la incoherencia entre CV y perfil es la que más nota un reclutador.

## 5. Mapeo de hechos

| Bloque | Se toma de |
|---|---|
| Resumen | `wiki/entities/person-*` |
| Periodos de experiencia, modalidad | `wiki/entities/employer-*` |
| Responsabilidades, clientes | `wiki/entities/position-*`, `wiki/entities/client-*` |
| Aptitudes | `wiki/concepts/skill-*` |
| Formación | `wiki/entities/education-*` |
| Certificaciones, idiomas | `wiki/entities/person-*` |

## 6. Registro de desviaciones (estructural)

Algunos CV se desvían de la *fuente* a propósito: un borrador antiguo dice una cosa y la cronología confirmada dice otra. Anota esas desviaciones aquí con su resolución, para que no se vuelvan a discutir:

| Desviación | Resolución |
|---|---|
| <el borrador antiguo dice X, el registro confirmado dice Y> | <gana el wiki; no "arregles" el archivo antiguo> |

No edites `raw/` para que coincida. El archivo antiguo es la evidencia de lo que se envió en su momento.

## 7. Prohibiciones

| Nunca escribas | Porque |
|---|---|
| Palabras de seniority que el historial no respalda | Se comprueban en la entrevista |
| Aptitudes que solo aparecen en cursos, sin etiquetar | Habitual y fácil de detectar |
| Nombres de clientes presentados como empleadores | Falsifica el historial laboral |
| Porcentajes o "mejoré X un Y %" sin fuente | No verificable y hoy se espera que lo expliques |
| Una segunda columna de habilidades blandas | Ruido para el ATS; si acaso, van en el resumen |

## 8. Lista de aceptación

- [ ] Número de páginas dentro del límite, comprobado en el PDF exportado
- [ ] Texto seleccionable en el PDF; nada atrapado en una imagen
- [ ] Fechas, títulos y empleadores idénticos al wiki
- [ ] La redacción del seniority en el resumen coincide con la variante del perfil
- [ ] Cada viñeta empieza por un verbo; ninguna frase empieza por "Responsible for"
- [ ] Aptitudes agrupadas, sin duplicados y no más largas que la lista del perfil
- [ ] Archivo exportado con el nombre de la §3

## 9. Procedimiento de publicación

1. Copia el último borrador y adáptalo al puesto (reordena, repondera).
2. Exporta el PDF; verifica el número de páginas y que el texto se pueda seleccionar.
3. Recorre la lista; corrige el borrador.
4. Registra en `state.md`: qué variante se envió a dónde y cuándo. Un CV que no se envió a ningún sitio no es una publicación.
