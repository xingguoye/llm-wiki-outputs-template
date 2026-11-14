<!-- translation: es · canonical: METHOD.md · synced: 2026-11-14 -->

# Método: hechos, destinos y el límite entre ellos

Este es el razonamiento detrás de la plantilla. Léelo una vez antes de reestructurar un wiki existente; las reglas operativas viven en [`wiki/SCHEMA.md`](wiki/SCHEMA.md) y [`outputs/SPEC.md`](outputs/SPEC.md).

## 1. Dos formas en que un wiki se pudre

El patrón LLM Wiki te da un lugar donde el conocimiento se acumula. Eso basta cuando el wiki lo lees tú. Se rompe cuando el wiki también alimenta destinos con reglas propias: un CV, un perfil, un portafolio, un pitch.

**Modo de pudrición A — las reglas de canal se filtran en los hechos.** Un campo del perfil tiene un límite duro, así que alguien escribe "≤ 2.000 caracteres" junto a la descripción del proyecto. Seis páginas después el límite aparece en seis sitios, redactado de seis maneras, y una de ellas está desfasada. Cuando la plataforma cambia el límite, ya no sabes cuántos sitios hay que editar, así que no editas ninguno.

**Modo de pudrición B — los entregables se citan como fuentes.** El borrador del perfil cita una cronología, y una ingesta posterior registra el borrador como fuente de esa cronología. El hecho ha perdido su origen: el wiki cita su propia salida y nada se puede reverificar. Peor aún: la *redacción* del borrador empieza a tratarse como evidencia, así que el lenguaje de marketing se endurece hasta convertirse en "hecho".

Los dos modos son el mismo error: **dos tipos distintos de afirmación comparten una capa**. Los hechos son verificables, estables y no pertenecen a nadie en particular. Las reglas de canal son arbitrarias, volátiles y pertenecen a un destino concreto. Mezclarlas vuelve inestables a ambas.

## 2. Tres capas

| Capa | Mutabilidad | Dueño | Pregunta que responde | Si se fusiona con el wiki |
|---|---|---|---|---|
| `raw/` | Inmutable, solo-añadir | Tú (curaduría) | ¿Qué decía la fuente en realidad? | No se puede reverificar; la PII acaba en git |
| `wiki/` | El LLM la reescribe libremente | El LLM | ¿Qué es verdad, dicho una sola vez? | — |
| `outputs/` | Versionada por publicación | Tú + el LLM | ¿Cómo debe renderizarlo el destino X? | Las reglas de plataforma contaminan los hechos; los borradores se vuelven "evidencia" |

`raw/` no forma parte del wiki. Es la evidencia contra la que compruebas, y es la única capa que puede ser desordenada, duplicada o ilegible: un PDF escaneado, un docx, una nota de voz. También es la capa que no debe commitearse.

`wiki/` es el único lugar donde un hecho puede originarse. Una página puede decir "9 años y 6 meses a 2026-11" exactamente una vez; otras tres páginas enlazan a esa. Si dos páginas se contradicen, el wiki está roto y se supone que el ciclo de lint lo detecta — pero la contradicción es barata de arreglar cuando el número existe una sola vez.

`outputs/` contiene tres tipos de archivo, y mantenerlos distintos importa:

- `SPEC.md` — las reglas del destino: orden de campos, límites duros, idioma, qué recortar cuando te pasas, de qué página del wiki sale cada campo, y qué no debe escribirse nunca.
- `state.md` — qué está publicado ahora mismo: versión, fecha, desviaciones conocidas, confirmaciones pendientes.
- `drafts/` — el texto en sí, un directorio por publicación.

## 3. Flujo unidireccional

```
raw/  ──ingesta──▶  wiki/  ──render──▶  outputs/  ──publica──▶  el mundo
        ▲                                  │
        └──────── tú verificas aquí ───────┘
```

Nada vuelve atrás. En concreto, cuatro leyes:

