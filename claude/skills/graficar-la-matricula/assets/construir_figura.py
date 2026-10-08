#!/usr/bin/env python3
"""Compone una figura del saber desde su spec: una página autocontenida, sin CDN.

    python3 construir_figura.py --entrada figura.json --salida figura.html

El agente es dueño del encuadre —título, subtítulo, qué series— y de las notas; este script es
dueño de la forma. Tres cosas que hace cumplir, porque su incumplimiento no se ve a simple vista:

1. **Una serie con un hueco o un valor que salta, sin declarar, no se dibuja.** Las exigencias se
   DERIVAN de los datos, no de lo que diga el spec: un hueco omitido no se puede esconder.
2. **La fuente no se escribe.** Se estampa desde `provenance.fuente_original`, copiada de la
   herramienta. Si el spec trae `source`, se niega.
3. **La página no lleva vocabulario interno** de quien construye el saber.

Cuando se niega sale con código 2, dice por qué y **imprime la tabla** que hay que entregar en lugar
del gráfico. Las reglas son las mismas que `validar()` en `recetas_plot.js`; `probar_figura.py`
comprueba que las dos digan lo mismo sobre los mismos specs.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
FACTOR_DE_SALTO = 3
MAX_EN_UN_PANEL = 5
# Lo que el lector no tiene por qué entender: nombres de reglas, documentos y piezas internas.
JERGA = re.compile(r"regla R[0-9]|del pack|artefacto|ADR-")


def _vacio(p: dict) -> bool:
    return p.get("value") is None


def exigencias(spec: dict) -> tuple[list[dict], list[dict], list[dict]]:
    huecos, saltos, bordes = [], [], []
    x = spec.get("x") or []
    for serie in spec.get("series") or []:
        pts = sorted(serie.get("points") or [], key=lambda p: p.get("year", 0))
        con_dato = [p for p in pts if not _vacio(p)]
        if not con_dato:
            continue
        primero, ultimo = con_dato[0]["year"], con_dato[-1]["year"]
        for p in pts:
            if _vacio(p) and primero < p["year"] < ultimo:
                huecos.append({"series": serie.get("label"), "year": p["year"]})
        desde, hasta = (min(x), max(x)) if x else (primero, ultimo)
        if primero > desde or ultimo < hasta:
            bordes.append({"series": serie.get("label"), "from": primero, "to": ultimo})
        for i in range(1, len(con_dato) - 1):
            a, v, b = con_dato[i - 1]["value"], con_dato[i]["value"], con_dato[i + 1]["value"]
            if a <= 0 or b <= 0 or v <= 0:
                continue
            sube = v >= FACTOR_DE_SALTO * a and v >= FACTOR_DE_SALTO * b
            baja = v * FACTOR_DE_SALTO <= a and v * FACTOR_DE_SALTO <= b
            if sube or baja:
                saltos.append({"series": serie.get("label"), "year": con_dato[i]["year"], "value": v})
    return huecos, saltos, bordes


def _num(v) -> str:
    """Un número como lo escribe JavaScript en un mensaje: 1025, no 1025.0."""
    return str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)


_FALTA = object()


def js(v) -> str:
    """Un valor como lo escribe JavaScript en un mensaje: los dos guardias tienen que decir lo mismo."""
    if v is _FALTA:
        return "undefined"
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    return _num(v) if isinstance(v, (int, float)) else str(v)


def crecimiento(x: list, v: list, desde: int, hasta: int):
    """Igual que en la receta: redondeo a un decimal con empates hacia arriba (Math.round), no al par."""
    if desde not in x or hasta not in x:
        return None
    a, b = v[x.index(desde)], v[x.index(hasta)]
    if a is None or b is None or not a:
        return None
    return math.floor(1000 * (b - a) / a + 0.5) / 10


def validar(spec: dict) -> list[str]:
    """Los motivos por los que el spec NO se dibuja. Mismas reglas y mensajes que la receta."""
    forma = spec.get("form", _FALTA) if isinstance(spec, dict) else _FALTA
    if forma not in VALIDADORES:
        return [f"la forma «{js(forma)}» no está implementada; hoy existen matricula_series y matricula_region"]
    errores: list[str] = []
    encabezado(spec, errores)
    return VALIDADORES[forma](spec, errores)


def encabezado(spec: dict, errores: list[str]) -> None:
    for campo in ("title", "subtitle"):
        if not str(spec.get(campo) or "").strip():
            errores.append(f"falta «{campo}»")
    if "source" in spec:
        errores.append("el spec trae «source»: la fuente no se escribe, se deriva de «provenance»")
    if not str((spec.get("provenance") or {}).get("fuente_original") or "").strip():
        errores.append("falta «provenance.fuente_original»: cópiala tal cual de la herramienta")
    x = spec.get("x") or []
    if not x or any(not isinstance(v, int) or isinstance(v, bool) or (i > 0 and v <= x[i - 1])
                    for i, v in enumerate(x)):
        errores.append("«x» tiene que ser una lista de años enteros, creciente y sin repetir")


def validar_series(spec: dict, errores: list[str]) -> list[str]:
    x = spec.get("x") or []
    series = spec.get("series") or []
    if not series:
        errores.append("no hay series")
    nombres: set = set()
    for serie in series:
        label = serie.get("label")
        if not str(label or "").strip():
            errores.append("una serie no trae «label»")
        if label in nombres:
            errores.append(f"la serie «{label}» está repetida")
        nombres.add(label)
        anios = [p.get("year") for p in serie.get("points") or []]
        faltan = [a for a in x if a not in anios]
        if faltan:
            errores.append(f"«{label}» no trae punto para {', '.join(map(str, faltan))}: un año sin dato va como null, no se omite")
        if len(set(anios)) != len(anios):
            errores.append(f"«{label}» repite años")
        for p in serie.get("points") or []:
            if p.get("year") not in x:
                errores.append(f"«{label}» trae el año {p.get('year')}, que no está en «x»")
            v = p.get("value")
            if v is not None and (not isinstance(v, (int, float)) or isinstance(v, bool) or v < 0):
                errores.append(f"«{label}» {p.get('year')}: el valor tiene que ser un número no negativo o null")
    if series and all(s.get("retreating") for s in series):
        errores.append("todas las series vienen en retirada: no queda nada que comparar")
    notas = {f"{a.get('kind')}|{a.get('series')}|{a.get('year')}": a.get("note") for a in spec.get("annotations") or []}
    huecos, saltos, _ = exigencias(spec)
    for h in huecos:
        clave = f"gap|{h['series']}|{h['year']}"
        if clave not in notas:
            errores.append(f"hueco sin declarar: «{h['series']}» no tiene dato en {h['year']}")
        elif not str(notas[clave] or "").strip():
            errores.append(f"el hueco de «{h['series']}» en {h['year']} se anotó sin nota")
    for s in saltos:
        clave = f"inconsistent|{s['series']}|{s['year']}"
        if clave not in notas:
            errores.append(f"valor inconsistente sin declarar: «{s['series']}» {s['year']} = {_num(s['value'])}, "
                           f"{FACTOR_DE_SALTO} veces o más distinto de sus dos vecinos con dato")
        elif not str(notas[clave] or "").strip():
            errores.append(f"el valor inconsistente de «{s['series']}» en {s['year']} se anotó sin nota")
    return errores


def validar_region(spec: dict, errores: list[str]) -> list[str]:
    """`matricula_region`: aritmética, años sin total declarados y crecimiento recalculado."""
    x = spec.get("x") or []
    total, activa = spec.get("total") or [], spec.get("active") or []
    if len(total) != len(x) or len(activa) != len(x):
        errores.append("«total» y «active» tienen que traer un valor por año de «x», con null donde no hay total")
        return errores
    for nombre, v in (("total", total), ("active", activa)):
        for i, y in enumerate(v):
            if y is not None and (not isinstance(y, (int, float)) or isinstance(y, bool) or y < 0):
                errores.append(f"«{nombre}» {x[i]}: tiene que ser un número no negativo o null")
    for i, a in enumerate(x):
        if total[i] is not None and activa[i] is not None and activa[i] > total[i]:
            errores.append(f"{a}: lo activo ({js(activa[i])}) supera al total ({js(total[i])}), y es una parte de él")
    incompletos = spec.get("incomplete") or []

    def declarado(serie, anio, trato):
        return any(c.get("series") == serie and c.get("year") == anio and c.get("treatment") == trato
                   for c in incompletos)
    for nombre, v in (("total", total), ("active", activa)):
        for i, y in enumerate(v):
            if y is None and not declarado(nombre, x[i], "no_total"):
                errores.append(f"año sin total sin declarar: «{nombre}» {x[i]}")
    for c in incompletos:
        serie = c.get("series")
        v = total if serie == "total" else activa if serie == "active" else None
        if v is None:
            errores.append(f"un año incompleto nombra la serie «{js(c.get('series', _FALTA))}», que no existe")
            continue
        anio = c.get("year")
        if anio not in x:
            errores.append(f"un año incompleto nombra {js(c.get('year', _FALTA))}, que no está en «x»")
        else:
            y = v[x.index(anio)]
            trato = c.get("treatment", _FALTA)
            if trato == "no_total" and y is not None:
                errores.append(f"«{serie}» {anio} se declara sin total y trae {js(y)}")
            elif trato == "summed" and y is None:
                errores.append(f"«{serie}» {anio} se declara sumado y no trae valor")
            elif trato not in ("summed", "no_total"):
                errores.append(f"«{serie}» {anio}: el tratamiento «{js(trato)}» no existe")
        if not c.get("missing"):
            errores.append(f"«{serie}» {js(c.get('year', _FALTA))}: un año incompleto tiene que decir qué sede falta")
    g = spec.get("growth") or {}
    periodo = g.get("period") or []
    desde, hasta = (periodo + [None, None])[:2]
    if desde not in x or hasta not in x:
        errores.append("«growth.period» tiene que ser dos años de «x»")
    else:
        for nombre, v in (("total", total), ("active", activa)):
            real = crecimiento(x, v, desde, hasta)
            declarado_g = g.get(nombre)
            if real != declarado_g:
                errores.append(f"el crecimiento «{nombre}» declarado ({js(g.get(nombre, _FALTA))}) "
                               f"no es el de las cifras ({js(real)})")
    difieren = any(t is not None and a is not None and t != a for t, a in zip(total, activa))
    if difieren and not spec.get("retreating_sites"):
        errores.append("las dos curvas difieren y no se nombra ninguna sede en retirada")
    return errores


VALIDADORES = {"matricula_series": validar_series, "matricula_region": validar_region}


def _miles(v) -> str:
    return "sin total" if v is None else f"{v:,.0f}".replace(",", ".")


def _pct(v) -> str:
    return "no derivable" if v is None else (f"+{v}" if v > 0 else f"{v}").replace(".", ",") + "%"


def tabla(spec: dict) -> str:
    """La tabla que se entrega cuando la figura no se dibuja: los mismos datos, sin interpolar."""
    if spec.get("form") == "matricula_region":
        filas = ["| Año | Todas las sedes | Sin las sedes en retirada |", "|---|---:|---:|"]
        for a, t, v in zip(spec.get("x") or [], spec.get("total") or [], spec.get("active") or []):
            filas.append(f"| {a} | {_miles(t)} | {_miles(v)} |")
        return "\n".join(filas)
    series = spec.get("series") or []
    x = spec.get("x") or sorted({p.get("year") for s in series for p in s.get("points") or []})
    cab = "| Año | " + " | ".join(str(s.get("label")) for s in series) + " |"
    sep = "|---|" + "---:|" * len(series)
    filas = []
    for a in x:
        celdas = []
        for s in series:
            v = next((p.get("value") for p in s.get("points") or [] if p.get("year") == a), None)
            celdas.append("sin dato" if v is None else f"{v:,.0f}".replace(",", "."))
        filas.append(f"| {a} | " + " | ".join(celdas) + " |")
    return "\n".join([cab, sep, *filas])


def e(texto) -> str:
    return html.escape(str(texto if texto is not None else ""), quote=False)


def notas_region(spec: dict) -> str:
    """El pie de la serie regional: el crecimiento de lo que se dibuja y todo lo que no es firme."""
    items = []
    g = spec["growth"]
    desde, hasta = g["period"]
    items.append(f"<li>Crecimiento {desde}→{hasta}: <b>{e(_pct(g.get('total')))}</b> con todas las sedes; "
                 f"<b>{e(_pct(g.get('active')))}</b> sin las sedes en retirada.</li>")
    for c in spec.get("incomplete") or []:
        if c.get("series") != "total":
            continue
        quienes = "; ".join(f"{m.get('site')} (cerca del {str(m.get('weight_pct')).replace('.', ',')}%)"
                            for m in c.get("missing") or [])
        if c.get("treatment") == "summed":
            items.append(f'<li><span class="marca">{e(c["year"])}, sumado sin una sede:</span> falta {e(quienes)}. '
                         "El punto va hueco.</li>")
        else:
            items.append(f'<li><span class="marca">{e(c["year"])}, sin total:</span> falta {e(quienes)}, y sumar '
                         "sin ella mostraría una caída que no ocurrió.</li>")
    for a in spec.get("annotations") or []:
        if a.get("kind") == "inconsistent":
            items.append(f'<li><span class="marca">{e(a.get("year"))}:</span> {e(a.get("note"))}</li>')
    if spec.get("retreating_sites"):
        items.append("<li>Sedes en retirada (la banda): " + e("; ".join(spec["retreating_sites"])) + ".</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>'


def notas_html(spec: dict) -> str:
    """Lo que el lector tiene que saber para no leer mal la figura, derivado de los datos."""
    if spec.get("form") == "matricula_region":
        return notas_region(spec)
    items = []
    for a in spec.get("annotations") or []:
        if a.get("kind") == "inconsistent":
            items.append(f'<li><span class="marca">{e(a.get("series"))}, {e(a.get("year"))}:</span> {e(a.get("note"))}</li>')
        elif a.get("kind") == "gap":
            items.append(f'<li>{e(a.get("series"))}, {e(a.get("year"))}: {e(a.get("note"))}</li>')
    _, _, bordes = exigencias(spec)
    activas = {s.get("label") for s in spec.get("series") or [] if not s.get("retreating")}
    for b in bordes:
        if b["series"] in activas:
            tramo = f"desde {b['from']}" if b["to"] == max(spec["x"]) else f"de {b['from']} a {b['to']}"
            items.append(f"<li>{e(b['series'])}: con registro {e(tramo)}.</li>")
    retiradas = [s for s in spec.get("series") or [] if s.get("retreating")]
    if retiradas:
        nombres = []
        for s in retiradas:
            ultimo = next((p for p in sorted(s.get("points") or [], key=lambda p: -p["year"]) if p.get("value") is not None), None)
            extra = f" ({ultimo['year']}: {ultimo['value']:,.0f})".replace(",", ".") if ultimo else ""
            nombres.append(f"{s.get('label')}{extra}")
        items.append("<li>No se comparan, por estar en retirada: " + e("; ".join(nombres)) + ".</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>' if items else ""


def componer(spec: dict) -> str:
    fuente = str(spec["provenance"]["fuente_original"]).strip()
    cuerpo = (
        "<figure>"
        f'<p class="ft">{e(spec["title"])}</p>'
        f'<p class="fs">{e(spec["subtitle"])}</p>'
        '<div class="grafico" id="grafico"></div>'
        f"{notas_html(spec)}"
        f'<p class="src">Fuente: {e(fuente)}.</p>'
        "</figure>"
    )
    plantilla = (ASSETS / "figura.template.html").read_text(encoding="utf-8")
    return (plantilla
            .replace("__TITULO__", e(spec["title"]))
            .replace("__CUERPO__", cuerpo)
            .replace("/* __D3__ */", (ASSETS / "vendor" / "d3.min.js").read_text(encoding="utf-8"))
            .replace("/* __PLOT__ */", (ASSETS / "vendor" / "plot.umd.min.js").read_text(encoding="utf-8"))
            .replace("__RECETAS__", (ASSETS / "recetas_plot.js").read_text(encoding="utf-8"))
            .replace("/* __FIGURA__ */", json.dumps(spec, ensure_ascii=False)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    spec = json.loads(a.entrada.read_text(encoding="utf-8"))

    errores = validar(spec)
    if errores:
        print("NO SE DIBUJA:", file=sys.stderr)
        for err in errores:
            print(f"  - {err}", file=sys.stderr)
        print("\nEntrega esta tabla en lugar del gráfico, y di por qué:\n", file=sys.stderr)
        print(tabla(spec), file=sys.stderr)
        return 2

    pagina = componer(spec)
    jerga = sorted(set(JERGA.findall(pagina)))
    if jerga:
        print(f"NO SE COMPONE: la página trae vocabulario interno ({', '.join(jerga)}). "
              "Revisa título, subtítulo y notas.", file=sys.stderr)
        return 2
    a.salida.write_text(pagina, encoding="utf-8")
    print(a.salida)
    if spec["form"] == "matricula_region":
        print(f"serie regional · {len(spec['x'])} años · incompletos: {len(spec.get('incomplete') or [])} · "
              f"sedes en retirada: {len(spec.get('retreating_sites') or [])}")
        return 0
    activas = [s for s in spec["series"] if not s.get("retreating")]
    print(f"series dibujadas: {len(activas)} de {len(spec['series'])} · "
          f"{'un panel' if len(activas) <= MAX_EN_UN_PANEL else 'un panel por serie'} · "
          f"anotaciones: {len(spec.get('annotations') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
