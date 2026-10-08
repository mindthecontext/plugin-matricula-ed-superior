---
description: Responde sobre el mercado universitario de una región chilena — «¿cómo está el mercado en La Araucanía?», «¿quién crece y quién se estanca?», «¿cuántos egresados se quedan a estudiar acá?», «¿hacia dónde se van los que salen?», «¿cómo le va a esta universidad frente a sus competidores?». Cubre universidades. NO responde sobre una carrera específica en el sistema completo: para eso está explorar-una-carrera.
---

# Analizar una región

## El orden

1. **`panorama_region`** para el cuadro: participación, evolución, selectividad y equidad por sede.
2. **`flujos_region`** y **`perfil_migrante`** si la pregunta es de retención o migración.
3. **`ficha_sede`** cuando la pregunta sea por UNA sede: todos sus ejes con su n, su serie de matrícula
   desde 2007, origen por vía, gratuidad y desenlaces de cohorte.
4. **`vista_institucion`** cuando la pregunta sea por una casa multi-sede: integra sus sedes y da su
   posición en cada mercado.
5. **`preferencias`** para competencia revelada; **`acceso_equidad`** para gratuidad y PACE;
   **`carreras_tope`** para las carreras de mayor exigencia PAES de cada sede.

## La evolución de la región: con y sin las sedes en retirada

`panorama_region` trae `matricula_region` con la serie regional y su crecimiento **con todas las sedes
y sin las en retirada**. Las dos cifras son correctas y responden cosas distintas: cuánto cambió la
matrícula de la región, y cuánto creció el mercado que sigue compitiendo. Si das una, di cuál es.
Y lee `avisos` antes de dar el número: un año puede venir sin total, o sumado sin una sede, y eso se
dice.

**En retirada no es lo mismo que chica.** Una sede con `en_retirada` ya casi no recibe estudiantes
nuevos y no entra en comparaciones. Una con `nota` de muestra chica sigue compitiendo: se compara,
sin lecturas fuertes sobre ella.

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
- **Las sedes en retirada no entran a los rankings**: llegan con `en_retirada` y su razón.
- **Nada de comparar puntajes cruzando 2022/2023** — quiebre PSU→PAES.

## Dos cifras que parecen contradictorias y no lo son

La *permanencia territorial* («de los egresados de la región, cuántos estudian acá») y la
*composición local de una sede* («de quienes entran a esta sede, cuántos egresaron acá») son
condicionales inversas. Pueden dar 78% y 92% a la vez sin contradicción. Si ambas aparecen, nombra
el denominador de cada una.

## Cierra con las fuentes

Fuente original, años y consideraciones desde `procedencia`. Y si en la misma respuesta usaste la
puerta por carrera, explica por qué los universos difieren.
