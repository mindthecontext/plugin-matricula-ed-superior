# El spec de `matricula_series`

**Lo emite el servicio:** `figura_matricula(region, instituciones)` devuelve este objeto en `spec`. Lo
guardas tal cual; sólo `title` y `subtitle` son tuyos. Esta página existe para que sepas qué contiene.

Claves en inglés y textos en español. Ejemplo con dos sedes, una de ellas con un hueco y un valor
inconsistente:

```json
{
  "form": "matricula_series",
  "title": "La matrícula de dos sedes universitarias de La Araucanía",
  "subtitle": "matrícula total de pregrado por sede, universidades, 2007–2025",
  "provenance": {
    "fuente_original": "<copiado de procedencia_matricula.fuente_original>",
    "universo": "<copiado de procedencia_matricula.universo>"
  },
  "x": [2007, 2008, 2009, 2010, 2011, 2012, "…", 2025],
  "series": [
    { "label": "U. Santo Tomás",
      "points": [{ "year": 2007, "value": 1097 }, { "year": 2008, "value": 1139 }, "…"] },
    { "label": "Pontificia U. Católica de Chile",
      "points": [{ "year": 2007, "value": null }, { "year": 2008, "value": 216 },
                 { "year": 2009, "value": 234 }, { "year": 2010, "value": null },
                 { "year": 2011, "value": 1025 }, { "year": 2012, "value": 196 }, "…"] },
    { "label": "U. La República", "retreating": true, "points": ["…"] }
  ],
  "annotations": [
    { "series": "Pontificia U. Católica de Chile", "year": 2010, "kind": "gap",
      "note": "sin registro en la fuente" },
    { "series": "Pontificia U. Católica de Chile", "year": 2011, "kind": "inconsistent",
      "note": "el registro es inconsistente en este tramo: el valor no calza con los años vecinos" }
  ],
  "notices": []
}
```

| Clave | Obligatoria | Qué es |
|---|---|---|
| `form` | sí | Siempre `matricula_series`. |
| `title` | sí | El QUÉ: frase nominal que nombra la vista. No una oración ni el hallazgo. |
| `subtitle` | sí | Unidad, universo y ventana. |
| `provenance` | sí | El bloque `procedencia_matricula` de la herramienta, con `fuente_original`. |
| `x` | sí | Los años, enteros y crecientes, tal como vienen en `serie_matricula.x`. |
| `series[].label` | sí | El nombre de la sede, escrito como se escribe. |
| `series[].points` | sí | **Un punto por año de `x`**, con `null` donde no hay dato. |
| `series[].retreating` | no | `true` para una sede con `en_retirada`: no se dibuja, se nombra al pie. |
| `annotations` | según los datos | Una por hueco (`gap`) y una por valor inconsistente (`inconsistent`), con `series`, `year` y `note`. |
| `notices` | no | Avisos que el lector necesita y no salen de los datos. |

**Prohibido:** `source`. La fuente se estampa desde `provenance`.

**Lo que la receta decide sola**, sin que se pueda configurar desde el spec:
- La base del eje es cero.
- La línea se corta en un hueco y no pasa por un valor inconsistente.
- Hasta cinco series van en un panel, distinguidas por color, trazo y forma. Con más, va un panel por
  sede con el mismo eje.
- Los bordes de cobertura («con registro desde 2008») se anotan solos al pie.


# El spec de `matricula_region`

**Lo emite el servicio:** `figura_matricula_region(region)` lo devuelve en `spec`. Sólo `title` y
`subtitle` son tuyos.

```json
{
  "form": "matricula_region",
  "title": "La matrícula universitaria de La Araucanía",
  "subtitle": "matrícula total de pregrado de la región, universidades, 2007–2025; con todas las sedes y sin las que están en retirada",
  "provenance": { "fuente_original": "…", "universo": "…" },
  "x": [2007, "…", 2025],
  "total": [22271, "…", 36351],
  "active": [22198, "…", 36299],
  "growth": { "period": [2019, 2025], "total": 11.8, "active": 14.5 },
  "incomplete": [
    { "series": "total", "year": 2010, "treatment": "summed",
      "missing": [{ "site": "Pontificia U. Católica de Chile", "weight_pct": 0.84 }] }
  ],
  "annotations": [{ "year": 2011, "kind": "inconsistent", "note": "el total incluye un valor inconsistente de …" }],
  "retreating_sites": ["U. Tecnológica de Chile INACAP", "U. La República"],
  "notices": []
}
```

**Lo que la receta comprueba**, y por lo que se niega:
- Lo activo nunca supera al total.
- Todo `null` está declarado en `incomplete` con `treatment: "no_total"`.
- Todo año incompleto dice qué sede falta.
- **El crecimiento declarado es el de las cifras:** la receta lo recalcula.
- Si las dos curvas difieren, se nombra al menos una sede en retirada.