1. **Una sola fuente de verdad por hecho.** Un número, una fecha o un periodo aparece en exactamente una página del wiki. Todas las demás páginas — y todas las especificaciones de canal — enlazan a ella por su slug.
2. **Los destinos son renderizadores, no autores.** Un canal puede citar, comprimir, traducir y reordenar hechos. No puede introducir un hecho que el wiki no tiene. Cuando un borrador necesita un hecho que falta, lo correcto es ingerir y actualizar el wiki primero, y luego volver a renderizar.
3. **Los entregables nunca son fuentes.** Ningún campo `sources:` puede referenciar `outputs/`. Si un borrador contiene información que no existe en ningún otro sitio, esa información se promueve a `wiki/` —con su fuente real— o se descarta.
4. **Primero cambia el hecho.** Edita `wiki/` y luego regenera los borradores. Nunca parchees un borrador dejando el wiki atrás: eso es el modo de pudrición B en un solo paso.

La ley 3 es la que se rompe primero, porque citar un borrador es cómodo. También es la que destruye en silencio el valor del wiki: un wiki cuyas fuentes incluyen sus propias salidas solo puede confirmarse a sí mismo.

## 4. Anatomía de una especificación de canal

Una especificación de canal es un documento pequeño, no una guía de estilo. Siete secciones sostienen el peso:

1. **Audiencia y objetivo** — quién lo lee, qué decisión está tomando.
2. **Estructura** — orden fijo de campos, una fila por campo.
3. **Límites duros** — tabla de límites de la plataforma, con el valor medido la última vez. Los límites son hechos públicos; tu medición es asunto tuyo.
4. **Prioridad de recorte** — cuando te pasas del límite, qué se corta primero, segundo y tercero. Escrito como lista ordenada, porque "sé conciso" no es accionable a las 3 de la mañana.
5. **Mapeo de hechos** — cada campo apunta, por slug, a la página del wiki que renderiza. Esta tabla es la razón por la que la especificación puede ser corta: no contiene hechos.
6. **Convenciones de nombres** — títulos de puesto, etiquetas de sección y sus traducciones, cuando el destino los muestra literalmente.
7. **Prohibido** — afirmaciones que has decidido no hacer nunca en este canal, y por qué. Esta sección es un registro de decisiones; sin ella, la misma mala afirmación se vuelve a proponer cada pocos meses.

Dos cosas que una especificación **no** debe contener: hechos (se desfasan) y métricas personales que no publicarías (se filtran).

## 5. state.md es un registro de versiones, no una lista de tareas

`state.md` responde "qué está vivo ahora mismo", algo que la especificación no puede: la especificación describe cómo *sería* un perfil correcto, mientras que el estado registra que el que está vivo va una versión por detrás y todavía lleva un título de puesto viejo.

Redúcelo a cuatro secciones: versión y fecha actuales; lo que se sabe que está mal o pendiente; una tabla de versiones (versión, fecha, qué cambió); y la siguiente acción. El valor aparece la primera vez que una plataforma reformatea un campo en silencio: puedes saber si la copia viva coincide con el borrador.

## 6. El ciclo

1. **Ingerir** (ocasional): una fuente nueva aterriza en `raw/`, el LLM escribe una página resumen, actualiza las páginas de entidad que toca y añade una entrada a `log.md`.
2. **Corregir** (cuando aparece una contradicción): arregla la única página dueña del hecho; no arregles las copias.
3. **Renderizar** (por publicación): lee la especificación del canal, toma los hechos por slug, produce el borrador, comprueba límites y la lista de prohibidos.
4. **Registrar** (por publicación): actualiza `state.md`, anota desviaciones, deja constancia en el log.
5. **Lint** (periódico): `wiki_lint.py` para la estructura, una lectura completa para contradicciones y deriva.

La propiedad crítica es que los pasos 1 y 2 tocan solo `wiki/`, y el paso 3 solo la lee. Si te descubres editando un borrador para arreglar un hecho, el modelo ha fallado: esa edición pertenece al wiki.

## 7. Opcional: IDs de afirmación

Cuando varios canales citan literalmente las mismas afirmaciones (fechas, periodos, tecnologías), puedes dar a cada una un identificador estable dentro de la página que la posee:

```markdown
- [logro:position-acme-1] 2020-01 → 2024-02 · Híbrido
  Desarrollo y mantenimiento de APIs internas; 12 servicios; .NET Core 3.1 → 6.
```

