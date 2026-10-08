---
description: Dibuja cómo evolucionó la matrícula de una o varias sedes universitarias, 2007–2025 — «¿cómo ha evolucionado la matrícula de la UST en Temuco?», «grafícame la matrícula de las sedes de La Araucanía», «muéstrame la serie de esta universidad», «compara cómo crecieron estas sedes». Produce una figura que se publica como página, con los huecos y los valores inconsistentes declarados. NO dibuja carreras, regiones agregadas ni otros indicadores: hoy existe una sola forma.
---

# Graficar la matrícula

Una serie de diecinueve años se lee mejor dibujada que contada. Esta skill produce **una figura**: la
matrícula total de pregrado de una o varias sedes universitarias, año a año. Tú armas el **spec**
—los datos y el encuadre—; la receta dibuja. **Nunca escribas HTML ni código de gráfico.**

## 1 · Trae los datos de las herramientas, en esta sesión

- **Las sedes de una región:** `panorama_region(region)`. De ahí sale la lista de sedes y cuáles están
  en retirada: las que traen `nota` con «sede residual».
- **La serie de cada sede:** `ficha_sede(institucion, region)` → `serie_matricula {x, matricula}`.
  `panorama_region` no trae la serie, así que es **una llamada por sede**.
- **La procedencia:** el bloque `procedencia` de la misma respuesta. Lo copias tal cual.

Ninguna cifra del spec ni de tu texto sale de otra parte. Si una herramienta no responde, no hay figura.

## 2 · Arma el spec

El formato completo, con un ejemplo, está en `references/spec.md`. Lo esencial:

- **`title`** nombra la vista, no el hallazgo: «La matrícula de las sedes universitarias de La
  Araucanía», no «La UFRO lidera». **`subtitle`** dice unidad, universo y ventana: «matrícula total de
  pregrado por sede, universidades, 2007–2025».
- **`provenance`** es el bloque de la herramienta. **No escribas `source`**: la fuente se estampa sola,
  y si la escribes, la figura se niega.
- **Un punto por año de `x`**, con `"value": null` donde no hay dato. **No omitas el año**: si falta,
  la línea uniría el hueco y la figura se niega.
- **`label`** con el nombre como se escribe, no en mayúsculas: «U. de la Frontera», no
  «UNIVERSIDAD DE LA FRONTERA».
- Las sedes residuales van con `"retreating": true`: no se dibujan, se nombran al pie.

## 3 · Declara lo que la serie no dice sola

La receta **deriva** de los datos lo que hay que declarar, y se niega si falta:

- **Un hueco** —un `null` entre el primer y el último dato de una serie— exige una anotación
  `kind: "gap"` con su nota: por ejemplo, «sin registro en la fuente».
- **Un valor inconsistente** —el triple o un tercio de sus dos vecinos con dato— exige
  `kind: "inconsistent"`: por ejemplo, «el registro es inconsistente en este tramo». Se dibuja suelto y
  rodeado, sin unirlo a la línea. **No lo borres ni lo corrijas**: se declara.

No necesitas buscarlos a mano: compón, y si la receta se niega, te dice exactamente cuáles faltan.

## 4 · Compón

    python3 <carpeta de esta skill>/assets/construir_figura.py --entrada figura.json --salida figura.html

- **Si responde con el nombre del archivo**, la figura está lista.
- **Si se niega (código 2)**, dice por qué e imprime **una tabla con los mismos datos**. Corrige el
  spec si el motivo es tuyo, como una anotación que falta. Si no se puede, **entrega esa tabla** y di
  por qué no hay gráfico. No la reemplaces por un dibujo hecho de otra forma.

## 5 · Entrega

- **Si puedes publicar una página** (un Artifact), publica `figura.html` tal cual.
- **Si no puedes**, entrega el archivo.

En el texto que la acompaña:
- **La figura acompaña, no reemplaza.** Di en una o dos frases qué muestra, con cifras tomadas del
  spec, y repite los avisos que importan: el hueco, el valor inconsistente y las sedes que no se comparan.
- **Sin superlativos** que no salgan de comparar todas las series dibujadas.
- **Declara el universo:** son universidades. IP y CFT no están en esta serie.

## Lo que esta skill no hace

Hoy existe **una forma**: la serie de matrícula por sede. No dibuja la matrícula de una región
agregada (el servicio todavía no la entrega con y sin residuales), ni carreras, ni otros indicadores.
Si te piden otro gráfico, dilo y responde con la tabla de las herramientas correspondientes.
