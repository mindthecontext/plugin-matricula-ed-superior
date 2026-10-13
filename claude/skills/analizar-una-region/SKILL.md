---
description: Responde sobre el mercado universitario de una región chilena — «¿cómo está el mercado en La Araucanía?», «¿quién crece y quién se estanca?», «¿cuántos egresados se quedan a estudiar acá?», «¿hacia dónde se van los que salen?», «¿cómo le va a esta universidad frente a sus competidores?». Cubre universidades. NO responde sobre una carrera específica en el sistema completo: para eso está explorar-una-carrera.
---

# Analizar una región

## El orden

1. **`panorama_region`** para el cuadro: participación, evolución, selectividad y equidad por sede.
2. **`flujos_region`** y **`perfil_migrante`** si la pregunta es de retención o migración.
3. **`ficha_sede`** cuando la pregunta sea por UNA sede: todos sus ejes con su n, su serie de matrícula
   desde 2007, origen por vía, gratuidad y desenlaces de cohorte.
4. **`vista_institucion`** cuando la pregunta sea por una universidad multi-sede: integra sus sedes y da su
   posición en cada mercado. Para un **instituto profesional o un CFT** no sirve —esta puerta es sólo de
   universidades—: usa `presencia_institucional`, que los mira carrera por carrera.
5. **`preferencias`** para competencia revelada; **`acceso_equidad`** para gratuidad y PACE;
   **`carreras_tope`** para las carreras de mayor exigencia PAES de cada sede.

## La evolución de la región: con y sin las sedes en retirada

`panorama_region` trae `matricula_region` con la serie regional y su crecimiento **con todas las sedes
y sin las en retirada**. Las dos cifras son correctas y responden cosas distintas: cuánto cambió la
matrícula de la región, y cuánto creció el mercado que sigue compitiendo. Si das una, di cuál es.
Y lee `avisos` antes de dar el número: un año puede venir sin total, o sumado sin una sede, y eso se
dice.

Si la pregunta se responde mejor con una figura, `figura_matricula_region` la entrega lista (skill
graficar-la-matricula).

**Es matrícula total, no de primer año.** La serie cuenta todos los años de la carrera. De primer año
sólo hay los entrantes acumulados de la ventana, sin serie: si piden la evolución de primer año de una
región, dilo y ofrece la total o los entrantes. Para una carrera, la serie de primer año está en
`panorama_carrera` (`evolucion`).

**En retirada no es lo mismo que chica.** Una sede con `en_retirada` ya casi no recibe estudiantes
nuevos y no entra en comparaciones. Una con `nota` de muestra chica sigue compitiendo: se compara,
sin lecturas fuertes sobre ella.

Si la pregunta es sobre un eje del reporte regional (la PAES por sede, la gratuidad, las preferencias, los
planos), `figura_region(region, figura)` entrega esa figura sola, con sus `groups`, sin pedir el reporte
completo; en claude.ai y Claude Desktop aparece dibujada en la conversación.

## El universo de esta puerta es universitario

Solo universidades, sin IP ni CFT. Si la pregunta es «¿cuánta gente estudia esto en la región?», la
respuesta universitaria **no es el total del sistema** — dilo antes de que el lector lo suponga.

## Una serie con huecos no se rellena

La serie de matrícula de una sede puede traer años sin dato (`null`) y algún valor que no calza con
sus vecinos. No interpoles sobre un hueco ni lo tapes con el año de al lado, y no construyas el
relato de la sede sobre un único valor que salta: preséntalo y di que el registro es inconsistente
en ese tramo.

## Las reglas duras del dominio

- **Los percentiles no se promedian entre sedes.** El PAES consolidado de una institución multi-sede
  llega como `no_derivable`: se entrega el rango y se explica por qué.
- **Sin superlativos que no vengan del dato.** «La más inclusiva» exige haber comparado el eje
  completo, no haber mirado dos filas.
- **Las sedes en retirada no entran a ninguna comparación**: ni rankings, ni rangos («va de X a Y»), ni
  mínimos o máximos, ni promedios. Llegan con `en_retirada` y su razón; si las nombras, que sea aparte y
  como lo que son. En qa/ (08-10) una respuesta dijo «va de 38,9% (INACAP)…» con INACAP en retirada: el
  rango real entre las sedes activas empezaba en 58,4%.
- **Cada eje trae su `n`, que es el de quienes tienen el dato**, no el de toda la sede. La cobertura de un
  eje en una sede es su `n` dividido por los entrantes de la sede, y se puede comparar entre sedes. No
  digas que «los datos no traen la cobertura»: la traen.
- **Nada de comparar puntajes cruzando 2022/2023** — quiebre PSU→PAES.

## Dos cifras que parecen contradictorias y no lo son

La *permanencia territorial* («de los egresados de la región, cuántos estudian acá») y la
*composición local de una sede* («de quienes entran a esta sede, cuántos egresaron acá») son
condicionales inversas. Pueden dar 78% y 92% a la vez sin contradicción. Si ambas aparecen, nombra
el denominador de cada una.

## Cierra con las fuentes

Fuente original, años y consideraciones desde `procedencia`. La fuente y el alcance de **cada indicador**
están en `procedencia.por_eje`: úsalos, porque no todos los indicadores salen de la misma base ni cubren
los mismos años. Y si en la misma respuesta usaste la
puerta por carrera, explica por qué los universos difieren.
