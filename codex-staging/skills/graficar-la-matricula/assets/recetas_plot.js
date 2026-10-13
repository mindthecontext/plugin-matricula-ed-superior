// Recetas de visualización del saber Matrícula de Educación Superior. Hay tres formas:
// `matricula_series`, la serie de matrícula de una o varias sedes; `matricula_region`, la de una
// región entera, con y sin las sedes en retirada; y `barras_sedes`, un eje con una barra por sede.
//
// EL REPARTO. El agente produce un spec JSON con datos y encuadre; la receta dibuja. Las reglas
// van pegadas a la receta y no se configuran desde el spec: que la línea se corte en un hueco, que
// un valor que salta se declare, que la base del eje sea cero. El spec aporta datos y encuadre,
// nunca el criterio.
//
// LA NEGATIVA ES LA CONDUCTA CORRECTA, no un error que sortear. Una serie con un hueco o un salto
// sin declarar produciría un gráfico que miente con cifras correctas; en ese caso se entrega la
// tabla.
//
// Las series se distinguen por color, trazo y forma de marca: el color solo excluye a quien no lo
// percibe.
//
// Este archivo se carga en el navegador y también en node, para probar `validar()` sin DOM.

// La paleta de datos es fija y no cambia con el tema (Okabe-Ito, en el orden del sitio publicado).
const COLORES = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#56779b"];
const SIMBOLOS = ["circle", "square", "triangle", "diamond", "cross"];
const TRAZOS = [null, "6 3", "2 3", "8 3 2 3", "1 2"];
// Más series que colores no caben en un solo panel sin volverse un ovillo: se parten en paneles.
const MAX_EN_UN_PANEL = COLORES.length;
// MUCHAS SEDES (MAT-29): un solo panel, el nombre al final de cada línea. Siete colores aptos para
// daltonismo (Okabe-Ito sin el amarillo, que no se lee sobre crema) por cinco símbolos: combinaciones
// únicas hasta 35 sedes. Con tantas líneas lo que identifica es el NOMBRE; el color y el símbolo ayudan.
const COLORES_MUCHAS = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#56779b"];
// Cuántas sedes llevan nombre. FIJO, no según el ancho: el pie (Python) dice cuántas quedan sin nombre y
// tiene que decir lo mismo que el dibujo. 15 nombres a 14 px caben en el alto útil más chico (≈260 px).
const MAX_ROTULOS = 15;

// Un valor es INCONSISTENTE con su serie si multiplica por este factor —o divide— a sus dos
// vecinos con dato. Es juicio, y está aquí y no en el spec a propósito: quien arma el spec no
// puede subirlo para que su serie pase. El caso que lo motivó: una sede con 234 y 196 alrededor
// y 1025 en medio.
const FACTOR_DE_SALTO = 3;

/** Lo que la receta exige declarar, derivado de los datos y no de lo que diga el spec. */
function exigencias(spec) {
  const huecos = [];
  const saltos = [];
  const bordes = [];
  for (const serie of spec.series || []) {
    const pts = (serie.points || []).slice().sort((a, b) => a.year - b.year);
    const conDato = pts.filter(p => p.value !== null && p.value !== undefined);
    if (conDato.length === 0) continue;
    const primero = conDato[0].year;
    const ultimo = conDato[conDato.length - 1].year;
    // Un null ENTRE el primer y el último dato es un hueco: la serie existe y falta un año.
    // Uno en los extremos es el borde de la cobertura: la serie empieza o termina ahí.
    for (const p of pts) {
      const vacio = p.value === null || p.value === undefined;
      if (vacio && p.year > primero && p.year < ultimo) huecos.push({ series: serie.label, year: p.year });
    }
    const desde = Math.min(...(spec.x || [primero]));
    const hasta = Math.max(...(spec.x || [ultimo]));
    if (primero > desde || ultimo < hasta) bordes.push({ series: serie.label, from: primero, to: ultimo });
    for (let i = 1; i < conDato.length - 1; i++) {
      const [a, v, b] = [conDato[i - 1].value, conDato[i].value, conDato[i + 1].value];
      if (a <= 0 || b <= 0 || v <= 0) continue;
      const sube = v >= FACTOR_DE_SALTO * a && v >= FACTOR_DE_SALTO * b;
      const baja = v * FACTOR_DE_SALTO <= a && v * FACTOR_DE_SALTO <= b;
      if (sube || baja) saltos.push({ series: serie.label, year: conDato[i].year, value: v });
    }
  }
  return { huecos, saltos, bordes };
}

/**
 * Los motivos por los que este spec NO se dibuja. Vacío = se puede dibujar.
 *
 * Función pura, sin DOM: el compositor en Python aplica las mismas reglas y una prueba compara
 * las dos sobre los mismos specs.
 */
function validar(spec) {
  const forma = spec && spec.form;
  if (!VALIDADORES[forma]) {
    // UNA FORMA DESCONOCIDA ES UN PLUGIN VIEJO, no un dato malo: el servicio se actualiza al publicar y el
    // plugin instalado puede ir atrás (qa/, 08-10: la §2 salió «no implementada»). Se dice qué hacer.
    return [`esta versión del plugin no conoce la forma «${forma}» (conoce ${Object.keys(VALIDADORES).join(", ")}): ` +
            "el servicio es más nuevo que el plugin instalado; actualiza el plugin y vuelve a componer"];
  }
  const errores = [];
  encabezado(spec, errores);
  return VALIDADORES[forma](spec, errores);
}

/** Lo que toda forma exige: los tres textos con sus roles, la procedencia y los años. */
function encabezado(spec, errores) {
  for (const campo of ["title", "subtitle"]) {
    if (!String(spec[campo] || "").trim()) errores.push(`falta «${campo}»`);
  }
  // LA FUENTE NO SE ESCRIBE: se estampa desde la procedencia que entregó la herramienta.
  if ("source" in spec) errores.push("el spec trae «source»: la fuente no se escribe, se deriva de «provenance»");
  if (!spec.provenance || !String(spec.provenance.fuente_original || "").trim()) {
    errores.push("falta «provenance.fuente_original»: cópiala tal cual de la herramienta");
  }
}

/** Las formas con años: una lista entera, creciente y sin repetir. */
function anios(spec, errores) {
  const x = spec.x || [];
  if (!x.length || x.some((v, i) => !Number.isInteger(v) || (i > 0 && v <= x[i - 1]))) {
    errores.push("«x» tiene que ser una lista de años enteros, creciente y sin repetir");
  }
}

