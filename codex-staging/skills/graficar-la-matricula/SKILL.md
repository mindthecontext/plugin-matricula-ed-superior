---
name: graficar-la-matricula
description: Dibuja cómo evolucionó la matrícula universitaria, desde 2007, de una o varias sedes o de una región entera — «¿cómo ha evolucionado la matrícula de la UST en Temuco?», «grafícame la matrícula de las sedes de La Araucanía», «compara cómo crecieron estas sedes», «grafícame la matrícula de la región», «¿cuánto creció la región con y sin las sedes que cierran?». Produce una figura que se publica como página, con los huecos, los años incompletos y los valores inconsistentes declarados. NO dibuja carreras ni otros indicadores.
---

# Graficar la matrícula

Una serie de diecinueve años se lee mejor dibujada que contada. Esta skill produce **una figura**: la
matrícula total de pregrado de una o varias sedes universitarias, año a año. El servicio entrega el
**spec** con los datos; tú decides el encuadre; la receta dibuja. **Nunca escribas HTML ni código de
gráfico, y nunca armes el spec a mano.**

## 1 · Elige la forma y pide el spec al servicio

Hay **seis herramientas**, y responden preguntas distintas:

| La pregunta | La herramienta | La figura |
|---|---|---|
| cómo evolucionaron **unas sedes**, o compararlas entre sí | `figura_matricula(region, instituciones=None)` | una línea por sede, en un solo panel; con más de cinco, el nombre de cada sede va al final de su línea |
| cómo evolucionó **la región entera** | `figura_matricula_region(region)` | el total, y una banda con lo que aportaban las sedes en retirada |
| **una figura del reporte regional**, sola (la PAES por sede, el plano del precio, las preferencias…) | `figura_region(region, figura)` | la misma figura del reporte, con sus `groups`; un id que no existe trae la lista |
| cómo evolucionó la matrícula de **primer año de una carrera**, en el país o en una región | `figura_primer_anio(carrera, region=None)` | la forma de la región entera, con un solo total: los años que una sede no reportó van huecos o cortados, y se dicen |
| **quién gana y quién pierde** participación en una carrera, en el país o en una región | `figura_participacion(carrera, region=None, desde=None, hasta=None)` | una barra por institución con su participación el último año, y al lado la del primero y el cambio |
| el **técnico-profesional** de una región (IP y CFT): sus unidades en el tiempo o un eje por unidad | `figura_tecnico_region(region, figura, nivel=None, instituciones=None)` | «matricula»: una línea por institución × ciudad × nivel; un eje: una barra por unidad contra los IP y CFT del país |

`figura_matricula` sin `instituciones` trae todas las sedes de la región; con ellas, sólo esas
(`["UFRO", "católica de temuco"]`). Las dos devuelven `spec` **listo para la receta**: las cifras, los
huecos y los valores inconsistentes declarados, las sedes en retirada marcadas y la procedencia propia
de la matrícula. La regional trae además el crecimiento, con todas las sedes y sin las en retirada.

- **Guarda `spec` tal cual** en un archivo JSON, completo: sin resumirlo, sin redondear y sin copiar sus
  valores a un script. Viene firmado (`huella`) y el compositor comprueba que sea el que entregó el
  servicio.
- **Puedes cambiar `title` y `subtitle`** para que digan lo que la pregunta pide (por ejemplo, «Tres
  sedes que crecen en Temuco»). Respeta sus roles, abajo.
- **No toques `series`, `annotations`, `notices` ni `provenance`.** Si algo no te parece bien, dilo en
  el texto; no lo corrijas en el spec.

Si la herramienta responde con `error`, dilo: no armes el spec a mano.

### La serie es de matrícula total, no de primer año

Las series de `figura_matricula` y `figura_matricula_region` cuentan la **matrícula total** de pregrado:
todos los años de la carrera, no sólo quienes entran. De primer año, la puerta regional tiene los
**entrantes acumulados de la ventana** (los años los dice cada respuesta), sin serie por año, y en `figura_region` ni `serie`
ni `entrantes` son una serie de primer año.

Si piden «la evolución de la matrícula de primer año» de una región:

- **Dilo primero:** esa serie no está en el saber.
- **Ofrece lo que hay:** la serie de matrícula total, rotulada como total (no le cambies el `subtitle` a
  «primer año»), o los entrantes de la ventana.
