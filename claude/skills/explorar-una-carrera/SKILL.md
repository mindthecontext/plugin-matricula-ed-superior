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

## Si el retorno laboral trae un aviso, el aviso va primero

Cuando `desenlaces_carrera` traiga `_aviso_vintage` en `retorno_laboral`, la empleabilidad y los
ingresos de esa respuesta pueden venir del grupo de instituciones equivocado. Dilo **antes** de la
cifra, con las palabras del aviso, y no la uses para comparar entre carreras. Si el campo no viene,
no hay nada que advertir.

## No inventes causas

Que quienes se van tengan otro perfil describe **quiénes** migran, no **por qué**. La misma brecha
es compatible con oferta, recursos y preferencias a la vez. Enumera las hipótesis sin escoger, y di
qué haría falta para distinguirlas.

## Cierra con las fuentes

Toda respuesta con datos cierra con fuente original, años y consideraciones, **copiados del campo
`procedencia`** — nunca redactados de memoria. Y declara el universo: esta puerta cubre la educación
superior completa, la regional solo universidades.