function validarSeries(spec, errores) {
  anios(spec, errores);
  const x = spec.x || [];
  const series = spec.series || [];
  if (!series.length) errores.push("no hay series");
  const nombres = new Set();
  for (const serie of series) {
    if (!String(serie.label || "").trim()) errores.push("una serie no trae «label»");
    if (nombres.has(serie.label)) errores.push(`la serie «${serie.label}» está repetida`);
    nombres.add(serie.label);
    // UN PUNTO POR AÑO, con null donde no hay dato. Si el año sin dato se omite en vez de venir
    // como null, no hay hueco que detectar y la línea se une por encima: la mentira que esto evita.
    const anios = (serie.points || []).map(p => p.year);
    const faltan = x.filter(a => !anios.includes(a));
    if (faltan.length) errores.push(`«${serie.label}» no trae punto para ${faltan.join(", ")}: un año sin dato va como null, no se omite`);
    if (new Set(anios).size !== anios.length) errores.push(`«${serie.label}» repite años`);
    for (const p of serie.points || []) {
      if (!x.includes(p.year)) errores.push(`«${serie.label}» trae el año ${p.year}, que no está en «x»`);
      const vacio = p.value === null || p.value === undefined;
      if (!vacio && (typeof p.value !== "number" || p.value < 0)) {
        errores.push(`«${serie.label}» ${p.year}: el valor tiene que ser un número no negativo o null`);
      }
    }
  }
  if (series.length && series.every(s => s.retreating)) {
    errores.push("todas las series vienen en retirada: no queda nada que comparar");
  }
  const anotadas = new Set((spec.annotations || []).map(a => `${a.kind}|${a.series}|${a.year}`));
  const notas = new Map((spec.annotations || []).map(a => [`${a.kind}|${a.series}|${a.year}`, a.note]));
  const { huecos, saltos } = exigencias(spec);
  for (const h of huecos) {
    const clave = `gap|${h.series}|${h.year}`;
    if (!anotadas.has(clave)) errores.push(`hueco sin declarar: «${h.series}» no tiene dato en ${h.year}`);
    else if (!String(notas.get(clave) || "").trim()) errores.push(`el hueco de «${h.series}» en ${h.year} se anotó sin nota`);
  }
  for (const s of saltos) {
    const clave = `inconsistent|${s.series}|${s.year}`;
    if (!anotadas.has(clave)) {
      errores.push(`valor inconsistente sin declarar: «${s.series}» ${s.year} = ${s.value}, ` +
                   `${FACTOR_DE_SALTO} veces o más distinto de sus dos vecinos con dato`);
    } else if (!String(notas.get(clave) || "").trim()) {
      errores.push(`el valor inconsistente de «${s.series}» en ${s.year} se anotó sin nota`);
    }
  }
  return errores;
}

/** El crecimiento entre dos años de una serie, redondeado a un decimal, o null si falta un extremo. */
function crecimiento(x, v, desde, hasta) {
  const a = v[x.indexOf(desde)], b = v[x.indexOf(hasta)];
  if (a === null || a === undefined || b === null || b === undefined || !a) return null;
  return Math.round(1000 * (b - a) / a) / 10;
}

/**
 * `matricula_region`: el total de una región y lo que queda sin las sedes en retirada.
 *
 * LA RECETA COMPRUEBA LA ARITMÉTICA Y RECALCULA EL CRECIMIENTO. Lo activo no puede superar al total,
 * y el crecimiento que dirá el pie tiene que ser el de las cifras que se dibujan: si el spec trae
 * otro número, se niega. Así el pie no puede contar una historia distinta de la figura.
 */
function validarRegion(spec, errores) {
  anios(spec, errores);
  const x = spec.x || [];
  const total = spec.total || [], activa = spec.active || [];
  if (total.length !== x.length || activa.length !== x.length) {
    errores.push("«total» y «active» tienen que traer un valor por año de «x», con null donde no hay total");
    return errores;
  }
  const vacio = v => v === null || v === undefined;
  for (const [nombre, v] of [["total", total], ["active", activa]]) {
    v.forEach((y, i) => {
      if (!vacio(y) && (typeof y !== "number" || y < 0)) errores.push(`«${nombre}» ${x[i]}: tiene que ser un número no negativo o null`);
    });
  }
  x.forEach((a, i) => {
    if (!vacio(total[i]) && !vacio(activa[i]) && activa[i] > total[i]) {
      errores.push(`${a}: lo activo (${activa[i]}) supera al total (${total[i]}), y es una parte de él`);
    }
  });
  const incompletos = spec.incomplete || [];
  const declarado = (serie, anio, trato) => incompletos.some(c => c.series === serie && c.year === anio && c.treatment === trato);
  for (const [nombre, v] of [["total", total], ["active", activa]]) {
    v.forEach((y, i) => {
      if (vacio(y) && !declarado(nombre, x[i], "no_total")) errores.push(`año sin total sin declarar: «${nombre}» ${x[i]}`);
    });
  }
  for (const c of incompletos) {
    const v = c.series === "total" ? total : c.series === "active" ? activa : null;
    if (!v) { errores.push(`un año incompleto nombra la serie «${c.series}», que no existe`); continue; }
    const y = v[x.indexOf(c.year)];
    if (!x.includes(c.year)) errores.push(`un año incompleto nombra ${c.year}, que no está en «x»`);
    else if (c.treatment === "no_total" && !vacio(y)) errores.push(`«${c.series}» ${c.year} se declara sin total y trae ${y}`);
    else if (c.treatment === "summed" && vacio(y)) errores.push(`«${c.series}» ${c.year} se declara sumado y no trae valor`);
    else if (!["summed", "no_total"].includes(c.treatment)) errores.push(`«${c.series}» ${c.year}: el tratamiento «${c.treatment}» no existe`);
    if (!(c.missing || []).length) errores.push(`«${c.series}» ${c.year}: un año incompleto tiene que decir qué sede falta`);
  }
  const g = spec.growth || {};
  const [desde, hasta] = g.period || [];
  if (!x.includes(desde) || !x.includes(hasta)) {
    errores.push("«growth.period» tiene que ser dos años de «x»");
  } else {
    for (const [nombre, v] of [["total", total], ["active", activa]]) {
      const real = crecimiento(x, v, desde, hasta);
      if (real !== (g[nombre] ?? null)) {
        errores.push(`el crecimiento «${nombre}» declarado (${g[nombre]}) no es el de las cifras (${real})`);
      }
    }
  }
  const difieren = x.some((_, i) => !vacio(total[i]) && !vacio(activa[i]) && total[i] !== activa[i]);
  if (difieren && !(spec.retreating_sites || []).length) {
    errores.push("las dos curvas difieren y no se nombra ninguna sede en retirada");
  }
  return errores;
}

// «clp_m»: millones de pesos, para el arancel (MAT-22).
const UNIDADES = ["count", "pct", "years", "clp_m"];

/**
 * `barras_sedes`: un eje, una barra por sede activa, con el valor nacional como referencia.
 *
 * LAS SEDES EN RETIRADA NO ENTRAN AL CUERPO (el gate del reporte local): el spec las nombra en
 * `excluded`, y si alguna aparece entre las barras, la receta se niega.
 */
function validarBarras(spec, errores) {
  if (!UNIDADES.includes(spec.unit)) errores.push(`«unit» tiene que ser una de ${UNIDADES.join(", ")}`);
  const barras = spec.bars || [];
  if (!barras.length) errores.push("no hay barras");
  const nombres = new Set();
  const fuera = new Set(spec.excluded || []);
  for (const b of barras) {
    if (!String(b.label || "").trim()) errores.push("una barra no trae «label»");
    if (nombres.has(b.label)) errores.push(`la barra «${b.label}» está repetida`);
    nombres.add(b.label);
    if (fuera.has(b.label)) errores.push(`«${b.label}» está en retirada y no puede aparecer en el cuerpo`);
    const vacio = b.value === null || b.value === undefined;
    if (!vacio && (typeof b.value !== "number" || b.value < 0)) errores.push(`«${b.label}»: el valor tiene que ser un número no negativo o null`);
    else if (!vacio && spec.unit === "pct" && b.value > 100) errores.push(`«${b.label}»: un porcentaje no puede pasar de 100`);
    if (b.n !== null && b.n !== undefined && (!Number.isInteger(b.n) || b.n < 0)) errores.push(`«${b.label}»: «n» tiene que ser un entero no negativo`);
    if (b.detail !== null && b.detail !== undefined && typeof b.detail !== "string") errores.push(`«${b.label}»: «detail» tiene que ser un texto o null`);
  }
  const ref = spec.reference;
  if (ref !== null && ref !== undefined) {
    if (!String(ref.label || "").trim() || typeof ref.value !== "number" || ref.value < 0) {
      errores.push("«reference» tiene que traer «label» y un «value» numérico no negativo, o ser null");
    }
  }
  return errores;
}

