<!-- translation: es · canonical: docs/career/source-cv-2026.md · synced: 2026-11-14 -->

---
title: "Fuente: CV 2026 (PDF)"
created: 2026-01-03
type: source
tags: [timeline]
raw: raw/cv-2026.pdf
updated: 2026-01-03
---
# Fuente: CV 2026 (PDF)

`raw/cv-2026.pdf`, dos páginas, leído el 2026-01-03. Todo lo de abajo es lo que dice el documento; nada es inferido.

> Ejemplo ficticio. El archivo no existe; copia la misma forma para tu propio CV.

## Qué aporta

- Cuatro periodos de empleo, 2015-04 → hoy. Se copian a `employer-nexo` y a ningún otro sitio.
- Dos nombres de puesto, en español y en inglés, para el mismo rol.
- Palabras clave del stack: .NET, C#, SQL Server, Angular, MAUI.
- Una certificación: AZ-900, 2025-09 → `person`.
- Un título, 2015 → `person`.

## Qué no aporta (preguntas abiertas)

- El segundo periodo tiene año pero no mes. Pregunta antes de anotar una fecha; no inventes un `-01`.
- El mismo puesto aparece como "Junior Programmer" en una línea y como "Programmer" en otra.
- No hay nombres de cliente: el documento nombra productos, no clientes. Las páginas de cliente se quedan vacías hasta que una segunda fuente las confirme.

## Notas de manejo

- Los datos personales (teléfono, correo, dirección, número de documento) se quedan en `raw/`. Esta página nunca los repite, y `wiki_lint.py` falla si lo hace.
- El original no se versiona: `raw/*` está ignorado por git excepto `README.md`.
- Si un CV posterior contradice esta página, añade una nota fechada en **Preguntas abiertas**. No sobrescribas en silencio: la contradicción es información.

## Páginas siguientes

`raw/cv-2026.pdf` → esta página → `employer-nexo` (periodos), `position-*` (puestos), `person` (totales, idiomas, certificaciones).

## Relacionado

`employer-nexo` · `person` · `decisions-2026`