Después, una especificación o un borrador puede referenciar `logro:position-acme-1` en lugar de repetir el periodo, y un cambio de nombre o una fecha corregida se propaga con un grep.

Es opcional y tiene un coste: cada afirmación necesita un ID, los IDs no pueden reutilizarse y el wiki se vuelve más ruidoso. Compensa cuando (a) la misma afirmación se cita en tres o más destinos, o (b) una afirmación ha sido discutida o corregida al menos una vez. Empieza por la sección que ya te ha quemado, no por todo.

## 8. Cuándo esto es ceremonia

- **Un solo destino.** Si el wiki existe solo para escribir un CV una vez, la capa de especificación es puro sobrecoste. Dos capas bastan: los hechos en el wiki y el borrador del CV citándolos.
- **Sin hechos reutilizables.** Notas de investigación que alimentan un único ensayo no necesitan capa de canal.
- **Hechos que cambian más rápido que el destino.** Si los números se recalculan cada semana desde un sistema vivo, no los congeles en páginas del wiki.

La separación se paga sola cuando los mismos hechos se renderizan en dos o más destinos con restricciones **distintas e impuestas desde fuera** — que es exactamente el caso de CV + perfil + portafolio.

## 9. Migrar un wiki de una sola capa

1. **Congela una copia de seguridad.** Copia el directorio del wiki, anota la fecha.
2. **Clasifica cada línea** de cada página como hecho / regla de canal / texto publicado. Edita en bloque con grep buscando pistas: recuentos de caracteres, "debería escribirse como", nombres de plataforma junto a consejos de maquetación, "borrador", "pega esto".
3. **Crea `outputs/`** y mueve las reglas de canal fuera, un destino cada vez; escribe la especificación a partir de lo que moviste, no de memoria.
4. **Reescribe el esquema** para declarar las tres capas y las cuatro leyes, y añade la tabla de registro de canales.
5. **Borra del wiki las páginas de entrega antiguas**, pásalas a `outputs/state.md` y arregla todos los enlaces entrantes. Pasa el lint: espera huérfanas y enlaces rotos, y resuélvelos enlazando a la página de hechos que sobrevive.

Hazlo de una sentada. Un wiki a medio migrar enseña a todo el mundo la regla equivocada: que el límite es opcional.

## 10. Límites conocidos

- **PII.** `raw/` debe estar en `.gitignore` y el wiki no debe guardar nunca teléfonos, direcciones, números de documento ni fechas de nacimiento. `wiki_lint.py` marca correos, teléfonos y rutas absolutas en páginas y borradores; los nombres y las direcciones siguen siendo un paso de revisión, porque los patrones no los encuentran.
- **Duplicación de idiomas.** Los perfiles multilingües duplican texto en `outputs/`, no en `wiki/`. Mantén los hechos neutrales al idioma (fechas, periodos, nombres propios) para que solo se multiplique la redacción. Este repositorio aplica la misma regla a su propia documentación: un archivo canónico por documento más las versiones `.zh.md`/`.es.md`, que declaran de qué se tradujeron y cuándo. Los registros, los índices generados y los fragmentos para copiar están exentos: traducirlos garantiza la deriva, y la lista de exenciones vive en `scripts/check_translations.py`.
- **Las traducciones se desincronizan.** Cada versión lleva `<!-- translation: es · canonical: <ruta> · synced: <fecha> -->`; `scripts/check_translations.py` falla si falta una o está mal etiquetada, y avisa si su fecha es anterior a la del archivo canónico. No puede saber si el *contenido* sigue coincidiendo: solo que nadie lo ha releído desde entonces. Resincroniza tras cada edición o la copia española se convertirá en la mentira más antigua del repositorio.
- **El CI solo protege cuatro cosas.** [`.github/workflows/lint.yml`](.github/workflows/lint.yml) falla si hay errores de lint estructural, si un campo `sources:` referencia `outputs/` (ley 3), si hay algún archivo versionado dentro de `raw/` y si falta una traducción o está desfasada. Todo lo demás —contradicciones, deriva, un hecho que cambió sin avisar— sigue siendo una lectura completa.
- **El lint comprueba estructura, no verdad.** Encuentra enlaces rotos y huérfanas. La detección de contradicciones sigue siendo tuya.