const EXTREMOS = ["p10_p90", "min_max"];

/**
 * `rangos_sedes`: una fila por sede (o por la carrera de una sede), con su distribución: extremos,
 * caja del p25 al p75 y centro. `whiskers` declara qué marcan los extremos, porque no es lo mismo un
 * p10–p90 que un mínimo–máximo.
 *
 * UNA FILA NO ROBUSTA NO TRAE CAJA: con pocos puntajes, unos percentiles fingirían una distribución que
 * el dato no sostiene (el reporte local). Si la trae, la receta se niega.
 */
function validarRangos(spec, errores) {
  if (spec.unit !== "score") errores.push("«unit» tiene que ser score");
  if (!EXTREMOS.includes(spec.whiskers)) errores.push(`«whiskers» tiene que ser una de ${EXTREMOS.join(", ")}`);
  const filas = spec.rows || [];
  if (!filas.length) errores.push("no hay filas");
  const nombres = new Set();
  const fuera = new Set(spec.excluded || []);
  const num = v => typeof v === "number" && Number.isFinite(v);
  for (const f of filas) {
    if (!String(f.label || "").trim()) errores.push("una fila no trae «label»");
    if (nombres.has(f.label)) errores.push(`la fila «${f.label}» está repetida`);
    nombres.add(f.label);
    if (fuera.has(f.label)) errores.push(`«${f.label}» está en retirada y no puede aparecer en el cuerpo`);
    if (!Number.isInteger(f.n) || f.n < 0) errores.push(`«${f.label}»: «n» tiene que ser un entero no negativo`);
    if (typeof f.robust !== "boolean") errores.push(`«${f.label}»: «robust» tiene que ser true o false`);
    if (![f.low, f.mid, f.high].every(num)) {
      errores.push(`«${f.label}»: «low», «mid» y «high» tienen que ser números`);
      continue;
    }
    const caja = [f.q1, f.q3].every(v => v !== null && v !== undefined);
    if (f.robust === false && caja) errores.push(`«${f.label}»: una fila no robusta no lleva caja («q1» y «q3» van null)`);
    if (f.robust === true && !(caja && [f.q1, f.q3].every(num))) errores.push(`«${f.label}»: una fila robusta trae «q1» y «q3»`);
    const orden = caja && [f.q1, f.q3].every(num) ? [f.low, f.q1, f.mid, f.q3, f.high] : [f.low, f.mid, f.high];
    if (orden.some((v, i) => i > 0 && v < orden[i - 1])) errores.push(`«${f.label}»: los valores no están en orden (extremo bajo ≤ caja ≤ centro ≤ caja ≤ extremo alto)`);
  }
  const ref = spec.reference;
  if (ref !== null && ref !== undefined) {
    if (!String(ref.label || "").trim() || !num(ref.value)) {
      errores.push("«reference» tiene que traer «label» y un «value» numérico, o ser null");
    }
  }
  return errores;
}

// Los colores de los tramos, en orden: azul y bermellón para dos (lo bueno y lo que se pierde), y para
// cuatro la escala del reporte local: los dos títulos en azules, seguir en ámbar, salir sin título en
// bermellón. Con su tinta, para que el número dentro del tramo se lea (blanco sobre lo oscuro).
const COLORES_TRAMOS = ["#0072B2", "#56B4E9", "#E69F00", "#D55E00"];
const TINTAS_TRAMOS = ["white", "#0f2e46", "#3d2c00", "white"];
// Los redondeos a un decimal de cada tramo pueden alejar la suma de 100 en unas décimas, no más.
const TOLERANCIA_SUMA = 1.0;
// Con dos tramos se usan los extremos de la escala —azul y bermellón—, no dos azules casi iguales.
const indicesTramos = n => (n === 2 ? [0, 3] : [...Array(n).keys()]);

function validarTramos(label, valores, claves, errores) {
  if (!valores || typeof valores !== "object" || Object.keys(valores).length !== claves.length || !claves.every(k => k in valores)) {
    errores.push(`«${label}»: «values» tiene que traer un valor por tramo (${claves.join(", ")})`);
    return;
  }
  const vs = claves.map(k => valores[k]);
  if (!vs.every(v => typeof v === "number" && Number.isFinite(v) && v >= 0)) {
    errores.push(`«${label}»: cada tramo tiene que ser un número no negativo`);
    return;
  }
  const suma = vs.reduce((a, b) => a + b, 0);
  if (Math.abs(suma - 100) > TOLERANCIA_SUMA) errores.push(`«${label}»: los tramos suman ${Math.round(suma * 10) / 10}, no 100`);
}

/**
 * `barras_partidas` (MAT-23): cada fila es una sede partida en tramos que suman 100% —convencidos y
 * desplazados, o los cuatro desenlaces de una cohorte—, con el país como última fila de referencia.
 */
function validarPartidas(spec, errores) {
  if (spec.unit !== "pct") errores.push("«unit» tiene que ser pct");
  const tramos = spec.segments || [];
  const claves = tramos.map(t => t.key);
  if (tramos.length < 2 || tramos.length > COLORES_TRAMOS.length) errores.push(`«segments» tiene que traer entre 2 y ${COLORES_TRAMOS.length} tramos`);
  if (new Set(claves).size !== claves.length || !claves.every(k => String(k || "").trim()) || !tramos.every(t => String(t.label || "").trim())) {
    errores.push("cada tramo trae «key» y «label», y las «key» no se repiten");
  }
  const filas = spec.rows || [];
  if (!filas.length) errores.push("no hay filas");
  const nombres = new Set();
  const fuera = new Set(spec.excluded || []);
  for (const f of filas) {
    if (!String(f.label || "").trim()) errores.push("una fila no trae «label»");
    if (nombres.has(f.label)) errores.push(`la fila «${f.label}» está repetida`);
    nombres.add(f.label);
    if (fuera.has(f.label)) errores.push(`«${f.label}» está en retirada y no puede aparecer en el cuerpo`);
    validarTramos(f.label, f.values, claves, errores);
    if (f.n !== null && f.n !== undefined && (!Number.isInteger(f.n) || f.n < 0)) errores.push(`«${f.label}»: «n» tiene que ser un entero no negativo`);
    if (f.detail !== null && f.detail !== undefined && typeof f.detail !== "string") errores.push(`«${f.label}»: «detail» tiene que ser un texto o null`);
  }
  const ref = spec.reference;
  if (ref !== null && ref !== undefined) {
    if (!String(ref.label || "").trim()) errores.push("«reference» tiene que traer «label», o ser null");
    validarTramos("reference", ref.values, claves, errores);
  }
  return errores;
}

// MAT-24: los ejes de una dispersión, los cuadrantes que nombra y lo mínimo para que un plano diga algo.
const UNIDADES_EJE = ["score", "pct", "clp_m"];
const CUADRANTES = ["x_above_y_above", "x_above_y_below", "x_below_y_above", "x_below_y_below"];
const MIN_EN_PLANO = 3;

/**
 * `dispersion_sedes` (MAT-24): una burbuja por sede, con dos ejes y el país como referencia en los dos.
 * Sin el país los cuadrantes no significan nada, así que la referencia es obligatoria.
 */
