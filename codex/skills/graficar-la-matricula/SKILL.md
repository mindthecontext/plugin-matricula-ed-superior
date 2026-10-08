---
name: graficar-la-matricula
description: Dibuja cómo evolucionó la matrícula de una o varias sedes universitarias, 2007–2025 — «¿cómo ha evolucionado la matrícula de la UST en Temuco?», «grafícame la matrícula de las sedes de La Araucanía», «muéstrame la serie de esta universidad», «compara cómo crecieron estas sedes». Produce una figura que se publica como página, con los huecos y los valores inconsistentes declarados. NO dibuja carreras, regiones agregadas ni otros indicadores: hoy existe una sola forma.
---

# Graficar la matrícula

Una serie de diecinueve años se lee mejor dibujada que contada. Esta skill produce **una figura**: la
matrícula total de pregrado de una o varias sedes universitarias, año a año. El servicio entrega el
**spec** con los datos; tú decides el encuadre; la receta dibuja. **Nunca escribas HTML ni código de
gráfico, y nunca armes el spec a mano.**

## 1 · Pide el spec al servicio

    figura_matricula(region, instituciones=None)

Sin `instituciones`, trae todas las sedes universitarias de la región; con ellas, sólo esas (`["UFRO",
"católica de temuco"]`). Devuelve `spec` **listo para la receta**: las cifras, un punto por año, los
huecos y los valores inconsistentes ya declarados, las sedes en retirada marcadas y la procedencia
propia de la matrícula.

- **Guarda `spec` tal cual** en un archivo JSON.
- **Puedes cambiar `title` y `subtitle`** para que digan lo que la pregunta pide (por ejemplo, «Tres
  sedes que crecen en Temuco»). Respeta sus roles, abajo.
- **No toques `series`, `annotations`, `notices` ni `provenance`.** Si algo no te parece bien, dilo en
  el texto; no lo corrijas en el spec.

Si la herramienta responde con `error`, dilo: no armes el spec a mano.

## 2 · El encuadre: los roles de los textos

El formato completo está en `references/spec.md`. El servicio ya trae un título y un subtítulo
correctos; si los cambias, respeta sus roles:

- **`title`** nombra la vista, no el hallazgo: «La matrícula de las sedes universitarias de La
  Araucanía», no «La UFRO lidera».
- **`subtitle`** dice unidad, universo y ventana: «matrícula total de pregrado por sede, universidades,
  2007–2025».
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

## 4 · Compón

    python3 <carpeta de esta skill>/assets/construir_figura.py --entrada figura.json --salida figura.html

- **Si responde con el nombre del archivo**, la figura está lista.
- **Si se niega (código 2)**, dice por qué e imprime **una tabla con los mismos datos**. Si tocaste el
  spec, vuelve a pedirlo y cambia sólo el encuadre. Si no, **entrega esa tabla** y di por qué no hay
  gráfico. No la reemplaces por un dibujo hecho de otra forma.

## 5 · Entrega

- **Si puedes publicar una página** (un Artifact), publica `figura.html` tal cual.
- **Si no puedes**, entrega el archivo.

En el texto que la acompaña:
- **La figura acompaña, no reemplaza.** Di en una o dos frases qué muestra, con cifras tomadas del
  spec, y repite los avisos que importan: el hueco, el valor inconsistente y las sedes que no se comparan.
- **Sin superlativos** que no salgan de comparar todas las series dibujadas.
- **Declara el universo:** son universidades. IP y CFT no están en esta serie.

## Lo que esta skill no hace

Hoy existe **una forma**: la serie de matrícula por sede. No dibuja la serie de la región agregada
—`panorama_region` la entrega en `matricula_region.serie`, con y sin las sedes en retirada, pero esa
forma todavía no tiene receta: dila con sus cifras y sus avisos—, ni carreras, ni otros indicadores.
Si te piden otro gráfico, dilo y responde con la tabla de las herramientas correspondientes.