- **Si la pregunta es por una carrera,** la serie de primer año sí existe, también en una región:
  `figura_primer_anio(carrera, region)` (CNED, desde 2005). Si la pregunta por la región admite leerse por una
  carrera, ofrécela.

Cada respuesta de figura trae `sobre_primer_anio` con estas mismas palabras.

## 2 · El encuadre: los roles de los textos

El formato completo está en `references/spec.md`. El servicio ya trae un título y un subtítulo
correctos; si los cambias, respeta sus roles:

- **`title`** nombra la vista, no el hallazgo: «La matrícula de las sedes universitarias de La
  Araucanía», no «La UFRO lidera».
- **`subtitle`** dice unidad, universo y ventana: «matrícula total de pregrado por sede, universidades,
  2007–2026».
- **No agregues `source`**: la fuente se estampa sola desde `provenance`, y si la escribes, la figura
  se niega.

Las sedes en retirada vienen con `"retreating": true`: no se dibujan y se nombran al pie. Si pides sólo
sedes en retirada, se dibujan y la marca va en `notices`.

## 3 · Lo que la serie no dice sola ya viene declarado

El servicio lo anota con las mismas reglas con que la receta lo exige, así que normalmente no tienes
que hacer nada. Para que sepas qué es:

- **Un hueco** —un `null` entre el primer y el último dato de una serie— exige una anotación
  `kind: "gap"` con su nota: por ejemplo, «sin registro en la fuente».
- **Un valor inconsistente** —el triple o un tercio de sus dos vecinos con dato— exige
  `kind: "inconsistent"`: por ejemplo, «el registro es inconsistente en este tramo». Se dibuja suelto y
  rodeado, sin unirlo a la línea. **No lo borres ni lo corrijas**: se declara.

Si alguna vez la receta se niega, es que el spec se tocó donde no debía: vuelve a pedirlo.

## 3b · Cómo se lee la figura de la región

- **La línea sólida es el total**, con todas las sedes. **La línea discontinua es lo que queda sin las
  sedes en retirada.** La banda entre las dos es lo que ellas aportaban: si se angosta, se fueron
  achicando, y por eso el crecimiento sin ellas es mayor.
- **Un punto hueco** es un año que se sumó sin una sede, porque lo que faltaba pesaba menos del 1%.
  **Un año sin punto** es uno sin total: lo que faltaba pesaba más, y sumar mostraría una caída que no
  ocurrió. El pie dice qué sede faltó y cuánto pesaba.
- **El pie trae los dos crecimientos.** En tu texto di cuál usas y por qué: son dos preguntas, cuánto
  cambió la región y cuánto creció el mercado que sigue compitiendo.

## 4 · Compón

    python3 <carpeta de esta skill>/assets/construir_figura.py --entrada figura.json --salida figura.html

- **Si responde con el nombre del archivo**, la figura está lista.
- **Si se niega (código 2)**, dice por qué e imprime **una tabla con los mismos datos**. Si tocaste el
  spec, vuelve a pedirlo y cambia sólo el encuadre. Si no, **entrega esa tabla** y di por qué no hay
  gráfico. No la reemplaces por un dibujo hecho de otra forma.
- **Si dice que «el spec no es el que entregó el servicio»**, el archivo no es copia fiel: vuelve a pedir
  la herramienta y guarda su `spec` tal cual. No lo corrijas a mano.

## 5 · Entrega

- **Si la figura ya aparece dibujada en la conversación** (en claude.ai y Claude Desktop, las seis herramientas
  traen su propio widget, con sus notas), no la publiques de nuevo como página salvo que te lo pidan: escribe el texto que la
  acompaña. En los demás clientes la figura no aparece sola, y sigues como abajo.
- **Si puedes publicar una página** (un Artifact), publica `figura.html` tal cual.
- **Si no puedes**, entrega el archivo.

En el texto que la acompaña:
- **La figura acompaña, no reemplaza.** Di en una o dos frases qué muestra, con cifras tomadas del
  spec, y repite los avisos que importan: el hueco, el valor inconsistente y las sedes que no se comparan.
- **Sin superlativos** que no salgan de comparar todas las series dibujadas.
- **Declara el universo:** son universidades. IP y CFT no están en esta serie.

## Lo que esta skill no hace

Existen **dos formas**: la serie por sede y la de la región entera. No dibuja carreras, ni
universidades fuera de una región, ni otros indicadores (selectividad, gratuidad, flujos). Si te piden
otro gráfico, dilo y responde con la tabla de las herramientas correspondientes.