function validarDispersion(spec, errores) {
  for (const eje of ["x", "y"]) {
    const e = spec[eje] || {};
    if (!String(e.label || "").trim() || !UNIDADES_EJE.includes(e.unit)) errores.push(`«${eje}» tiene que traer «label» y una «unit» de ${UNIDADES_EJE.join(", ")}`);
  }
  const puntos = spec.points || [];
  if (puntos.length < MIN_EN_PLANO) errores.push(`un plano necesita al menos ${MIN_EN_PLANO} sedes`);
  const nombres = new Set();
  const fuera = new Set(spec.excluded || []);
  const num = v => typeof v === "number" && Number.isFinite(v);
  for (const p of puntos) {
    if (!String(p.label || "").trim()) errores.push("una burbuja no trae «label»");
    if (nombres.has(p.label)) errores.push(`la burbuja «${p.label}» está repetida`);
    nombres.add(p.label);
    if (fuera.has(p.label)) errores.push(`«${p.label}» está en retirada y no puede aparecer en el cuerpo`);
    for (const eje of ["x", "y"]) {
      const v = p[eje];
      if (!num(v) || v < 0) errores.push(`«${p.label}»: «${eje}» tiene que ser un número no negativo`);
      else if ((spec[eje] || {}).unit === "pct" && v > 100) errores.push(`«${p.label}»: un porcentaje no puede pasar de 100`);
    }
    if (!Number.isInteger(p.size) || p.size < 0) errores.push(`«${p.label}»: «size» tiene que ser un entero no negativo`);
  }
  const ref = spec.reference;
  if (!ref || typeof ref !== "object" || !num(ref.x) || !num(ref.y) || !String(ref.label || "").trim()) {
    errores.push("«reference» tiene que traer «label», «x» e «y»: sin el país los cuadrantes no significan nada");
  }
  const q = Object.keys(spec.quadrant_labels || {});
  if (q.length !== CUADRANTES.length || !CUADRANTES.every(k => q.includes(k))) {
    errores.push(`«quadrant_labels» tiene que nombrar los cuatro cuadrantes (${CUADRANTES.join(", ")})`);
  }
  return errores;
}

const VALIDADORES = { matricula_series: validarSeries, matricula_region: validarRegion, barras_sedes: validarBarras,
                      rangos_sedes: validarRangos, barras_partidas: validarPartidas, dispersion_sedes: validarDispersion };

// ── el dibujo ───────────────────────────────────────────────────────────────────────────────────
const tono = nombre => getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();

function filas(series) {
  // Los null se CONSERVAN: Plot corta la línea donde falta el dato. Filtrarlos la uniría.
  return series.flatMap((serie, i) =>
    (serie.points || []).map(p => ({ year: p.year, value: p.value ?? null, serie: serie.label, i })));
}

function matriculaSeries(spec, Plot, ancho) {
  const activas = (spec.series || []).filter(s => !s.retreating);
  const { saltos } = exigencias({ ...spec, series: activas });
  const esSalto = d => saltos.some(s => s.series === d.serie && s.year === d.year);
  const datos = filas(activas);
  const conDato = datos.filter(d => d.value !== null);
  const marcados = conDato.filter(esSalto);
  // LA LÍNEA NO PASA POR UN VALOR INCONSISTENTE. El punto se dibuja suelto, rodeado y declarado;
  // unido a sus vecinos, el salto se leería como una trayectoria —subida y derrumbe— que el
  // registro no sostiene. Para la línea, ese año cuenta como hueco.
  const linea = datos.map(d => (esSalto(d) ? { ...d, value: null } : d));
  const nombres = activas.map(s => s.label);
  const desde = Math.min(...spec.x);
  const hasta = Math.max(...spec.x);
  const angosto = ancho < 520;
  const ticks = spec.x.filter(a => (a - desde) % (angosto ? 6 : 3) === 0 || a === hasta);
  const comunes = {
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px",
             fontFamily: tono("--sans") },
    x: { label: null, domain: [desde, hasta], ticks, tickFormat: v => String(v), inset: 8 },
    // Base en cero: un eje recortado por abajo convierte una variación chica en un derrumbe.
    y: { label: null, zero: true, grid: true, nice: true, tickFormat: v => Math.round(v).toLocaleString("es-CL") },
  };
  const salto = (seleccion, extra = {}) => [
    // El valor inconsistente se dibuja (se declara, no se omite) y se rodea para que no pase por dato firme.
    Plot.dot(seleccion, { x: "year", y: "value", r: 9, stroke: tono("--marca-cuadro"), strokeWidth: 1.6,
                          fill: "none", ...extra }),
    Plot.text(seleccion, { x: "year", y: "value", text: () => "inconsistente", dy: -15, fontSize: 10,
                           fill: tono("--marca-cuadro"), ...extra }),
  ];

  if (activas.length <= MAX_EN_UN_PANEL) {
    return Plot.plot({
      ...comunes,
      width: ancho, height: angosto ? 260 : 320, marginLeft: 52, marginRight: 16, marginTop: 26, marginBottom: 30,
      color: { domain: nombres, range: COLORES, legend: false },
      symbol: { domain: nombres, range: SIMBOLOS, legend: false },
      marks: [
        Plot.ruleY([0], { stroke: tono("--fig-regla") }),
        ...activas.map((serie, i) => Plot.line(linea.filter(d => d.serie === serie.label), {
          x: "year", y: "value", stroke: COLORES[i], strokeWidth: 2.2, strokeDasharray: TRAZOS[i],
        })),
        Plot.dot(conDato, { x: "year", y: "value", fill: "serie", symbol: "serie", r: angosto ? 2.8 : 3.4,
                            tip: true, title: d => `${d.serie} · ${d.year}: ${d.value.toLocaleString("es-CL")}` }),
        ...salto(marcados),
      ],
    });
  }

  // MÁS DE CINCO SERIES: UN SOLO PANEL (MAT-29). Hasta la 0.10 iba un panel por sede, y así no se veía
  // cómo se comparan: el reporte local publicado lo resolvía con el nombre al final de cada línea.
  // A diferencia de ese gráfico, las líneas son RECTAS: una curva suavizada inventa forma entre años.
  const color = nombre => COLORES_MUCHAS[nombres.indexOf(nombre) % COLORES_MUCHAS.length];
  const simbolo = nombre => SIMBOLOS[nombres.indexOf(nombre) % SIMBOLOS.length];
  // El final de cada línea: su último año con dato firme (un valor inconsistente no cuenta).
  const fin = activas.map(s => {
    const firmes = conDato.filter(d => d.serie === s.label && !esSalto(d));
    const ult = firmes[firmes.length - 1];
    return ult ? { serie: s.label, year: ult.year, value: ult.value } : null;
  }).filter(Boolean);
  const rotuladas = new Set(fin.slice().sort((a, b) => b.value - a.value).slice(0, MAX_ROTULOS).map(f => f.serie));
  const alto = angosto ? 340 : 380;
  const util = alto - 30 - 26;
  const ymax = Math.max(...conDato.map(d => d.value));
  const gap = (ymax * 1.05) * 14 / util;
  // LOS NOMBRES SE APILAN SIN ENCIMARSE, de abajo hacia arriba y conservando el orden vertical: así la
  // asociación no depende del color. Si un nombre queda lejos de su línea, un conector fino lo une.
  let base = 0;
  const rotulos = fin.filter(f => rotuladas.has(f.serie)).sort((a, b) => a.value - b.value)
    .map(f => { const ym = Math.max(f.value, base); base = ym + gap; return { ...f, ym }; });
  const largo = Math.max(...rotulos.map(r => r.serie.length), 8);
  const margen = Math.min(angosto ? Math.round(ancho * 0.42) : 260, Math.round(largo * 5.6) + 14);
  const maxCh = Math.floor((margen - 14) / 5.6);
  const corta = t => (t.length <= maxCh ? t : t.slice(0, Math.ceil((maxCh - 1) * 0.5)) + "…" + t.slice(-Math.floor((maxCh - 1) * 0.5)));
  // Un símbolo cada cuatro años sobre cada línea: la línea sola distingue por color, y eso no basta.
  const conSimbolo = conDato.filter(d => (d.year - desde) % 4 === 2 && !esSalto(d));
  return Plot.plot({
    ...comunes,
    width: ancho, height: alto, marginLeft: 52, marginRight: margen, marginTop: 26, marginBottom: 30,
    marks: [
      Plot.ruleY([0], { stroke: tono("--fig-regla") }),
      ...activas.map(s => Plot.line(linea.filter(d => d.serie === s.label), {
        x: "year", y: "value", stroke: color(s.label), strokeWidth: 1.9 })),
      ...activas.map(s => Plot.dot(conSimbolo.filter(d => d.serie === s.label), {
        x: "year", y: "value", stroke: color(s.label), symbol: () => simbolo(s.label), r: 3.4, strokeWidth: 1.6,
        fill: tono("--superficie") })),
      // Puntos invisibles con su cifra: al pasar el cursor por cualquier año, la sede y el valor.
      Plot.dot(conDato, { x: "year", y: "value", r: 4, fill: "transparent",
                          tip: true, title: d => `${d.serie} · ${d.year}: ${d.value.toLocaleString("es-CL")}` }),
      Plot.link(rotulos.filter(r => Math.abs(r.ym - r.value) > gap / 2), {
        x1: "year", y1: "value", x2: "year", y2: "ym", stroke: tono("--texto-tenue"), strokeWidth: 0.7 }),
      Plot.text(rotulos, { x: "year", y: "ym", text: r => corta(r.serie), dx: 8, textAnchor: "start",
                           fontSize: angosto ? 9 : 10, fill: r => color(r.serie),
                           stroke: tono("--superficie"), strokeWidth: 3, paintOrder: "stroke" }),
      ...salto(marcados),
    ],
  });
}

