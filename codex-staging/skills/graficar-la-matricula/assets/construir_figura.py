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
import hashlib
import html
import json
import math
import re
import sys
from pathlib import Path

# LA VERSIÓN DEL COMPOSITOR (MAT-51, qa del 13-10). Dos veces un cliente compuso un reporte nuevo con un compositor
# viejo —«0 sedes universitarias», «12 sedes universitarias» en un reporte de IP y CFT— aunque el servicio estaba al día:
# el compositor viaja en el plugin y el plugin no se había actualizado. El spec dice qué compositor necesita
# (`requires_composer`); este se niega si es más viejo, y `--version` le deja al agente comprobarlo antes.
COMPOSITOR = "0.45.0"


# LA HUELLA DEL SPEC (MAT-56, qa de O'Higgins del 14-10). El control de cifras revisa las lecturas contra el spec, pero
# confiaba en el spec: un agente que copió la portada a mano a un script podía cambiar un número sin aviso. El servicio
# firma cada spec que entrega (`huella`) y este compositor la recalcula: si no coincide, no compone y dice qué parte
# cambió. Firma lo que el agente NO escribe: quedan fuera `title` y `subtitle` del spec (el encuadre es suyo) y el texto
# de las lecturas (`text`, `compatible`). El servidor importa estas mismas funciones: hay una sola definición.
DEL_AGENTE = ("title", "subtitle")
_PARTES = {"cover": "la portada", "series": "las series", "facts": "las cifras de contexto",
           "annotations": "las anotaciones", "provenance": "la procedencia", "bars": "las barras", "rows": "las filas",
           "points": "los puntos"}


def _canonico(v):
    """La forma que se firma: sin huellas anidadas ni el texto de las lecturas, y 84.0 igual a 84 (un número reescrito
    con otro formato es el mismo número)."""
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, dict):
        fuera = ("huella", "text", "compatible") if v.get("kind") == "reading" else ("huella",)
        return {k: _canonico(x) for k, x in v.items() if k not in fuera}
    if isinstance(v, list):
        return [_canonico(x) for x in v]
    return v


