---
description: Responde sobre una carrera en el sistema de educación superior chileno — «¿cómo está Enfermería?», «¿quién dicta Psicología y con qué selectividad?», «¿dónde se estudia Kinesiología?», «¿qué empleabilidad tiene?», «¿a quién le pierde estudiantes esta universidad en esta carrera?». Cubre universidades, institutos profesionales y CFT. NO responde sobre el mercado de una región completa: para eso está analizar-una-region.
---

# Explorar una carrera

## El orden que la evidencia pide

1. **`panorama_carrera`** siempre primero. Trae `composicion_del_mercado`, que dice si la carrera es
   universitaria, mixta o de IP y CFT — y eso **cambia cómo se lee todo lo demás**.
2. Después, lo que la pregunta pida: `sedes_de_la_carrera`, `quien_entra`, `desenlaces_carrera`,
   `competencia_carrera`.
3. Ante una duda de interpretación, `obtener_criterios()`. Ante una de alcance, `preguntas_abiertas()`.

## Empieza por el tipo de mercado, no por la cifra

«Enfermería la lidera una universidad» y «Técnico en Enfermería la lidera un instituto profesional»
son dos frases del mismo saber sobre dos mundos distintos. Decir el perfil primero evita que el
lector proyecte supuestos universitarios sobre un mercado que no lo es. Quién lidera y con qué
participación sale de `panorama_carrera`, nunca de este texto.

## La cobertura va antes de la cifra

Cuando una respuesta traiga `_leer_primero` o una cobertura parcial, **el porcentaje va primero**:

> La vía de ingreso se observa para el 3% del alumnado de esta carrera —el registro de admisión
> solo cubre la vía centralizada—, y en esa fracción…

Nunca la cifra sola. Un dato que describe al 3% no puede leerse igual que uno que describe al 81%.

## Lo que no aplica no es un vacío

En IP y CFT no se entra por PAES: `selectividad` llega como `no_derivable` con su razón. **Eso es un
hallazgo, no una falla** — dice que el puntaje no es el eje que organiza ese mercado. Trasládalo así,
y ofrece el eje que sí aplica: quién capta a los primeros de su curso.

## La matriz de sustitución es lo que hay que lucir

`competencia_carrera` trae, de quienes dejaron una institución, a cuál llegaron — con n y share de
ambos lados. Es la respuesta a *«¿a quién le pierdo mis estudiantes?»* con nombre y apellido, y
captura el flujo entre tipos de institución —de una universidad a un IP— que ninguna otra capa mide.

Al presentarla, distingue el flujo **dentro del mismo tipo** del que **cruza tipos**: no es lo mismo
perder alumnado hacia una universidad par que hacia un instituto profesional.

**Y es un top-K.** Trae los flujos mayores del país, no todos. Si te preguntan por una institución
que no aparece como origen, la respuesta no es «no pierde a nadie» sino «su fuga, si existe, está
repartida en montos bajo el corte de esta matriz». Decirlo al revés invierte el hallazgo.

## El retorno laboral es de un tipo de institución: dilo

`retorno_laboral` trae la empleabilidad y los ingresos del **tipo de institución que domina la
matrícula de la carrera** (`tipo_servido`), y en `por_tipo` los tres que publica mifuturo
—universidades, institutos profesionales y CFT—, cada uno con su peso en la carrera
(`pct_matricula_de_la_carrera`).

- **Di siempre de qué tipo es la cifra.** «Al primer año, los egresados de institutos profesionales
  ganan $0,80 millones», no «los egresados ganan…».
- **Si el dominante gana por poco** (los dos primeros a menos de 10 puntos de matrícula, como IP 49%
  y CFT 45% en Técnico en Enfermería), da los dos: la cifra «de la carrera» depende de un empate.
- **No compares tipos como si fueran mejores o peores.** Un instituto profesional con más ingreso
  que una universidad puede estar recibiendo a adultos que ya trabajaban; los datos no dicen por qué.
- **No compares entre carreras de tipos distintos** sin decirlo: el ingreso de una carrera
  universitaria y el de una técnica describen poblaciones distintas.
- Si `retorno_laboral` viene como no derivable, mifuturo no publica esa carrera: dilo así.

Hasta octubre de 2026 estas cifras eran siempre las de universidades. Si alguien cita un valor
anterior, puede no coincidir.

## Una institución en todas sus carreras

Cuando la pregunta sea por una institución —«¿dónde está el CFT Santo Tomás?», «¿cómo le va al IP en sus
carreras?»—, usa `presencia_institucional`. Sirve para universidades, IP y CFT.

- **Si el nombre es de un grupo** («Santo Tomás», «INACAP»), te devuelve los candidatos: pregunta cuál
  —la universidad, el IP o el CFT— en vez de elegir.
- **El puesto sólo existe entre las cinco primeras** del mercado. Fuera de ellas no hay puesto: di que no
  está entre las cinco primeras, no inventes «sexta».
- **Cubre las 69 carreras del saber**, no toda su oferta. Dilo antes de la lista.
- **Cita sus cifras, no las de otra herramienta.** La titulación es el promedio de sus sedes ponderado por
  cohorte (`titulacion.metodo`): no la reemplaces por una mediana sacada de otra respuesta. Si la cohorte es
  chica (`n_cohortes` bajo 100), dilo junto a la cifra.
- **Los dos conteos de sedes son de periodos distintos**: `sedes_con_entrantes_2021_2025` y
  `sedes_con_cohortes_2011_2016`. Si difieren, es porque abrió o cerró sedes, no una inconsistencia.
- **`presencia: sólo en cohortes antiguas`** es una carrera que tuvo y ya no recibe entrantes: nómbrala
  aparte, no como parte de su oferta de hoy.
- **La titulación es de las cohortes 2011–2016.** El retorno laboral de la institución se compara con **su
  propio tipo** (`retorno_laboral.su_tipo`: un CFT con los CFT, un IP con los IP), no con el tipo que domina
  la carrera, que va sólo de contexto: comparar un CFT con el promedio de los IP exagera la brecha. Una brecha —más titulación y menos empleabilidad, por ejemplo— se describe, no se
  explica: puede ser quién entra a cada una. Nunca la presentes como un juicio sobre la institución.

## No inventes causas

Que quienes se van tengan otro perfil describe **quiénes** migran, no **por qué**. La misma brecha
es compatible con oferta, recursos y preferencias a la vez. Enumera las hipótesis sin escoger, y di
qué haría falta para distinguirlas.

## Cierra con las fuentes

Toda respuesta con datos cierra con fuente original, años y consideraciones, **copiados del campo
`procedencia`** — nunca redactados de memoria. Y declara el universo: esta puerta cubre la educación
superior completa, la regional solo universidades.