function matriculaRegion(spec, Plot, ancho) {
  const x = spec.x;
  const sumados = new Set((spec.incomplete || []).filter(c => c.series === "total" && c.treatment === "summed").map(c => c.year));
  const filas = x.map((anio, i) => ({ year: anio, total: spec.total[i] ?? null, active: spec.active[i] ?? null }));
  const angosto = ancho < 520;
  const desde = x[0], hasta = x[x.length - 1];
  const conTotal = filas.filter(f => f.total !== null);
  const banda = filas.map(f => (f.total !== null && f.active !== null ? f : { ...f, total: null, active: null }));
  const medio = banda.filter(f => f.total !== null && f.total > f.active)
    .sort((a, b) => (b.total - b.active) - (a.total - a.active))[0];
  // SIN SEDES EN RETIRADA NO HAY BANDA NI LÍNEA PUNTEADA (MAT-48): la serie de primer año de una carrera en una
  // región trae `active` igual a `total`, y dibujar las dos sería sugerir una diferencia que no existe.
  const conRetirada = (spec.retreating_sites || []).length > 0;
  return Plot.plot({
    width: ancho, height: angosto ? 260 : 320, marginLeft: 56, marginRight: 16, marginTop: 20, marginBottom: 30,
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px", fontFamily: tono("--sans") },
    x: { label: null, domain: [desde, hasta], ticks: x.filter(a => (a - desde) % (angosto ? 6 : 3) === 0 || a === hasta),
         tickFormat: v => String(v), inset: 8 },
    y: { label: null, zero: true, grid: true, nice: true, tickFormat: v => Math.round(v).toLocaleString("es-CL") },
    marks: [
      Plot.ruleY([0], { stroke: tono("--fig-regla") }),
      // LA BANDA ES LA MATRÍCULA DE LAS SEDES EN RETIRADA: entre lo activo y el total.
      ...(conRetirada ? [
        Plot.areaY(banda, { x: "year", y1: "active", y2: "total", fill: COLORES[1], fillOpacity: 0.42 }),
        Plot.line(banda, { x: "year", y: "active", stroke: COLORES[0], strokeWidth: 1.3, strokeDasharray: "3 2" }),
      ] : []),
      Plot.line(filas, { x: "year", y: "total", stroke: COLORES[0], strokeWidth: 2.4 }),
      // UN AÑO SUMADO SIN UNA SEDE VA HUECO: es una cifra, pero no una firme. El año sin total corta la línea.
      Plot.dot(conTotal, { x: "year", y: "total", r: angosto ? 3 : 3.6, stroke: COLORES[0], strokeWidth: 1.6,
                           fill: f => (sumados.has(f.year) ? tono("--superficie") : COLORES[0]),
                           tip: true, title: f => `${f.year}: ${f.total.toLocaleString("es-CL")}${sumados.has(f.year) ? " (sumado sin una sede)" : ""}` }),
      ...(medio ? [Plot.text([medio], { x: "year", y: f => (f.total + f.active) / 2, text: () => "sedes en retirada",
                                         dx: 8, textAnchor: "start", fontSize: angosto ? 9.5 : 10.5, fill: tono("--marca-cuadro"),
                                         // Un halo del color del fondo, para que el rótulo se lea sobre las líneas.
                                         stroke: tono("--superficie"), strokeWidth: 3.5, paintOrder: "stroke" })] : []),
    ],
  });
}

// Los VALORES llevan sus decimales fijos («76,0%», «$4,20 M»), como los escriben las lecturas; el EJE
// los suprime cuando sobran («50%», «$2 M»): en una marca redonda, «$2,00 M» es ruido (MAT-22).
function formatoUnidad(unidad, eje = false) {
  const dec = (v, n) => v.toLocaleString("es-CL", { minimumFractionDigits: eje ? 0 : n, maximumFractionDigits: n });
  if (unidad === "clp_m") return v => `$${dec(v, 2)} M`;
  if (unidad === "pct") return v => `${dec(v, 1)}%`;
  if (unidad === "years") return v => v.toLocaleString("es-CL", { maximumFractionDigits: 1 });
  return v => Math.round(v).toLocaleString("es-CL");
}

/** Las barras que se dibujan: con dato, y sin las que valen cero si son la gran mayoría. */
function barrasVisibles(spec) {
  const conDato = (spec.bars || []).filter(b => b.value !== null && b.value !== undefined);
  const ceros = conDato.filter(b => b.value === 0).length;
  const ocultar = conDato.length > 0 && ceros / conDato.length > 0.7;
  return { filas: (ocultar ? conDato.filter(b => b.value !== 0) : conDato).sort((a, b) => b.value - a.value), ocultas: ocultar ? ceros : 0 };
}

