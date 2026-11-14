<!-- translation: es · canonical: outputs/_template/SPEC.md · synced: 2026-11-14 -->

# SPEC: <channel name>

> Copia este directorio a `outputs/<channel>/` y rellena cada `<corchete angular>`. Borra las secciones que puedas justificar borrar, pero el contrato de `outputs/SPEC.md` explica por qué las secciones 3, 4, 5 y 7 son imprescindibles.

Este archivo es la única fuente de reglas de este canal. No contiene hechos: los hechos vienen de `wiki/`, por slug. Cuando este archivo y el wiki discrepen sobre un *hecho*, gana el wiki; cuando discrepen sobre una *restricción*, gana este archivo.

## 1. Audiencia y objetivo

- Lector: <quién lo abre: reclutador, responsable de contratación, colega, tribunal>
- Decisión que toma en los primeros 10 segundos: <preselección / descarte / agendar una llamada>
- Para qué optimiza este canal: <legibilidad / coincidencia de palabras clave / profundidad / brevedad>

## 2. Estructura

Orden fijo. No lo reordenes para una candidatura concreta.

| # | Campo | Qué va dentro |
|---|---|---|
| 1 | <field> | <una línea: qué corresponde, qué no> |
| 2 | <field> | |

## 3. Límites duros

| Campo | Límite de la plataforma | Último medido |
|---|---|---|
| <field> | <N caracteres / N elementos> | <déjalo vacío hasta que midas> |

Mide con un script, no a ojo: `len(text)` después de normalizar los saltos de línea.

## 4. Prioridad de recorte

Cuando te pases de un límite, recorta en este orden:

1. <lo primero que se corta: normalmente lo más ornamental>
2. <lo segundo>
3. <último recurso: la parte que más información aporta>

## 5. Mapeo de hechos

| Campo | Se toma de |
|---|---|
| <field> | `wiki/entities/<slug>` |
| <field> | `wiki/synthesis/decisions-<period>` |

Todo lo que no esté en esta tabla no puede aparecer en el borrador.

## 6. Nomenclatura

Títulos y etiquetas que este canal muestra tal cual:

| Hueco | Forma |
|---|---|
| <role> | `<exact string>` |

## 7. Prohibiciones

| Nunca escribas | Porque |
|---|---|
| <claim> | <una línea: riesgo, afirmación excesiva o algo no verificable> |

## 8. Lista de aceptación

- [ ] Cada campo dentro de su límite, medido
- [ ] Ningún hecho ausente del mapeo
- [ ] Lista de prohibiciones recorrida, punto por punto
- [ ] Variante de idioma coherente con la principal
- [ ] Los enlaces resuelven; la ortografía de los nombres propios coincide con el wiki

## 9. Procedimiento de publicación

1. Redacta en `outputs/<channel>/drafts/<YYYY-MM>/`.
2. Mide, pasa la lista, corrige el borrador.
3. Publica y actualiza `state.md` (versión, fecha, desviaciones) y `wiki/log.md`.
