<!-- translation: es · canonical: docs/career/linkedin-draft-excerpt.md · synced: 2026-11-14 -->

# Borrador de LinkedIn — extracto (ficticio)

Muestra cómo un borrador renderiza hechos sin poseerlos. El borrador es desechable; el wiki no.

## Titular

```
Backend Developer · .NET · APIs & integrations · Madrid
```
Longitud: 55 / 220. Medida con `len(text)`, no estimada.

## Extracto — dos primeros párrafos

```
Backend developer in Madrid with over seven years building business systems,
most of them inside a consultancy — so the same employer, several clients,
and a lot of context switching.

My core is C# and .NET: APIs, integrations, and the unglamorous middle layer
between a legacy reporting stack and something that can be tested.
```

## IDs de claim

El párrafo de "About" renderiza el total que posee `person.md`. El borrador apunta al claim en lugar de reescribirlo como un hecho independiente:

```markdown
<!-- claim:person-1 -->
over seven years building business systems
```

Si `person.md` deja de definir `claim:person-1`, `wiki_lint.py` falla: un borrador puede citar un hecho, nunca inventar la página que debería poseerlo.

## Entrada de experiencia

```
Backend Developer / Analista Programador
Nexo Digital · 2024-03 → present · Hybrid

Delivered for a banking client (see the client's own entry, not this field):
- Rewrote the reporting service; 14 reports decommissioned
- Owned the integration layer: 6 services, .NET 6 → .NET 8
```

## Lo que este extracto no hace

- No escribe las fechas a mano: se copian de `employer.md`, que las posee.
- No pone el cliente en el campo de organización. La organización sigue siendo el empleador legal.
- No nombra un nivel de seniority superior al que permite el registro.
- No repite los totales; "over seven years" es un renderizado del `7+` de la página de la persona.

## Cuando algo está mal aquí

Si un número o un título está mal, la corrección va a la página del wiki y el borrador se vuelve a renderizar. Editar este archivo para corregir un hecho es la única edición que rompe el modelo (véase `METHOD.md` §3, ley 4).