function barrasSedes(spec, Plot, ancho) {
  const { filas } = barrasVisibles(spec);
  // TODAS EN CERO: no hay barras, y un eje vacío con la referencia sola no dice nada. El pie lo explica.
  if (!filas.length) return document.createElement("div");
  const fmt = formatoUnidad(spec.unit);
  const fmtEje = formatoUnidad(spec.unit, true);
  const angosto = ancho < 520;
  const ref = spec.reference;
  // El detalle de una barra (las personas, o el % de colegio pagado de una universidad) va en gris al
  // final de la fila, alineado: el valor de la barra sigue siendo lo que se compara (MAT-20).
  const conDetalle = filas.some(f => f.detail);
  // El detalle va FUERA del área de las barras, en su propio margen: dentro, chocaba con el valor de la
  // barra más larga («15,2%pagado 54,4%»).
  const tope = Math.max(...filas.map(f => f.value), ref ? ref.value : 0, 0) * 1.18 || 1;
  const margenDerecho = conDetalle ? (angosto ? 92 : 112) : 50;
  const margen = Math.min(angosto ? 150 : 210, Math.round(ancho * 0.42));
  return Plot.plot({
    width: ancho, height: 40 + Math.max(filas.length, 1) * (angosto ? 26 : 28), marginLeft: margen, marginRight: margenDerecho,
    marginTop: ref ? 22 : 8, marginBottom: 24,
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px", fontFamily: tono("--sans") },
    x: { label: null, domain: [0, tope], grid: true, ticks: angosto ? 3 : 5, tickFormat: fmtEje },
    y: { label: null, domain: filas.map(f => f.label), tickFormat: t => (t.length > 34 ? t.slice(0, 33) + "…" : t) },
    marks: [
      Plot.barX(filas, { x: "value", y: "label", fill: COLORES[0], fillOpacity: 0.85, insetTop: 4, insetBottom: 4,
                         tip: true, title: f => `${f.label}: ${fmt(f.value)}${f.n != null ? ` (n=${f.n.toLocaleString("es-CL")})` : ""}` }),
      Plot.ruleX([0], { stroke: tono("--fig-regla") }),
      ...(conDetalle ? [Plot.text(filas.filter(f => f.detail), { x: tope, y: "label", text: "detail", textAnchor: "start", dx: 10,
                                                                  fontSize: angosto ? 8.5 : 9.5, fill: tono("--texto-tenue") })] : []),
      // EL VALOR NACIONAL ES LA REFERENCIA, no la mediana entre sedes (como en el reporte local).
      ...(ref ? [Plot.ruleX([ref.value], { stroke: COLORES[1], strokeWidth: 1.6, strokeDasharray: "4 3" }),
                 Plot.text([ref], { x: "value", text: r => `${r.label} ${fmt(r.value)}`, frameAnchor: "top", dy: -14,
                                    fontSize: 10, fill: tono("--marca-cuadro") })] : []),
      // El valor, DESPUÉS de la referencia: si no, la línea punteada se pinta encima del halo y tacha el
      // rótulo de las barras que terminan cerca del nacional (MAT-22, el arancel).
      Plot.text(filas, { x: "value", y: "label", text: f => fmt(f.value), dx: 5, textAnchor: "start", fontSize: angosto ? 9.5 : 10.5,
                         fill: tono("--texto"), stroke: tono("--superficie"), strokeWidth: 3, paintOrder: "stroke" }),
    ],
  });
}

/** Las filas de `rangos_sedes`, de mayor a menor centro, con su rótulo: la sede y, si la hay, la carrera. */
function filasRangos(spec) {
  return (spec.rows || []).map(f => ({ ...f, eti: f.detail ? `${f.label} — ${f.detail}` : f.label }))
    .sort((a, b) => b.mid - a.mid);
}