def _hash(v) -> str:
    texto = json.dumps(_canonico(v), sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


def huella(spec: dict) -> dict:
    """`total` firma todo lo que no es del agente; `partes`, cada pieza, para poder decir cuál cambió."""
    nucleo = {k: v for k, v in spec.items() if k not in DEL_AGENTE and k != "huella"}
    partes = {}
    for k, v in nucleo.items():
        if k == "sections" and isinstance(v, list):
            for i, sec in enumerate(v):
                partes[f"la sección «{(sec or {}).get('title') or i + 1}»"] = _hash(sec)
        else:
            partes[_PARTES.get(k, f"«{k}»")] = _hash(v)
    return {"total": _hash(nucleo), "partes": partes}


def revisar_huella(spec: dict) -> list[str]:
    """Vacío si el spec es el que entregó el servicio; si no, por qué."""
    dada = spec.get("huella")
    if not isinstance(dada, dict) or not dada.get("total"):
        return ["el spec no trae su huella: no es el que entregó el servicio, o viene de una versión anterior"]
    nueva = huella(spec)
    if nueva["total"] == dada["total"]:
        return []
    antes = dada.get("partes") or {}
    cambio = ([k for k, h in nueva["partes"].items() if antes.get(k) != h]
              + [k for k in antes if k not in nueva["partes"]])
    return [f"el spec no es el que entregó el servicio: cambió {', '.join(cambio) or 'su contenido'}"]


def _version(v: str) -> tuple:
    return tuple(int(x) for x in str(v).split(".") if x.isdigit())

ASSETS = Path(__file__).resolve().parent
FACTOR_DE_SALTO = 3
MAX_EN_UN_PANEL = 5
# Con más de MAX_EN_UN_PANEL sedes va un solo panel con el nombre al final de cada línea (MAT-29), y se
# rotulan a lo más estas: las de mayor matrícula. Igual que MAX_ROTULOS en la receta (la prueba lo exige).
MAX_ROTULOS = 15
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
        # UNA FORMA DESCONOCIDA ES UN PLUGIN VIEJO, no un dato malo (qa/, 08-10): se dice qué hacer.
        return [f"esta versión del plugin no conoce la forma «{js(forma)}» (conoce {', '.join(VALIDADORES)}): "
                "el servicio es más nuevo que el plugin instalado; actualiza el plugin y vuelve a componer"]
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


def _validar_anios(spec: dict, errores: list[str]) -> None:
    x = spec.get("x") or []
    if not x or any(not isinstance(v, int) or isinstance(v, bool) or (i > 0 and v <= x[i - 1])
                    for i, v in enumerate(x)):
        errores.append("«x» tiene que ser una lista de años enteros, creciente y sin repetir")


def validar_series(spec: dict, errores: list[str]) -> list[str]:
    _validar_anios(spec, errores)
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
            elif v is not None and spec.get("unit") == "pct" and v > 100:
                errores.append(f"«{label}» {p.get('year')}: un porcentaje no puede pasar de 100")
    # LA UNIDAD DE UNA SERIE (MAT-76): matrícula por defecto; el reporte por carrera trae series en % y en pesos
    if spec.get("unit", "count") not in UNIDADES + ("idx",):
        errores.append(f"«unit» tiene que ser una de {', '.join(UNIDADES + ('idx',))}")
    # UN ÍNDICE DICE SU BASE (MAT-76, etapa 2): sin el año en que todas valen 100, dos curvas no se comparan.
    if spec.get("unit") == "idx":
        base = spec.get("base_year")
        if base not in x:
            errores.append("un índice trae «base_year», uno de los años de «x»")
        else:
            for serie in series:
                v = next((p.get("value") for p in serie.get("points") or [] if p.get("year") == base), None)
                if v != 100:
                    errores.append(f"«{serie.get('label')}» no vale 100 en el año base {base}")
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
    _validar_anios(spec, errores)
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


UNIDADES = ("count", "pct", "years", "clp_m")


def _numero(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validar_barras(spec: dict, errores: list[str]) -> list[str]:
    """`barras_sedes`: una barra por sede activa; las sedes en retirada no entran al cuerpo."""
    if spec.get("unit") not in UNIDADES:
        errores.append(f"«unit» tiene que ser una de {', '.join(UNIDADES)}")
    barras = spec.get("bars") or []
    if not barras:
        errores.append("no hay barras")
    nombres, fuera = set(), set(spec.get("excluded") or [])
    for b in barras:
        label = b.get("label")
        if not str(label or "").strip():
            errores.append("una barra no trae «label»")
        if label in nombres:
            errores.append(f"la barra «{label}» está repetida")
        nombres.add(label)
        if label in fuera:
            errores.append(f"«{label}» está en retirada y no puede aparecer en el cuerpo")
        v = b.get("value")
        if v is not None and (not _numero(v) or v < 0):
            errores.append(f"«{label}»: el valor tiene que ser un número no negativo o null")
        elif v is not None and spec.get("unit") == "pct" and v > 100:
            errores.append(f"«{label}»: un porcentaje no puede pasar de 100")
        n = b.get("n")
        if n is not None and (not isinstance(n, int) or isinstance(n, bool) or n < 0):
            errores.append(f"«{label}»: «n» tiene que ser un entero no negativo")
        if b.get("detail") is not None and not isinstance(b.get("detail"), str):
            errores.append(f"«{label}»: «detail» tiene que ser un texto o null")
    ref = spec.get("reference")
    if ref is not None:
        if not str(ref.get("label") or "").strip() or not _numero(ref.get("value")) or ref["value"] < 0:
            errores.append("«reference» tiene que traer «label» y un «value» numérico no negativo, o ser null")
    return errores


EXTREMOS = ("p10_p90", "min_max")


def validar_rangos(spec: dict, errores: list[str]) -> list[str]:
    """`rangos_sedes`: una distribución por fila. Una fila no robusta no trae caja (MAT-19)."""
    if spec.get("unit") != "score":
        errores.append("«unit» tiene que ser score")
    if spec.get("whiskers") not in EXTREMOS:
        errores.append(f"«whiskers» tiene que ser una de {', '.join(EXTREMOS)}")
    filas = spec.get("rows") or []
    if not filas:
        errores.append("no hay filas")
    nombres, fuera = set(), set(spec.get("excluded") or [])
    for f in filas:
        label = f.get("label")
        if not str(label or "").strip():
            errores.append("una fila no trae «label»")
        if label in nombres:
            errores.append(f"la fila «{label}» está repetida")
        nombres.add(label)
        if label in fuera:
            errores.append(f"«{label}» está en retirada y no puede aparecer en el cuerpo")
        n = f.get("n")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            errores.append(f"«{label}»: «n» tiene que ser un entero no negativo")
        if not isinstance(f.get("robust"), bool):
            errores.append(f"«{label}»: «robust» tiene que ser true o false")
        if not all(_numero(f.get(k)) for k in ("low", "mid", "high")):
            errores.append(f"«{label}»: «low», «mid» y «high» tienen que ser números")
            continue
        caja = f.get("q1") is not None and f.get("q3") is not None
        if f.get("robust") is False and caja:
            errores.append(f"«{label}»: una fila no robusta no lleva caja («q1» y «q3» van null)")
        if f.get("robust") is True and not (caja and _numero(f["q1"]) and _numero(f["q3"])):
            errores.append(f"«{label}»: una fila robusta trae «q1» y «q3»")
        orden = ([f["low"], f["q1"], f["mid"], f["q3"], f["high"]] if caja and _numero(f["q1"]) and _numero(f["q3"])
                 else [f["low"], f["mid"], f["high"]])
        if any(v < orden[i - 1] for i, v in enumerate(orden) if i):
            errores.append(f"«{label}»: los valores no están en orden (extremo bajo ≤ caja ≤ centro ≤ caja ≤ extremo alto)")
    ref = spec.get("reference")
    if ref is not None:
        if not str(ref.get("label") or "").strip() or not _numero(ref.get("value")):
            errores.append("«reference» tiene que traer «label» y un «value» numérico, o ser null")
    return errores


# Los redondeos a un decimal de cada tramo pueden alejar la suma de 100 en unas décimas, no más.
TOLERANCIA_SUMA = 1.0


def _validar_tramos(label: str, valores, claves: list, errores: list[str]) -> None:
    if not isinstance(valores, dict) or set(valores) != set(claves):
        errores.append(f"«{label}»: «values» tiene que traer un valor por tramo ({', '.join(claves)})")
        return
    if not all(_numero(v) and v >= 0 for v in valores.values()):
        errores.append(f"«{label}»: cada tramo tiene que ser un número no negativo")
        return
    if abs(sum(valores.values()) - 100) > TOLERANCIA_SUMA:
        errores.append(f"«{label}»: los tramos suman {_num(round(sum(valores.values()), 1))}, no 100")


def validar_partidas(spec: dict, errores: list[str]) -> list[str]:
    """`barras_partidas` (MAT-23): cada fila es una sede partida en tramos que suman 100%."""
    if spec.get("unit") != "pct":
        errores.append("«unit» tiene que ser pct")
    tramos = spec.get("segments") or []
    claves = [t.get("key") for t in tramos]
    if not 2 <= len(tramos) <= len(COLORES_TRAMOS):
        errores.append(f"«segments» tiene que traer entre 2 y {len(COLORES_TRAMOS)} tramos")
    if len(set(claves)) != len(claves) or not all(str(k or "").strip() for k in claves) \
            or not all(str(t.get("label") or "").strip() for t in tramos):
        errores.append("cada tramo trae «key» y «label», y las «key» no se repiten")
    filas = spec.get("rows") or []
    if not filas:
        errores.append("no hay filas")
    nombres, fuera = set(), set(spec.get("excluded") or [])
    for f in filas:
        label = f.get("label")
        if not str(label or "").strip():
            errores.append("una fila no trae «label»")
        if label in nombres:
            errores.append(f"la fila «{label}» está repetida")
        nombres.add(label)
        if label in fuera:
            errores.append(f"«{label}» está en retirada y no puede aparecer en el cuerpo")
        _validar_tramos(label, f.get("values"), claves, errores)
        n = f.get("n")
        if n is not None and (not isinstance(n, int) or isinstance(n, bool) or n < 0):
            errores.append(f"«{label}»: «n» tiene que ser un entero no negativo")
        if f.get("detail") is not None and not isinstance(f.get("detail"), str):
            errores.append(f"«{label}»: «detail» tiene que ser un texto o null")
    ref = spec.get("reference")
    if ref is not None:
        if not str(ref.get("label") or "").strip():
            errores.append("«reference» tiene que traer «label», o ser null")
        _validar_tramos("reference", ref.get("values"), claves, errores)
    return errores


# Los colores de los tramos, en orden: azul y bermellón para dos (lo bueno y lo que se pierde), y para
# cuatro la escala del reporte local: los dos títulos en azules, seguir en ámbar, salir sin título en bermellón.
COLORES_TRAMOS = ("#0072B2", "#56B4E9", "#E69F00", "#D55E00")

# MAT-24: los ejes de una dispersión, los cuadrantes que nombra y lo mínimo para que un plano diga algo.
# «pp»: puntos porcentuales, una diferencia entre dos porcentajes (el mapa social: % pagado − % prioritario, MAT-76);
# es el único eje que admite negativos, entre −100 y 100.
UNIDADES_EJE = ("score", "pct", "clp_m", "pp")
CUADRANTES = ("x_above_y_above", "x_above_y_below", "x_below_y_above", "x_below_y_below")
MIN_EN_PLANO = 3


def validar_dispersion(spec: dict, errores: list[str]) -> list[str]:
    """`dispersion_sedes` (MAT-24): una burbuja por sede, dos ejes y el país como referencia en los dos."""
    for eje in ("x", "y"):
        e_ = spec.get(eje) or {}
        if not str(e_.get("label") or "").strip() or e_.get("unit") not in UNIDADES_EJE:
            errores.append(f"«{eje}» tiene que traer «label» y una «unit» de {', '.join(UNIDADES_EJE)}")
    puntos = spec.get("points") or []
    if len(puntos) < MIN_EN_PLANO:
        errores.append(f"un plano necesita al menos {MIN_EN_PLANO} sedes")
    nombres, fuera = set(), set(spec.get("excluded") or [])
    for p in puntos:
        label = p.get("label")
        if not str(label or "").strip():
            errores.append("una burbuja no trae «label»")
        if label in nombres:
            errores.append(f"la burbuja «{label}» está repetida")
        nombres.add(label)
        if label in fuera:
            errores.append(f"«{label}» está en retirada y no puede aparecer en el cuerpo")
        for eje in ("x", "y"):
            v = p.get(eje)
            if (spec.get(eje) or {}).get("unit") == "pp":
                if not _numero(v) or not -100 <= v <= 100:
                    errores.append(f"«{label}»: «{eje}» tiene que ser un número entre −100 y 100")
            elif not _numero(v) or v < 0:
                errores.append(f"«{label}»: «{eje}» tiene que ser un número no negativo")
            elif (spec.get(eje) or {}).get("unit") == "pct" and v > 100:
                errores.append(f"«{label}»: un porcentaje no puede pasar de 100")
        if not isinstance(p.get("size"), int) or isinstance(p.get("size"), bool) or p["size"] < 0:
            errores.append(f"«{label}»: «size» tiene que ser un entero no negativo")
    ref = spec.get("reference")
    if not isinstance(ref, dict) or not _numero(ref.get("x")) or not _numero(ref.get("y")) or not str(ref.get("label") or "").strip():
        errores.append("«reference» tiene que traer «label», «x» e «y»: sin el país los cuadrantes no significan nada")
    if set((spec.get("quadrant_labels") or {}).keys()) != set(CUADRANTES):
        errores.append(f"«quadrant_labels» tiene que nombrar los cuatro cuadrantes ({', '.join(CUADRANTES)})")
    return errores


def _validar_par(label: str, f: dict, unidad: str, errores: list[str]) -> None:
    for k in ("a", "b"):
        v = f.get(k)
        if v is not None and (not _numero(v) or v < 0):
            errores.append(f"«{label}»: «{k}» tiene que ser un número no negativo o null")
        elif v is not None and unidad == "pct" and v > 100:
            errores.append(f"«{label}»: un porcentaje no puede pasar de 100")


def validar_pares(spec: dict, errores: list[str]) -> list[str]:
    """`barras_pares` (MAT-76, etapa 2): dos barras por fila, A contra B (% de colegio pagado y % prioritario)."""
    if spec.get("unit") not in UNIDADES:
        errores.append(f"«unit» tiene que ser una de {', '.join(UNIDADES)}")
    par = spec.get("pair") or {}
    a, b = str(par.get("a") or "").strip(), str(par.get("b") or "").strip()
    if not a or not b or a == b:
        errores.append("«pair» tiene que nombrar «a» y «b», distintos")
    filas = spec.get("rows") or []
    if not filas:
        errores.append("no hay filas")
    nombres, fuera = set(), set(spec.get("excluded") or [])
    for f in filas:
        label = f.get("label")
        if not str(label or "").strip():
            errores.append("una fila no trae «label»")
        if label in nombres:
            errores.append(f"la fila «{label}» está repetida")
        nombres.add(label)
        if label in fuera:
            errores.append(f"«{label}» está en retirada y no puede aparecer en el cuerpo")
        _validar_par(label, f, spec.get("unit"), errores)
        if f.get("detail") is not None and not isinstance(f.get("detail"), str):
            errores.append(f"«{label}»: «detail» tiene que ser un texto o null")
        n = f.get("n")
        if n is not None and (not isinstance(n, int) or isinstance(n, bool) or n < 0):
            errores.append(f"«{label}»: «n» tiene que ser un entero no negativo")
    ref = spec.get("reference")
    if ref is not None:
        if not str(ref.get("label") or "").strip() or not _numero(ref.get("a")) or not _numero(ref.get("b")):
            errores.append("«reference» tiene que traer «label», «a» y «b», o ser null")
        else:
            _validar_par("reference", ref, spec.get("unit"), errores)
    return errores


VALIDADORES = {"matricula_series": validar_series, "matricula_region": validar_region,
               "barras_sedes": validar_barras, "rangos_sedes": validar_rangos,
               "barras_partidas": validar_partidas, "dispersion_sedes": validar_dispersion,
               "barras_pares": validar_pares}


def barras_visibles(spec: dict) -> tuple[list, int]:
    """Igual que `barrasVisibles` en la receta: con dato, y sin los ceros si son más del 70%."""
    con = [b for b in spec.get("bars") or [] if b.get("value") is not None]
    ceros = sum(1 for b in con if b["value"] == 0)
    ocultar = bool(con) and ceros / len(con) > 0.7
    filas = sorted([b for b in con if not (ocultar and b["value"] == 0)], key=lambda b: -b["value"])
    return filas, (ceros if ocultar else 0)


def _fmt_unidad(v, unidad: str) -> str:
    if unidad == "clp_m":
        return "$" + f"{v:.2f}".replace(".", ",") + " M"
    if unidad == "pct":
        return f"{v:.1f}".rstrip("0").rstrip(".").replace(".", ",") + "%"
    if unidad in ("years", "idx"):
        return f"{v:.1f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"{v:,.0f}".replace(",", ".")


def _miles(v) -> str:
    return "sin total" if v is None else f"{v:,.0f}".replace(",", ".")


def _pct(v) -> str:
    return "no derivable" if v is None else (f"+{v}" if v > 0 else f"{v}").replace(".", ",") + "%"


def tabla(spec: dict) -> str:
    """La tabla que se entrega cuando la figura no se dibuja: los mismos datos, sin interpolar."""
    if spec.get("form") == "barras_sedes":
        filas = ["| Fila | Valor | n | Detalle |", "|---|---:|---:|---|"]
        for b in spec.get("bars") or []:
            v = "sin dato" if b.get("value") is None else _fmt_unidad(b["value"], spec.get("unit"))
            filas.append(f"| {b.get('label')} | {v} | {'' if b.get('n') is None else b['n']} | {b.get('detail') or ''} |")
        return "\n".join(filas)
    if spec.get("form") == "rangos_sedes":
        bajo, alto = ("p10", "p90") if spec.get("whiskers") == "p10_p90" else ("Mínimo", "Máximo")
        filas = [f"| Sede | {bajo} | p25 | Mediana | p75 | {alto} | n |", "|---|---:|---:|---:|---:|---:|---:|"]
        for f in spec.get("rows") or []:
            c = [_fmt_unidad(f.get(k), "years") if f.get(k) is not None else "—" for k in ("low", "q1", "mid", "q3", "high")]
            eti = f"{f.get('label')} — {f['detail']}" if f.get("detail") else f.get("label")
            filas.append(f"| {eti} | " + " | ".join(c) + f" | {f.get('n')} |")
        return "\n".join(filas)
    if spec.get("form") == "dispersion_sedes":
        x, y = spec.get("x") or {}, spec.get("y") or {}
        filas = [f"| Sede | {x.get('label')} | {y.get('label')} | {spec.get('size_label') or 'tamaño'} |", "|---|---:|---:|---:|"]
        ref = spec.get("reference") or {}
        for p in (spec.get("points") or []) + ([{**ref, "size": None}] if ref else []):
            celda = lambda v, u: _fmt_unidad(v, "years" if u == "score" else u) if _numero(v) else "sin dato"
            filas.append(f"| {p.get('label')} | {celda(p.get('x'), x.get('unit'))} | {celda(p.get('y'), y.get('unit'))} | "
                         f"{'' if p.get('size') is None else _fmt_unidad(p['size'], 'count')} |")
        return "\n".join(filas)
    if spec.get("form") == "barras_partidas":
        tramos = spec.get("segments") or []
        filas = ["| Fila | " + " | ".join(str(t.get("label")) for t in tramos) + " | n | Detalle |",
                 "|---|" + "---:|" * len(tramos) + "---:|---|"]
        ref = spec.get("reference")
        for f in (spec.get("rows") or []) + ([ref] if ref else []):
            v = f.get("values") or {}
            celdas = [_fmt_unidad(v[t.get("key")], "pct") if _numero(v.get(t.get("key"))) else "sin dato" for t in tramos]
            filas.append(f"| {f.get('label')} | " + " | ".join(celdas)
                         + f" | {'' if f.get('n') is None else f['n']} | {f.get('detail') or ''} |")
        return "\n".join(filas)
    if spec.get("form") == "barras_pares":
        par = spec.get("pair") or {}
        filas = [f"| Fila | {par.get('a')} | {par.get('b')} | n | Detalle |", "|---|---:|---:|---:|---|"]
        ref = spec.get("reference")
        for f in (spec.get("rows") or []) + ([ref] if ref else []):
            celda = lambda v: _fmt_unidad(v, spec.get("unit")) if _numero(v) else "sin dato"
            filas.append(f"| {f.get('label')} | {celda(f.get('a'))} | {celda(f.get('b'))} | "
                         f"{'' if f.get('n') is None else f['n']} | {f.get('detail') or ''} |")
        return "\n".join(filas)
    if spec.get("form") == "matricula_region":
        if not spec.get("retreating_sites"):
            # sin sedes en retirada, una sola columna (MAT-48): la segunda repetiría la primera
            filas = ["| Año | Todas las sedes |", "|---|---:|"]
            filas += [f"| {a} | {_miles(t)} |" for a, t in zip(spec.get("x") or [], spec.get("total") or [])]
            return "\n".join(filas)
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
            celdas.append("sin dato" if v is None else _fmt_unidad(v, spec.get("unit") or "count"))
        filas.append(f"| {a} | " + " | ".join(celdas) + " |")
    return "\n".join([cab, sep, *filas])


def e(texto) -> str:
    return html.escape(str(texto if texto is not None else ""), quote=False)


def notas_region(spec: dict) -> str:
    """El pie de la serie regional: el crecimiento de lo que se dibuja y todo lo que no es firme."""
    items = []
    g = spec["growth"]
    desde, hasta = g["period"]
    if spec.get("retreating_sites"):
        items.append(f"<li>Crecimiento {desde}→{hasta}: <b>{e(_pct(g.get('total')))}</b> con todas las sedes; "
                     f"<b>{e(_pct(g.get('active')))}</b> sin las sedes en retirada.</li>")
    else:
        items.append(f"<li>Crecimiento {desde}→{hasta}: <b>{e(_pct(g.get('total')))}</b>.</li>")
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


def notas_barras(spec: dict) -> str:
    items = []
    visibles, ocultas = barras_visibles(spec)
    ref = spec.get("reference")
    if ocultas and not visibles:
        # Sin barras no hay línea punteada que explicar: el valor nacional se dice en la misma línea.
        nac = f"; el valor {e(ref['label'])} es {e(_fmt_unidad(ref['value'], spec.get('unit')))}" if ref else ""
        items.append(f"<li>Las {ocultas} sedes valen 0, así que no hay barras que dibujar{nac}.</li>")
        return f'<div class="notas"><ul>{"".join(items)}</ul></div>'
    if ocultas:
        items.append(f"<li>{ocultas} sedes valen 0 y no se dibujan: son la gran mayoría y el gráfico "
                     "quedaría vacío.</li>")
    sin = [b["label"] for b in spec.get("bars") or [] if b.get("value") is None]
    if sin:
        items.append("<li>Sin dato: " + e("; ".join(sin)) + ".</li>")
    if ref:
        items.append(f"<li>La línea punteada es el valor {e(ref['label'])} "
                     f"({e(_fmt_unidad(ref['value'], spec.get('unit')))}), calculado sobre todos los "
                     "estudiantes del país, no como promedio de las sedes.</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>' if items else ""


def notas_rangos(spec: dict) -> str:
    items = []
    if spec.get("whiskers") == "p10_p90":
        items.append("<li>La caja va del percentil 25 al 75, la marca gruesa es la mediana y los extremos llegan "
                     "al percentil 10 y al 90.</li>")
    else:
        items.append("<li>La línea va del mínimo al máximo; la caja, cuando está, va del percentil 25 al 75, y la "
                     "marca gruesa es la mediana.</li>")
    sueltas = [f for f in spec.get("rows") or [] if f.get("robust") is False]
    if sueltas:
        items.append("<li>Las filas marcadas con «~» tienen pocos puntajes y van sin caja: unos percentiles sobre "
                     "tan poca gente fingirían una distribución que el dato no sostiene.</li>")
    ref = spec.get("reference")
    if ref:
        items.append(f"<li>La línea punteada es la mediana {e(ref['label'])} "
                     f"({e(_fmt_unidad(ref['value'], 'years'))}), calculada sobre todos los estudiantes del país "
                     "que rindieron, no como promedio de las sedes.</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>'


def notas_partidas(spec: dict) -> str:
    items = []
    ref = spec.get("reference")
    if ref:
        items.append(f"<li>La última fila, separada, es el {e(ref['label'])}: calculada sobre todos los estudiantes "
                     "del país, no como promedio de las sedes.</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>' if items else ""


def notas_pares(spec: dict) -> str:
    items = []
    ref = spec.get("reference")
    if ref:
        items.append(f"<li>La última fila, separada, es el {e(ref['label'])}: calculada sobre todos los estudiantes "
                     "del país, no como promedio de las filas.</li>")
    for aviso in spec.get("notices") or []:
        items.append(f"<li>{e(aviso)}</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>' if items else ""


def notas_dispersion(spec: dict) -> str:
    q = spec.get("quadrant_labels") or {}
    items = ["<li>Los cuadrantes: arriba a la derecha, " + e(q.get("x_above_y_above")) + "; arriba a la izquierda, "
             + e(q.get("x_below_y_above")) + "; abajo a la derecha, " + e(q.get("x_above_y_below"))
             + "; abajo a la izquierda, " + e(q.get("x_below_y_below")) + ".</li>"]
    items += [f"<li>{e(a)}</li>" for a in spec.get("notices") or []]
    puntos = spec.get("points") or []
    if len(puntos) > 3:
        # La receta rotula hasta 15, las de más entrantes cuyo nombre no tapa a otro: el pie no promete cuántas.
        items.append(f"<li>Se rotulan hasta {MAX_ROTULOS} sedes, las de más entrantes cuyo nombre cabe sin tapar a otro; "
                     "al pasar el cursor por cualquier burbuja se ve de qué sede es y sus valores.</li>")
    return f'<div class="notas"><ul>{"".join(items)}</ul></div>' if items else ""


def notas_html(spec: dict) -> str:
    """Lo que el lector tiene que saber para no leer mal la figura, derivado de los datos."""
    if spec.get("form") == "dispersion_sedes":
        return notas_dispersion(spec)
    if spec.get("form") == "barras_partidas":
        return notas_partidas(spec)
    if spec.get("form") == "barras_pares":
        return notas_pares(spec)
    if spec.get("form") == "barras_sedes":
        return notas_barras(spec)
    if spec.get("form") == "rangos_sedes":
        return notas_rangos(spec)
    if spec.get("form") == "matricula_region":
        return notas_region(spec)
    items = []
    # El pie anota sólo lo que se dibuja: los huecos de una sede en retirada se declaran en el spec (la
    # receta lo exige), pero esa sede no se dibuja y su nota sólo alarga el pie. Si TODAS están en
    # retirada, se dibujan todas y se anotan todas.
    todas = spec.get("series") or []
    dibujadas = {s.get("label") for s in todas if not s.get("retreating")} or {s.get("label") for s in todas}
    for a in spec.get("annotations") or []:
        if a.get("series") not in dibujadas:
            continue
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
    if len(activas) > MAX_ROTULOS:
        items.append(f"<li>Se rotulan las {MAX_ROTULOS} sedes de mayor matrícula al final de la serie; las otras "
                     f"{len(activas) - MAX_ROTULOS} siguen dibujadas, sin nombre: al pasar el cursor por un punto "
                     "se ve de qué sede es.</li>")
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


# ── el reporte (MAT-17) ──────────────────────────────────────────────────────────────────────────
# Las lecturas las redacta el agente. Lo que se protege son las CIFRAS: todo número de un texto tiene
# que estar en lo que entregó el servicio —portada, figuras, cifras de contexto—, entero o redondeado
# a un decimal. Un número que no está, se inventó o se calculó por fuera, y el reporte se niega.
# Un decimal escrito con punto («1.32 millones»): NUMERO lo lee como dos números y el «1» pasaba el control.
PUNTO_DECIMAL = re.compile(r"(?<![\w.,])\d+\.\d{1,2}(?!\w|[.,]\d)")
NUMERO = re.compile(r"(?<![\w.,])\d{1,3}(?:\.\d{3})+(?:,\d+)?(?![\w])|(?<![\w.,])\d+(?:,\d+)?(?![\w])")


def _a_float(texto: str) -> float:
    return float(texto.replace(".", "").replace(",", "."))


CLAVES_PORCENTAJE = ("pct", "weight_pct")


def _variantes(v: float) -> set:
    """El valor exacto y su redondeo a un decimal. NO el redondeo a entero de un valor con decimales:
    con él, un 9,3% respaldaba un «9%» inventado (se vio al probarlo el 08-10-2026)."""
    return {float(v), round(float(v), 1)}


def numeros_del_spec(nodo, acc=None, pct=None, es_pct=False):
    """Todos los números que el servicio entregó: (todos, sólo los porcentajes).

    Un porcentaje es un valor de una figura con `unit: pct`, su referencia, un crecimiento, un peso
    (`weight_pct`), o un número seguido de «%» en un texto del servicio.
    """
    acc = set() if acc is None else acc
    pct = set() if pct is None else pct
    if isinstance(nodo, dict) and nodo.get("form") == "dispersion_sedes":
        # Una dispersión tiene dos ejes con su propia unidad (MAT-24): cada coordenada es % si su eje lo es.
        for p in (nodo.get("points") or []) + ([nodo["reference"]] if isinstance(nodo.get("reference"), dict) else []):
            for eje in ("x", "y"):
                numeros_del_spec(p.get(eje), acc, pct, (nodo.get(eje) or {}).get("unit") == "pct")
            numeros_del_spec(p.get("size"), acc, pct)
        resto = {k: v for k, v in nodo.items() if k not in ("points", "reference", "form")}
        return numeros_del_spec(resto, acc, pct)
    if isinstance(nodo, dict):
        en_pct = es_pct or nodo.get("unit") == "pct"
        for k, v in nodo.items():
            # Una serie en % (MAT-76 qa): sus puntos son porcentajes; sin "series" y "points" aquí, el control
            # rechazaba «el 59% con gratuidad en 2025», que es un punto de la figura.
            hijo_pct = en_pct and k in ("bars", "value", "reference", "rows", "series", "points", "a", "b") \
                or k in CLAVES_PORCENTAJE \
                or str(k).endswith("_pct") \
                or k == "growth" or (es_pct and k in ("total", "active"))
            if k == "blocks" and isinstance(v, list):
                for bl in v:
                    if bl.get("kind") in ("facts", "note", "findings"):
                        # Las cifras y las notas que escribe el servicio también respaldan (MAT-20).
                        numeros_del_spec({k: x for k, x in bl.items() if k != "kind"}, acc, pct)
                    if bl.get("kind") == "figure":
                        numeros_del_spec(bl.get("figure"), acc, pct)
                        # Los órdenes y los cambios que el servicio calculó junto a la figura (MAT-27):
                        # «creció 39,8%» o «su mayor alza, 632» salen de ahí y tienen respaldo.
                        numeros_del_spec(bl.get("groups"), acc, pct)
            elif k == "values" and en_pct and isinstance(v, dict):
                # Los tramos de `barras_partidas` (MAT-23) son porcentajes.
                for x in v.values():
                    numeros_del_spec(x, acc, pct, True)
            elif k == "growth" and isinstance(v, dict):
                for gk, gv in v.items():
                    if gk != "period":
                        numeros_del_spec(gv, acc, pct, True)
                numeros_del_spec(v.get("period"), acc, pct)
            else:
                numeros_del_spec(v, acc, pct, hijo_pct)
    elif isinstance(nodo, list):
        for v in nodo:
            numeros_del_spec(v, acc, pct, es_pct)
    elif _numero(nodo):
        # UNA CAÍDA SE CITA SIN SIGNO (MAT-51, qa del 13-10): la lectura dice «cayó 2,7%» o «−2,7%», y NUMERO lee
        # el número sin el signo; con sólo -2.7 en el spec, el control rechazaba una cifra que el servicio entregó.
        variantes = _variantes(nodo) | (_variantes(abs(nodo)) if nodo < 0 else set())
        acc.update(variantes)
        if es_pct:
            pct.update(variantes)
    elif isinstance(nodo, str):
        # LOS TEXTOS DEL SERVICIO TAMBIÉN RESPALDAN: «más de 30 años» es la definición del eje y está en
        # el subtítulo que escribió el servicio. Los textos del agente (las lecturas) no entran aquí.
        for m in re.finditer(NUMERO, nodo):
            acc.add(_a_float(m.group()))
            if nodo[m.end():m.end() + 2].lstrip().startswith("%"):
                pct.add(_a_float(m.group()))
    return acc, pct


def lecturas(spec: dict):
    for sec in spec.get("sections") or []:
        for b in sec.get("blocks") or []:
            if b.get("kind") == "reading":
                yield sec, b


def validar_reporte(spec: dict) -> list[str]:
    """Lo que hace que el REPORTE no se componga. Una figura inválida no lo detiene: va como tabla."""
    errores = []
    for campo in ("title", "subtitle"):
        if not str(spec.get(campo) or "").strip():
            errores.append(f"falta «{campo}»")
    if "source" in spec:
        errores.append("el spec trae «source»: la fuente no se escribe, se deriva de «provenance»")
    if not (spec.get("provenance") or {}).get("fuente_original"):
        errores.append("falta «provenance.fuente_original»")
    retiradas = {r.get("label") for r in (spec.get("cover") or {}).get("retreating") or []}
    for sec in spec.get("sections") or []:
        for b in sec.get("blocks") or []:
            if b.get("kind") != "figure":
                continue
            f = b.get("figure") or {}
            if f.get("form") not in VALIDADORES:
                # Una figura inválida va como tabla y el reporte sigue; una forma que esta versión no conoce,
                # no: la tabla saldría vacía y el reporte se publicaría a medias.
                errores += validar(f)
                continue
            nombres = [x.get("label") for x in (f.get("bars") or []) + (f.get("series") or []) + (f.get("rows") or [])
                       + (f.get("points") or [])]
            dentro = sorted(retiradas & set(nombres))
            if dentro:
                # EL GATE DEL REPORTE LOCAL: una sede en retirada se declara en la portada y no entra al cuerpo.
                errores.append(f"«{b.get('id')}» trae sedes en retirada en el cuerpo: {', '.join(dentro)}")
    todos, porcentajes = numeros_del_spec({k: v for k, v in spec.items() if k != "sections"})
    for sec in spec.get("sections") or []:
        t, p_ = numeros_del_spec({"blocks": [b for b in sec.get("blocks") or []
                                             if b.get("kind") in ("figure", "facts", "note", "findings")]})
        todos |= t
        porcentajes |= p_
    for sec, b in lecturas(spec):
        for campo in ("text", "compatible"):
            texto = str(b.get(campo) or "")
            for m in re.finditer(PUNTO_DECIMAL, texto):
                errores.append(f"la lectura de «{b.get('for')}» ({campo}) escribe {m.group()} con punto decimal: en "
                               f"Chile el decimal va con coma ({m.group().replace('.', ',')})")
            for m in re.finditer(NUMERO, texto):
                valor, es_pct = _a_float(m.group()), texto[m.end():m.end() + 2].lstrip().startswith("%")
                if es_pct and valor not in porcentajes:
                    errores.append(f"la lectura de «{b.get('for')}» ({campo}) cita {m.group()}%, que no es un "
                                   "porcentaje de los que entregó el servicio")
                elif not es_pct and valor not in todos:
                    errores.append(f"la lectura de «{b.get('for')}» ({campo}) cita {m.group()}, que no está en los "
                                   "datos que entregó el servicio")
    return errores


def _parrafos(texto: str) -> str:
    """Párrafos separados por una línea en blanco; un bloque cuyas líneas empiezan con «- » es una lista (la síntesis)."""
    partes = []
    for p in str(texto).split("\n\n"):
        lineas = [x.strip() for x in p.strip().splitlines() if x.strip()]
        if lineas and all(x.startswith("- ") for x in lineas):
            partes.append("<ul>" + "".join(f"<li>{e(x[2:].strip())}</li>" for x in lineas) + "</ul>")
        elif lineas:
            partes.append(f"<p>{e(p.strip())}</p>")
    return "".join(partes)


def _tabla_html(md: str) -> str:
    filas = [f.strip("|").split("|") for f in md.splitlines() if f.strip() and not set(f) <= set("|-: ")]
    cab, *cuerpo = filas
    return ('<div class="tw"><table><thead><tr>' + "".join(f"<th>{e(c.strip())}</th>" for c in cab) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{e(c.strip())}</td>" for c in f) + "</tr>" for f in cuerpo)
            + "</tbody></table></div>")


def figura_html(id_: str, spec: dict, dibujables: dict, avisos: list) -> str:
    errores = validar(spec)
    cabeza = f'<p class="ft">{e(spec.get("title"))}</p><p class="fs">{e(spec.get("subtitle"))}</p>'
    if errores:
        avisos.append(f"figura «{id_}» no dibujada: {'; '.join(errores)}")
        return ('<figure>' + cabeza + '<p class="negativa">Esta figura no se dibuja: '
                + e("; ".join(errores)) + ". Los datos van en la tabla.</p>" + _tabla_html(tabla(spec)) + "</figure>")
    fuente = e(str(spec["provenance"]["fuente_original"]).strip())
    if spec.get("form") == "barras_sedes" and not barras_visibles(spec)[0]:
        # TODAS EN CERO: no hay gráfico, y una caja vacía con su pie parece una figura rota (qa/, 08-10).
        return f'<figure>{cabeza}{notas_html(spec)}<p class="src">Fuente: {fuente}.</p></figure>'
    dibujables[id_] = spec
    return (f'<figure>{cabeza}<div class="grafico" id="fig-{e(id_)}"></div>{notas_html(spec)}'
            f'<p class="src">Fuente: {fuente}.</p></figure>')


def cifras_html(b: dict) -> str:
    """Un bloque de cifras del servicio (MAT-20): el marco de una sección, con su conclusión calculada."""
    def valor(x):
        if x.get("unit") == "ratio":
            return f"{x['value']:.2f}".replace(".", ",")
        if x.get("unit") == "score":
            return _fmt_unidad(x["value"], "years")
        return _fmt_unidad(x["value"], "pct" if x.get("unit") == "pct" else "count")
    celdas = "".join(f'<div class="cifra"><span class="v">{e(valor(x))}</span><span class="l">{e(x["label"])}</span></div>'
                     for x in b.get("items") or [])
    titulo = f'<p class="ft">{e(b["title"])}</p>' if b.get("title") else ""
    conclusion = f'<p class="conclusion">{e(b["conclusion"])}</p>' if b.get("conclusion") else ""
    return f'<div class="cifras">{titulo}<div class="rejilla">{celdas}</div>{conclusion}</div>'


def componer_reporte(spec: dict, avisos: list) -> str:
    c = spec.get("cover") or {}
    # La ciudad va una vez: si el nombre ya la trae (una institución con dos sedes), no se repite.
    def con_ciudad(x):
        ciudad = x.get("city")
        sobra = ciudad == spec.get("region") or str(x["label"]).endswith(f"({ciudad})")
        return e(x["label"]) + ("" if sobra else f" ({e(ciudad)})")
    sedes = "".join(f"<li>{con_ciudad(x)}</li>" for x in c.get("sites") or [])
    # SIN DATO NO ES CERO (MAT-51): una unidad sin matrícula el último año se dice así, no «2025: 0»
    retiradas = "; ".join(f"{x['label']} ({c.get('year_last')}: {_fmt_unidad(x['enrollment_last'], 'count')})"
                          if x.get("enrollment_last") is not None else f"{x['label']} (sin matrícula en {c.get('year_last')})"
                          for x in c.get("retreating") or [])
    # LA PORTADA DICE QUÉ SE CUENTA (MAT-51): «sedes universitarias» era fijo; la portada común de la región y el
    # reporte técnico traen su propio rótulo (`sites_label`) o un párrafo de entrada (`lead`) en vez de la lista.
    partes = [f'<header class="portada"><h1>{e(spec["title"])}</h1><p class="sub">{e(spec["subtitle"])}</p>']
    if c.get("lead"):
        partes.append(f'<p>{e(c["lead"])}</p>')
    if c.get("sites"):
        partes.append(f'<p>{len(c["sites"])} {e(c.get("sites_label") or "sedes universitarias en la región")}:</p>'
                      f'<ul class="sedes">{sedes}</ul>')
    if retiradas:
        sin_matricula = any(x.get("enrollment_last") is None for x in c.get("retreating") or [])
        cierre = ("Ya casi no reciben estudiantes nuevos; las que tienen cifra conservan matrícula."
                  if sin_matricula else "Conservan matrícula, pero ya casi no reciben estudiantes nuevos.")
        partes.append(f'<p class="retirada"><b>En retirada</b>, y fuera del resto del reporte: {e(retiradas)}. '
                      f"{cierre}</p>")
    partes.append(f'<p class="universo">Universo: {e(c.get("universe"))}.</p></header>')
    dibujables: dict = {}
    for sec in spec.get("sections") or []:
        partes.append(f'<section><h2>{e(sec.get("title"))}</h2><p class="pregunta">{e(sec.get("question"))}</p>')
        for b in sec.get("blocks") or []:
            if b.get("kind") == "figure":
                partes.append(figura_html(b.get("id"), b.get("figure") or {}, dibujables, avisos))
            elif b.get("kind") == "facts":
                partes.append(cifras_html(b))
            elif b.get("kind") == "note":
                partes.append('<div class="nota-seccion">' + _parrafos(b.get("text") or "") + "</div>")
            elif b.get("kind") == "reading" and (b.get("text") or b.get("compatible")):
                partes.append('<div class="lectura">' + _parrafos(b.get("text") or ""))
                if b.get("compatible"):
                    partes.append('<p class="compatible"><b>Explicación compatible:</b> '
                                  + e(b["compatible"]) + "</p>")
                partes.append("</div>")
        partes.append("</section>")
    # EL PIE LISTA TODAS LAS FUENTES QUE USA LA PÁGINA (MAT-30): decía sólo «matrícula», y el reporte cita
    # también puntajes, fichas del DEMRE, el registro de egreso y la SEP.
    fuentes = [spec["provenance"]["fuente_original"]]
    for sec in spec.get("sections") or []:
        for b in sec.get("blocks") or []:
            prov = (b.get("figure") or {}).get("provenance", {}) if b.get("kind") == "figure" else {}
            # Una figura con dos ejes de fuentes distintas (MAT-24) las declara por separado en `fuentes`.
            for f in prov.get("fuentes") or [prov.get("fuente_original")]:
                if f and f not in fuentes:
                    fuentes.append(f)
    lista = "".join(f"<li>{e(f)}</li>" for f in fuentes)
    partes.append(f'<footer><p class="src">Fuentes de este reporte:</p><ul class="src">{lista}</ul>'
                  f'<p class="src">Universo: {e(spec["provenance"].get("universo"))}.</p></footer>')
    return _pagina(spec["title"], "".join(partes), dibujables)


def _pagina(titulo: str, cuerpo: str, figuras: dict) -> str:
    plantilla = (ASSETS / "figura.template.html").read_text(encoding="utf-8")
    return (plantilla
            .replace("__TITULO__", e(titulo))
            .replace("__CUERPO__", cuerpo)
            .replace("/* __D3__ */", (ASSETS / "vendor" / "d3.min.js").read_text(encoding="utf-8"))
            .replace("/* __PLOT__ */", (ASSETS / "vendor" / "plot.umd.min.js").read_text(encoding="utf-8"))
            .replace("__RECETAS__", (ASSETS / "recetas_plot.js").read_text(encoding="utf-8"))
            .replace("/* __FIGURAS__ */", json.dumps(figuras, ensure_ascii=False)))


def componer(spec: dict) -> str:
    fuente = str(spec["provenance"]["fuente_original"]).strip()
    cuerpo = (
        "<figure>"
        f'<p class="ft">{e(spec["title"])}</p>'
        f'<p class="fs">{e(spec["subtitle"])}</p>'
        '<div class="grafico" id="fig-figura"></div>'
        f"{notas_html(spec)}"
        f'<p class="src">Fuente: {e(fuente)}.</p>'
        "</figure>"
    )
    return _pagina(spec["title"], cuerpo, {"figura": spec})


# El reporte de una región y el de una carrera (MAT-76) son la misma forma: portada, secciones con figuras y lecturas.
FORMAS_REPORTE = ("reporte_region", "reporte_carrera")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", type=Path)
    ap.add_argument("--salida", type=Path)
    ap.add_argument("--version", action="store_true", help="la versión de este compositor")
    a = ap.parse_args()
    if a.version:
        print(COMPOSITOR)
        return 0
    if not (a.entrada and a.salida):
        ap.error("faltan --entrada y --salida")
    spec = json.loads(a.entrada.read_text(encoding="utf-8"))
    pide = spec.get("requires_composer")
    if pide and _version(pide) > _version(COMPOSITOR):
        print(f"NO SE COMPONE: este spec necesita el compositor {pide} y éste es el {COMPOSITOR}. El plugin está "
              "desactualizado: actualízalo y vuelve a componer; no publiques una página armada con otro.", file=sys.stderr)
        return 2
    copia = revisar_huella(spec)
    if copia:
        print(f"NO SE COMPONE: {copia[0]}. No lo corrijas a mano: vuelve a pedirlo a la herramienta y guarda su `spec` "
              "en el archivo tal cual, sin reescribirlo ni copiar sus valores. Sólo el título, el subtítulo y el texto "
              "de las lecturas son tuyos.", file=sys.stderr)
        return 2

    if spec.get("form") in FORMAS_REPORTE:
        errores = validar_reporte(spec)
        if errores:
            print("NO SE COMPONE EL REPORTE:", file=sys.stderr)
            for err in errores:
                print(f"  - {err}", file=sys.stderr)
            print("\nCorrige la lectura (usa sólo cifras del spec) o vuelve a pedir el reporte.", file=sys.stderr)
            return 2
        avisos: list = []
        pagina = componer_reporte(spec, avisos)
        jerga = sorted(set(JERGA.findall(pagina)))
        if jerga:
            print(f"NO SE COMPONE: la página trae vocabulario interno ({', '.join(jerga)}).", file=sys.stderr)
            return 2
        a.salida.write_text(pagina, encoding="utf-8")
        n_fig = sum(1 for sec in spec["sections"] for b in sec["blocks"] if b.get("kind") == "figure")
        n_lec = sum(1 for _, b in lecturas(spec) if b.get("text") or b.get("compatible"))
        print(a.salida)
        print(f"reporte · {len(spec['sections'])} sección(es) · {n_fig} figuras · {n_lec} lecturas · "
              f"{len(avisos)} figuras como tabla")
        for aviso in avisos:
            print(f"  aviso: {aviso}")
        return 0

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
    if spec["form"] != "matricula_series":
        # una figura suelta de otra forma (MAT-49: barras de participación): el resumen es su forma y sus filas
        filas = spec.get("bars") or spec.get("rows") or spec.get("points") or []
        print(f"{spec['form']} · {len(filas)} filas · avisos: {len(spec.get('notices') or [])}")
        return 0
    activas = [s for s in spec["series"] if not s.get("retreating")]
    print(f"series dibujadas: {len(activas)} de {len(spec['series'])} · "
          f"un panel{'' if len(activas) <= MAX_EN_UN_PANEL else ' con el nombre al final de cada línea'} · "
          f"anotaciones: {len(spec.get('annotations') or [])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
