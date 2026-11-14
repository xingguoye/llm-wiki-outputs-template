<!-- translation: es · canonical: outputs/linkedin/SPEC.md · synced: 2026-11-14 -->

# SPEC: perfil de LinkedIn

Reglas solo para el destino LinkedIn. Aquí no hay hechos: cada hecho llega desde `wiki/` a través del mapeo de la §5.

## 1. Audiencia y objetivo

- Lector: reclutadores (a menudo no técnicos, escaneando palabras clave) y responsables de contratación (que leen el orden de la experiencia).
- Decisión en 10 segundos: preselección o descarte, según el titular + las dos primeras líneas del extracto + el puesto actual.
- Optimiza para: legibilidad por palabras clave, una cronología sin ambigüedad y ninguna afirmación inflada que se caiga en la entrevista.

## 2. Estructura

Orden fijo. El mismo orden en cada variante de idioma.

| # | Campo | Qué va dentro |
|---|---|---|
| 1 | Titular | Puesto + stack + un diferenciador. Sin adjetivos que no puedas defender. |
| 2 | Extracto | 3–4 párrafos: posicionamiento → años y stack → clientes/proyectos → idiomas |
| 3 | Experiencia | Una entrada por página de puesto; el campo de organización = empleador legal |
| 4 | Proyectos | Proyectos personales o destacables, una entrada cada uno |
| 5 | Formación | Título(s) y ubicación del campus |
| 6 | Idiomas | Autoevaluación, mapeada al desplegable de la plataforma en la §6 |
| 7 | Aptitudes | La lista completa de habilidades del wiki, ordenada según la §3 |
| 8 | Certificaciones | Certificación, entidad emisora, fecha |

La regla que evita casi toda la confusión: **la "Organización" de Experiencia es el empleador legal, nunca el cliente final.** Los clientes y proyectos van en la descripción o en una entrada de proyecto anidada. Poner el cliente en el campo de organización crea un historial laboral falso.

## 3. Límites duros

| Campo | Límite de la plataforma | Último medido |
|---|---|---|
| Titular | 220 caracteres | <measure> |
| Extracto | 2.600 caracteres | <measure> |
| Descripción de experiencia | 2.000 caracteres | <measure> |
| Descripción de proyecto (cada uno) | 2.000 caracteres | <measure> |
| Aptitudes | 50 elementos | <measure> |
| URL personalizada | – | – |

Los valores medidos pertenecen a `state.md`, no a este archivo: el límite es público, tu texto no.

**Orden de las aptitudes.** Las tres primeras son las que más se muestran; elígelas según el puesto objetivo, no según la longitud de la lista. El resto, en el orden canónico del wiki, para que volver a pegar sea determinista.

**Prioridad de recorte** cuando una descripción pasa de 2.000 caracteres:

1. Elimina el detalle de configuración herramienta por herramienta (cadenas de razonamiento, ajustes, inventarios de hardware).
2. Comprime la lista de hardware e infraestructura en una sola cláusula.
3. Acorta la narrativa de metodología: último recurso, es la que más señal aporta.

## 4. Versiones de idioma

- Un idioma principal, acorde con el lugar donde buscas trabajo.
- Las versiones secundarias son **variantes de esta especificación**, no especificaciones distintas: misma estructura, mismos hechos, solo cambia la redacción.
- Regla entre idiomas: cualquier frase que declare seniority, años o alcance debe leerse igual en todas las variantes. Mantén en `state.md` un "ancla de sincronización" de una línea —la frase que debe coincidir— porque las traducciones se desvían primero ahí.

## 5. Mapeo de hechos

| Campo | Se toma de |
|---|---|
| Titular, extracto (años, posicionamiento) | `wiki/entities/person-*` |
| Cronología de la experiencia, modalidad | `wiki/entities/employer-*` (posee los periodos) + `wiki/entities/position-*` |
| Responsabilidades, atribución de clientes | `wiki/entities/position-*`, `wiki/entities/client-*` |
| Aptitudes y exclusiones | `wiki/concepts/skill-*` |
| Proyectos | `wiki/entities/project-*` |
| Formación, campus | `wiki/entities/education-*` |
| Idiomas, certificaciones | `wiki/entities/person-*` |
| Resoluciones sobre qué no afirmar | `wiki/synthesis/decisions-*` |

## 6. Nomenclatura

- Puestos: usa el título que usó el empleador, en el idioma del perfil, con la forma inglesa cuando el título original no esté en inglés. Mantén una tabla de dos columnas por puesto en la página del puesto en lugar de traducir sobre la marcha.
- Mapeo del desplegable de idiomas: autoevaluación → opción de la plataforma. Fija el mapeo una vez aquí (p. ej. "professional working proficiency" para un idioma de trabajo, "native or bilingual" solo para la lengua materna) para que no se vuelva a discutir en cada publicación.

## 7. Prohibiciones

| Nunca escribas | Porque |
|---|---|
| Palabras de seniority que el historial no respalda ("senior", "lead", "expert") | Los entrevistadores las comprueban primero; el desajuste es peor que la palabra ausente |
| Clientes como empleadores | Falsifica la cronología; se ve con un clic |
| Tecnologías de nivel curso presentadas como experiencia profesional | No verificable y se expone rápido |
| Fechas solapadas que impliquen empleadores en paralelo | "Consecutivos, no simultáneos" es una afirmación que merece decirse en la descripción |
| Métricas que no puedes documentar | Cualquier número del perfil se te puede preguntar en la entrevista |

## 8. Lista de aceptación

- [ ] Titular ≤ 220, extracto ≤ 2.600, cada descripción ≤ 2.000, medido
- [ ] El campo de organización = empleador legal en cada entrada
- [ ] Las fechas de cada entrada coinciden exactamente con `wiki/entities/employer-*`
- [ ] El total de años del extracto coincide con la página de la persona (una sola fuente de verdad)
- [ ] Aptitudes ≤ 50 e idénticas a la lista del wiki
- [ ] Lista de prohibiciones recorrida punto por punto
- [ ] Variantes de idioma: las frases de seniority y años son idénticas

## 9. Procedimiento de publicación

1. Redacta en `outputs/linkedin/drafts/<YYYY-MM>/`: un archivo por idioma, más un archivo de bloques listo para pegar.
2. Mide las longitudes con un script; corrige el borrador, nunca el wiki (si un hecho está mal, aplica la ley 4).
3. Pega y vuelve a leer la página en vivo contra el borrador (las plataformas recomponen el texto).
4. Actualiza `state.md` (versión, fecha, valores medidos, desviaciones) y `wiki/log.md`.