function rangosSedes(spec, Plot, ancho) {
  const filas = filasRangos(spec);
  const angosto = ancho < 520;
  const ref = spec.reference;
  // UN DECIMAL, NO ENTERO: el dato es 674,5 y la lectura lo cita de la figura. Mostrado como «675», el
  // guardia de cifras lo rechazaría, porque no acepta el redondeo a entero de un valor con decimales.
  // El valor lleva siempre su decimal («609,0», como lo escribe la lectura); el eje, sólo si hace falta («600»).
  // La misma regla que las barras (MAT-22): un «609» junto a «567,3» parecía otra precisión (qa/, MAT-32).
  const fmt = v => v.toLocaleString("es-CL", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const fmtEje = v => v.toLocaleString("es-CL", { maximumFractionDigits: 1 });
  const halo = { stroke: tono("--superficie"), strokeWidth: 3, paintOrder: "stroke" };
  const largo = Math.max(...filas.map(f => f.eti.length));
  const margen = Math.min(angosto ? Math.round(ancho * 0.52) : 300, Math.round(largo * 5.6) + 14);
  const maxCh = Math.floor((margen - 14) / 5.6);
  // Lo que no cabe se acorta AL MEDIO: el final distingue («ingeniería civil en obras civiles»). Y LA
  // INSTITUCIÓN SE CONSERVA, que es la identidad de la fila: se acorta la carrera (el reporte local; en
  // un teléfono, «Pontificia U.... medicina» ya no decía de qué institución era).
  const medio = (t, n) => (t.length <= n ? t : t.slice(0, Math.ceil((n - 1) * 0.5)) + "…" + t.slice(-Math.floor((n - 1) * 0.5)));
  const acorta = t => {
    if (t.length <= maxCh) return t;
    const i = t.indexOf(" — ");
    if (i < 0) return medio(t, maxCh);
    const inst = t.slice(0, i), carr = t.slice(i + 3);
    // La carrera corta va entera («medicina»); una larga cede hasta un tercio. La institución, el resto.
    const paraCarrera = Math.min(carr.length, Math.max(9, Math.floor(maxCh * 0.34)));
    return medio(inst, maxCh - 3 - paraCarrera) + " — " + medio(carr, paraCarrera);
  };
  const robustas = filas.filter(f => f.robust);
  const sueltas = filas.filter(f => !f.robust);
  const bajo = Math.min(...filas.map(f => f.low), ref ? ref.value : Infinity);
  const alto = Math.max(...filas.map(f => f.high), ref ? ref.value : -Infinity);
  const color = COLORES[0];
  return Plot.plot({
    width: ancho, height: 44 + filas.length * (angosto ? 32 : 34), marginLeft: margen, marginRight: spec.whiskers === "min_max" ? 64 : 40,
    marginTop: ref ? 24 : 10, marginBottom: 24,
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px", fontFamily: tono("--sans") },
    x: { label: null, domain: [bajo - 20, alto + 20], grid: true, ticks: angosto ? 3 : 6, tickFormat: fmtEje },
    y: { label: null, domain: filas.map(f => f.eti), tickFormat: acorta },
    marks: [
      // DOS BIGOTES, NO UNA LÍNEA QUE CRUZA LA CAJA (el reporte local lo corrigió dos veces).
      Plot.ruleY(robustas, { y: "eti", x1: "low", x2: "q1", stroke: color, strokeWidth: 1.5 }),
      Plot.ruleY(robustas, { y: "eti", x1: "q3", x2: "high", stroke: color, strokeWidth: 1.5 }),
      // Sin caja, la línea sí va completa.
      Plot.ruleY(sueltas, { y: "eti", x1: "low", x2: "high", stroke: color, strokeWidth: 1.5, strokeOpacity: 0.6 }),
      Plot.tickX(filas, { x: "low", y: "eti", stroke: color, strokeWidth: 1.5, insetTop: 11, insetBottom: 11 }),
      Plot.tickX(filas, { x: "high", y: "eti", stroke: color, strokeWidth: 1.5, insetTop: 11, insetBottom: 11 }),
      Plot.barX(robustas, { y: "eti", x1: "q1", x2: "q3", fill: color, fillOpacity: 0.22, stroke: color, strokeWidth: 1.3,
                            insetTop: 10, insetBottom: 10 }),
      // El centro sobresale de la caja: se distingue del borde sin otro color.
      Plot.tickX(filas, { x: "mid", y: "eti", stroke: color, strokeWidth: 2.6, insetTop: 7, insetBottom: 7,
                          tip: true, title: f => `${f.eti}: ${fmt(f.mid)} (n=${f.n.toLocaleString("es-CL")})` }),
      // Con halo: la mediana cae a menudo sobre la línea de la referencia.
      Plot.text(filas, { x: "mid", y: "eti", text: f => fmt(f.mid), dy: -13, fontSize: 9, fill: tono("--texto-tenue"), ...halo }),
      ...(spec.whiskers === "min_max"
        ? [Plot.text(filas, { x: "high", y: "eti", dx: 8, textAnchor: "start", fontSize: 8.5, fill: tono("--texto-tenue"), ...halo,
                              text: f => `n=${f.n.toLocaleString("es-CL")}${f.robust ? "" : " ~"}` })]
        : []),
      ...(ref ? [Plot.ruleX([ref.value], { stroke: COLORES[1], strokeWidth: 1.6, strokeDasharray: "4 3" }),
                 Plot.text([ref], { x: "value", text: r => `${r.label} ${fmt(r.value)}`, frameAnchor: "top", dy: -16,
                                    fontSize: 10, fill: tono("--marca-cuadro"), ...halo })] : []),
    ],
  });
}

/**
 * `barras_partidas`: una barra al 100% por fila, partida en sus tramos, en el orden del spec. El país va
 * al pie, separado por un espacio, para que se lea como referencia y no como una sede más.
 *
 * EL TEXTO SE APILA CON LA MISMA TRANSFORMACIÓN QUE LAS BARRAS (reporte local): filtrar los tramos chicos
 * antes de apilar corre los rótulos; el filtro va en `text`, como cadena vacía.
 */
function barrasPartidas(spec, Plot, ancho) {
  const angosto = ancho < 520;
  const tramos = spec.segments;
  const fmt = v => `${v.toLocaleString("es-CL", { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;
  const ref = spec.reference;
  const SEP = "\u2003";  // la fila vacía que separa al país de las sedes
  const filas = [...spec.rows, ...(ref ? [{ label: SEP, values: null }, { ...ref, esRef: true }] : [])];
  const dominio = filas.map(f => f.label);
  const apilado = filas.filter(f => f.values).flatMap(f => tramos.map((t, j) => (
    { label: f.label, tramo: t.label, i: indicesTramos(tramos.length)[j], v: f.values[t.key], esRef: !!f.esRef, n: f.n })));
  // EL DETALLE VA A LA DERECHA EN ESCRITORIO Y SOBRE LA BARRA EN PANTALLA ANGOSTA: a la derecha no cabe, y
  // escondiéndolo la nota del pie hablaba de un rótulo que no se veía (revisado en el navegador, 09-10).
  const conDetalle = spec.rows.some(f => f.detail);
  const arriba = conDetalle && angosto;
  const margen = Math.min(angosto ? 150 : 210, Math.round(ancho * 0.42));
  const minimo = angosto ? 12 : 8;   // un tramo más angosto que esto no lleva número dentro
  const orden = tramos.map(t => t.label);
  return Plot.plot({
    width: ancho, height: 30 + filas.length * (arriba ? 40 : angosto ? 26 : 28), marginLeft: margen,
    marginRight: conDetalle && !angosto ? 200 : 16, marginTop: arriba ? 16 : 8, marginBottom: 26,
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px", fontFamily: tono("--sans") },
    x: { label: null, domain: [0, 100], grid: true, ticks: angosto ? 3 : 5, tickFormat: v => `${v}%` },
    y: { label: null, domain: dominio, tickFormat: t => (t.length > 34 ? t.slice(0, 33) + "…" : t) },
    color: { domain: orden, range: indicesTramos(tramos.length).map(i => COLORES_TRAMOS[i]) },
    marks: [
      Plot.barX(apilado, { y: "label", x: "v", fill: "tramo", order: orden, insetTop: arriba ? 10 : 4, insetBottom: arriba ? 4 : 4,
                           fillOpacity: d => (d.esRef ? 0.6 : 0.92),
                           tip: true, title: d => `${d.label}\n${d.tramo}: ${fmt(d.v)}${d.n != null ? ` (n=${d.n.toLocaleString("es-CL")})` : ""}` }),
      Plot.text(apilado, Plot.stackX({ y: "label", x: "v", z: "tramo", order: orden,
                                       fill: d => TINTAS_TRAMOS[d.i], fontSize: angosto ? 9 : 9.5, fontWeight: "bold",
                                       text: d => (d.v >= minimo ? fmt(d.v) : "") })),
      ...(conDetalle ? [Plot.text(spec.rows.filter(f => f.detail), arriba
        ? { y: "label", x: () => 0, text: "detail", dy: -14, textAnchor: "start", fontSize: 8.5, fill: tono("--texto-tenue") }
        : { y: "label", x: () => 100, text: "detail", dx: 8, textAnchor: "start", fontSize: 9, fill: tono("--texto-tenue") })] : []),
      Plot.ruleX([0], { stroke: tono("--fig-regla") }),
    ],
  });
}

/**
 * `dispersion_sedes`: una burbuja por sede (área = entrantes), con las líneas del país partiendo el plano.
 *
 * SE ROTULAN HASTA 15 SEDES, LAS DE MÁS ENTRANTES (decisión del 09-10): con treinta en la Metropolitana los
 * nombres se tapan. Las demás van sin nombre, y TODAS muestran su ficha al pasar el cursor. El nombre de cada cuadrante
 * va en el pie y no en el gráfico: en las esquinas tapaba a las sedes que caen justo ahí (revisado en el navegador).
 */
function dispersionSedes(spec, Plot, ancho) {
  const angosto = ancho < 520;
  const fmtDe = (u, eje) => v => (u === "clp_m" ? `$${v.toLocaleString("es-CL", { minimumFractionDigits: eje ? 0 : 2, maximumFractionDigits: 2 })} M`
    : u === "pct" ? `${v.toLocaleString("es-CL", { minimumFractionDigits: eje ? 0 : 1, maximumFractionDigits: 1 })}%`
    : v.toLocaleString("es-CL", { minimumFractionDigits: eje ? 0 : 1, maximumFractionDigits: 1 }));
  const fx = fmtDe(spec.x.unit), fy = fmtDe(spec.y.unit);
  const ref = spec.reference;
  const puntos = [...spec.points].sort((a, b) => b.size - a.size);
  const halo = { stroke: tono("--superficie"), strokeWidth: 3, paintOrder: "stroke" };
  const xs = [...puntos.map(p => p.x), ref.x], ys = [...puntos.map(p => p.y), ref.y];
  const holgura = (vs, f) => { const a = Math.min(...vs), b = Math.max(...vs), h = (b - a) * f || 1; return [a - h, b + h]; };
  const alto = Math.min(440, Math.round(ancho * 0.66) + 60);
  const m = { l: 56, r: 24, t: 30, b: 44 };
  const dx = holgura(xs, 0.12), dy = holgura(ys, 0.15);
  const corto = p => (p.label.length > 30 ? p.label.slice(0, 29) + "…" : p.label);
  const letra = angosto ? 8.5 : 9.5;
  // DE LAS 15 MÁS GRANDES, SE ROTULA LA QUE CABE: un nombre que tapa a otro ya puesto queda sin rótulo y se ve al
  // pasar el cursor (en la Metropolitana, quince nombres en el mismo rincón eran ilegibles). Las cajas se estiman
  // con las mismas escalas que usa Plot; el ancho de una letra, como 0,56 del cuerpo.
  const puestas = [];
  const rotuladas = new Set();
  for (const p of puntos.slice(0, MAX_ROTULOS)) {
    const cx = m.l + (p.x - dx[0]) / (dx[1] - dx[0]) * (ancho - m.l - m.r);
    const cy = alto - m.b - (p.y - dy[0]) / (dy[1] - dy[0]) * (alto - m.t - m.b) - 12;
    const w = corto(p).length * letra * 0.56, h = letra + 2;
    const caja = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2];
    if (puestas.some(o => caja[0] < o[2] && o[0] < caja[2] && caja[1] < o[3] && o[1] < caja[3])) continue;
    puestas.push(caja);
    rotuladas.add(p.label);
  }
  return Plot.plot({
    width: ancho, height: alto, marginLeft: m.l, marginRight: m.r, marginTop: m.t, marginBottom: m.b,
    style: { background: "transparent", color: tono("--texto-suave"), fontSize: angosto ? "10px" : "11px", fontFamily: tono("--sans") },
    x: { label: `${spec.x.label} →`, domain: dx, grid: true, ticks: angosto ? 4 : 6, tickFormat: fmtDe(spec.x.unit, true) },
    y: { label: `↑ ${spec.y.label}`, domain: dy, grid: true, ticks: 5, tickFormat: fmtDe(spec.y.unit, true) },
    r: { range: [4, angosto ? 16 : 22] },
    marks: [
      Plot.ruleX([ref.x], { stroke: COLORES[1], strokeWidth: 1.4, strokeDasharray: "4 3" }),
      Plot.ruleY([ref.y], { stroke: COLORES[1], strokeWidth: 1.4, strokeDasharray: "4 3" }),
      Plot.text([ref], { x: "x", text: r => `${r.label} ${fx(r.x)}`, frameAnchor: "top", dy: -14, fontSize: 9.5, fill: tono("--marca-cuadro") }),
      Plot.text([ref], { y: "y", text: r => `${r.label} ${fy(r.y)}`, frameAnchor: "right", textAnchor: "end", dy: -7, fontSize: 9.5,
        fill: tono("--marca-cuadro"), ...halo }),
      Plot.dot(puntos, { x: "x", y: "y", r: "size", fill: COLORES[0], fillOpacity: 0.45, stroke: COLORES[0], strokeWidth: 1.2,
        channels: { sede: "label", [spec.x.label]: d => fx(d.x), [spec.y.label]: d => fy(d.y),
                    [spec.size_label || "tamaño"]: d => d.size.toLocaleString("es-CL") },
        tip: { format: { x: false, y: false, r: false } } }),
      Plot.text(puntos.filter(p => rotuladas.has(p.label)), { x: "x", y: "y", text: corto,
        dy: -12, fontSize: letra, fill: tono("--texto"), ...halo }),
    ],
  });
}

/** La leyenda, en HTML: con muestra de color, trazo y forma, para que no dependa del color. */
// LOS TOOLTIPS SON LOS DE PLOT (`tip: true` sobre el `title` de cada marca), no el `title` nativo del navegador: el
// iframe de los widgets no muestra el nativo, y Plot dibuja el suyo dentro del gráfico en cualquier cliente (MAT-39).
function leyenda(spec) {
  if (spec.form === "matricula_region") return leyendaRegion(spec);
  if (spec.form === "barras_partidas") return leyendaPartidas(spec);
  if (spec.form === "barras_sedes" || spec.form === "rangos_sedes" || spec.form === "dispersion_sedes") return null;
  const activas = (spec.series || []).filter(s => !s.retreating);
  if (activas.length < 2 || activas.length > MAX_EN_UN_PANEL) return null;
  const caja = document.createElement("div");
  caja.className = "leyenda";
  const formas = {
    circle: '<circle cx="18" cy="6" r="3.6"/>', square: '<rect x="14.5" y="2.5" width="7" height="7"/>',
    triangle: '<path d="M18 2 L22 10 L14 10 Z"/>', diamond: '<path d="M18 1.5 L22.5 6 L18 10.5 L13.5 6 Z"/>',
    cross: '<path d="M16.5 2h3v2.5H22v3h-2.5V10h-3V7.5H14v-3h2.5z"/>',
  };
  activas.forEach((serie, i) => {
    const item = document.createElement("span");
    const trazo = TRAZOS[i] ? ` stroke-dasharray="${TRAZOS[i]}"` : "";
    item.innerHTML = `<svg width="36" height="12" aria-hidden="true"><line x1="0" y1="6" x2="36" y2="6" ` +
      `stroke="${COLORES[i]}" stroke-width="2.2"${trazo}/><g fill="${COLORES[i]}">${formas[SIMBOLOS[i]]}</g></svg>`;
    item.append(document.createTextNode(serie.label));
    caja.append(item);
  });
  return caja;
}

// Los tramos en su orden de izquierda a derecha: la posición, además del color, dice cuál es cuál.
function leyendaPartidas(spec) {
  const caja = document.createElement("div");
  caja.className = "leyenda";
  spec.segments.forEach((t, i) => {
    const item = document.createElement("span");
    item.innerHTML = `<svg width="14" height="12" aria-hidden="true"><rect x="0" y="1" width="14" height="10" fill="${COLORES_TRAMOS[indicesTramos(spec.segments.length)[i]]}"/></svg>`;
    item.append(document.createTextNode(`${i + 1}. ${t.label}`));
    caja.append(item);
  });
  return caja;
}

function leyendaRegion(spec) {
  const caja = document.createElement("div");
  caja.className = "leyenda";
  const items = [
    [`<line x1="0" y1="6" x2="36" y2="6" stroke="${COLORES[0]}" stroke-width="2.4"/><circle cx="18" cy="6" r="3.4" fill="${COLORES[0]}"/>`, "todas las sedes"],
  ];
  if ((spec.retreating_sites || []).length) {
    items.push([`<rect x="0" y="1" width="36" height="10" fill="${COLORES[1]}" fill-opacity="0.42"/>`, "sedes en retirada"],
               [`<line x1="0" y1="6" x2="36" y2="6" stroke="${COLORES[0]}" stroke-width="1.3" stroke-dasharray="3 2"/>`, "sin las sedes en retirada"]);
  }
  if ((spec.incomplete || []).some(c => c.series === "total" && c.treatment === "summed")) {
    items.push([`<circle cx="18" cy="6" r="3.4" fill="none" stroke="${COLORES[0]}" stroke-width="1.6"/>`, "año sumado sin una sede"]);
  }
  for (const [svg, texto] of items) {
    const item = document.createElement("span");
    item.innerHTML = `<svg width="36" height="12" aria-hidden="true">${svg}</svg>`;
    item.append(document.createTextNode(texto));
    caja.append(item);
  }
  return caja;
}

const FORMAS = { matricula_series: matriculaSeries, matricula_region: matriculaRegion, barras_sedes: barrasSedes,
                 rangos_sedes: rangosSedes, barras_partidas: barrasPartidas, dispersion_sedes: dispersionSedes };

/** Dibuja una figura en el ancho dado, o se niega. */
function dibujar(spec, ancho = 720) {
  const errores = validar(spec);
  if (errores.length) {
    throw new Error(`no se dibuja (${errores.join("; ")}); se entrega la tabla en su lugar`);
  }
  const Plot = globalThis.Plot;
  return escalable(FORMAS[spec.form](spec, Plot, Math.max(300, Math.round(ancho))));
}

/**
 * Plot emite `width` y `height` pero no `viewBox`, y sin viewBox un `height:auto` resuelve a cero:
 * el gráfico existe y ocupa cero píxeles. Se deriva el viewBox para que escale sin deformarse.
 */
function escalable(nodo) {
  const graficos = nodo.tagName === "svg" ? [nodo] : nodo.querySelectorAll("svg");
  for (const svg of graficos) {
    const ancho = Number(svg.getAttribute("width"));
    const alto = Number(svg.getAttribute("height"));
    if (!ancho || !alto || svg.getAttribute("viewBox")) continue;
    if (ancho < 80 || svg.closest("[class*=swatch]")) continue;
    svg.setAttribute("viewBox", `0 0 ${ancho} ${alto}`);
    svg.setAttribute("preserveAspectRatio", "xMinYMin meet");
    svg.removeAttribute("width");
    svg.style.width = "100%";
    svg.style.height = "auto";
  }
  return nodo;
}

if (typeof module !== "undefined") module.exports = { validar, exigencias, crecimiento, barrasVisibles, FACTOR_DE_SALTO, MAX_EN_UN_PANEL, MAX_ROTULOS };
