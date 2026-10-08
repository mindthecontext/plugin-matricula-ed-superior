// Recetas de visualización del saber Matrícula de Educación Superior. Hoy hay una forma:
// `matricula_series`, la serie de matrícula de una o varias sedes.
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
  const errores = [];
  if (!spec || spec.form !== "matricula_series") {
    errores.push(`la forma «${spec && spec.form}» no está implementada; hoy existe matricula_series`);
    return errores;
  }
  for (const campo of ["title", "subtitle"]) {
    if (!String(spec[campo] || "").trim()) errores.push(`falta «${campo}»`);
  }
  // LA FUENTE NO SE ESCRIBE: se estampa desde la procedencia que entregó la herramienta.
  if ("source" in spec) errores.push("el spec trae «source»: la fuente no se escribe, se deriva de «provenance»");
  if (!spec.provenance || !String(spec.provenance.fuente_original || "").trim()) {
    errores.push("falta «provenance.fuente_original»: cópiala tal cual de la herramienta");
  }
  const x = spec.x || [];
  if (!x.length || x.some((v, i) => !Number.isInteger(v) || (i > 0 && v <= x[i - 1]))) {
    errores.push("«x» tiene que ser una lista de años enteros, creciente y sin repetir");
  }
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
                            title: d => `${d.serie} · ${d.year}: ${d.value.toLocaleString("es-CL")}` }),
        ...salto(marcados),
      ],
    });
  }

  // Más de cinco series: un panel por sede, con el MISMO eje, para que las alturas se comparen.
  return Plot.plot({
    ...comunes,
    width: ancho, height: activas.length * (angosto ? 92 : 104) + 30,
    marginLeft: 52, marginRight: 16, marginTop: 10, marginBottom: 30,
    fy: { label: null, domain: nombres, axis: null },
    marks: [
      Plot.frame({ stroke: tono("--regla") }),
      Plot.text(nombres, { fy: d => d, text: d => d, frameAnchor: "top-left", dx: 6, dy: 6,
                           fontSize: 10.5, fill: tono("--texto") }),
      Plot.line(linea, { x: "year", y: "value", fy: "serie", stroke: COLORES[0], strokeWidth: 2 }),
      Plot.dot(conDato, { x: "year", y: "value", fy: "serie", fill: COLORES[0], r: 2.4,
                          title: d => `${d.serie} · ${d.year}: ${d.value.toLocaleString("es-CL")}` }),
      ...salto(marcados, { fy: "serie" }),
    ],
  });
}

/** La leyenda, en HTML: con muestra de color, trazo y forma, para que no dependa del color. */
function leyenda(spec) {
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

const FORMAS = { matricula_series: matriculaSeries };

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

if (typeof module !== "undefined") module.exports = { validar, exigencias, FACTOR_DE_SALTO, MAX_EN_UN_PANEL };
