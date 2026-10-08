---
name: reportar-una-region
description: Arma el reporte de la educación universitaria de una región chilena —portada, secciones con sus figuras y las lecturas que las acompañan— y lo entrega como una página. «Hazme el reporte de La Araucanía», «un informe de las universidades del Biobío», «quiero el reporte regional de Ñuble», «arma un documento sobre quiénes estudian en mi región». Hoy cubre la portada y la sección 1, «Quiénes son»; las demás secciones llegarán una a una. Para una sola figura, usa graficar-la-matricula.
---

# Reportar una región

Un reporte es más que una figura: tiene una portada que dice qué sedes hay y cuáles están en retirada,
y secciones donde cada figura viene con su **lectura**. El servicio entrega todo lo que es dato. **Las
lecturas las escribes tú**, y esta skill dice cómo, porque es lo que hace que el reporte se pueda creer.

## 1 · Pide el reporte

    reporte_region(region)

Devuelve `spec`: la portada (`cover`), las secciones con sus figuras ya armadas y, junto a cada figura,
un bloque `reading` vacío para su lectura. Trae además `facts`: cifras de contexto que puedes citar
(cuántas sedes activas, cuántas en retirada, los entrantes del período, la matrícula de la región).

Cada figura de barras trae a su lado **`groups`**, con los órdenes y los grupos ya calculados:

| Clave | Qué es |
|---|---|
| `rank` | Las sedes de mayor a menor, con su puesto. Dos sedes con el mismo valor comparten puesto. |
| `above_reference`, `at_reference`, `below_reference` | Las sedes sobre, en y bajo el valor nacional. |
| `zero`, `no_data` | Las sedes que valen 0 y las que no tienen dato. |
| `small_sample` | Las sedes con muestra chica: sin lecturas fuertes sobre ellas. |

La figura de la serie («Cómo han cambiado») trae también su **`groups`**, con lo que una lectura de una
serie dice con palabras:

| Clave | Qué es |
|---|---|
| `sites[].first`, `last`, `peak`, `low` | El primer y el último dato de cada sede, su máximo y su mínimo, con el año. |
| `sites[].change_full`, `change_window` | Cuánto cambió en todo su período y en `window` (2019–2025): sentido (`up`, `down`), cantidad, porcentaje y `small_base` si partió de menos de 150 estudiantes (su porcentaje no se compara). |
| `sites[].largest_rise`, `largest_fall` | Su mayor alza y su mayor caída de un año al siguiente. |
| `sites[].runs` | Los tramos en que subió o bajó **todos** los años (tres pasos o más). |
| `rank_change_full_amount`, `rank_change_full_pct`, `rank_change_window_amount`, `rank_change_window_pct` | Quién cambió más, en número y en porcentaje, en todo el período y en la ventana. |
| `rank_longest_run` | La racha más larga de cada sede, ordenadas: «el crecimiento más sostenido» sale de aquí. |

Un valor que no calza con sus vecinos no cuenta en nada de esto, y un año sin dato corta los tramos.

**No toques la portada ni las figuras.** Tu trabajo son los bloques `reading`.

## 2 · Escribe las lecturas

Cada bloque `reading` tiene dos campos, y la diferencia entre ellos es la regla más importante:

- **`text`: lo que las cifras muestran.** Hechos que se leen en la figura de al lado, con sus números.
- **`compatible`: una explicación que las cifras no prueban**, si hace falta. Se publica separada y
  rotulada como «Explicación compatible». Nunca la mezcles con `text`: una hipótesis escrita como
  hecho es la forma más común de que un reporte diga algo falso con cifras correctas.

Si para una figura no hay nada que decir que la figura no diga ya, **deja el bloque vacío**: no se
publica. Un reporte no mejora con párrafos de relleno.

### Las reglas editoriales (las del reporte local de la casa)

1. **Toda cifra sale del spec.** El compositor revisa cada número de tus lecturas contra los datos que
   entregó el servicio, y **se niega** si encuentra uno que no está:
   - un porcentaje tiene que ser uno de los porcentajes entregados;
   - un número sin decimales que redondeaste («9» por 9,3) no pasa: escribe el valor tal como viene,
     o con un decimal.

   No calcules diferencias, sumas ni razones por tu cuenta: si una cifra no está en `facts` ni en las
   figuras, no la escribas.

   **La cifra va con su sede**, y la sede se escribe **tal como viene en la figura**. El compositor no
   revisa a quién le pones cada cifra: eso es tuyo.
2. **Los órdenes y los grupos se copian de `groups`; no se deducen.** «Las tres que más reciben», «la
   segunda», «las que superan la referencia», «cinco de las siete», «las que no tienen jornada
   vespertina»: cada una de estas frases nombra un grupo, y **las sedes que pones en él son las de
   `groups`**, en ese orden.
   - Si citas un grupo de **otra** figura («las tres sedes con más entrantes», en la lectura de la
     edad), cópialo del `rank` de **esa** figura.
   - Es el error que las cifras correctas no delatan: una lectura dijo «las tres sedes con más
     entrantes … U. Mayor», con todas sus cifras bien, y la tercera era otra sede.
   - **Sin ranking de uno.** Con una sola sede no hay orden: se describe.
3. **Lo que dices de una serie también se copia de `groups`.** «La que más creció», «su mayor
   salto», «sin pausa hasta 2021», «subió todos los años desde 2019», «su máximo fue en 2021»: cada
   una de estas frases tiene su clave, y si no está, no la escribas.
   - **«La que más creció» exige decir en qué:** en número (`..._amount`) o en porcentaje
     (`..._pct`), y en qué período. Rara vez es la misma sede: en La Araucanía, entre 2019 y 2025,
     U. Autónoma de Chile sumó más estudiantes y U. Mayor creció más en porcentaje.
   - **«Todos los años», «sin pausa» o «sostenido» sólo si hay un tramo en `runs`** que cubra esos
     años. Una sede que creció en el total pero bajó un año no creció «sin pausa».
   - Un cambio con `small_base` puede tener un porcentaje enorme por partir de muy poco: no lo pongas
     como el que más creció en porcentaje. Los órdenes por porcentaje ya lo dejan fuera.
   - **«El más sostenido» compara rachas:** sale de `rank_longest_run`. Una racha que sigue abierta
     («sube todos los años desde 2017») no es la más larga si otra sede tuvo una mayor antes.
4. **Muestras chicas, sin lecturas fuertes.** Una sede con pocos entrantes (mira la figura «Cuántos
   entran» y el `n` de cada barra) puede tener porcentajes extremos por azar. Nómbrala si hace falta,
   pero no construyas el relato sobre ella.
5. **La referencia es el país, no el promedio de las sedes.** La línea punteada es el valor nacional,
   calculado sobre todos los estudiantes. Compara contra ella, no contra «el resto de la región».
6. **Las sedes en retirada se declaran una vez, en la portada**, y no vuelven a aparecer. No las nombres
   en las lecturas de las secciones.
7. **El universo son las universidades**, en pregrado. Si una lectura podría leerse como «todos los que
   estudian en la región», di que son universidades: los institutos profesionales y los CFT no están.
8. **Coma decimal y punto de miles**, como en Chile: 12,1% y 11.426.
9. **Sin jerga de la casa.** Nada de «pack», «artefacto», nombres de reglas ni códigos de criterio.

## 3 · Compón

    python3 <carpeta de la skill graficar-la-matricula>/assets/construir_figura.py --entrada reporte.json --salida reporte.html

El compositor está en la skill hermana `graficar-la-matricula`, junto a las recetas de las figuras.

- **Si responde con el nombre del archivo**, el reporte está listo. Dice cuántas figuras y lecturas
  lleva, y si alguna figura salió como tabla.
- **Si se niega (código 2)**, dice qué lectura cita qué cifra que no está. Corrige esa lectura y vuelve
  a componer. Si la negativa es por una sede en retirada en el cuerpo, el spec se tocó: pídelo de nuevo.
- **Una figura que no se puede dibujar sale como tabla** y el reporte sigue: dilo en tu respuesta.

## 4 · Entrega

- **Si puedes publicar una página** (un Artifact), publica `reporte.html` tal cual.
- **Si no puedes**, entrega el archivo.

En tu respuesta, en dos o tres frases, di qué cubre el reporte y qué no todavía. Hoy cubre la portada y
la sección 1; selectividad, el mercado y la movilidad, el origen escolar, el acceso y el financiamiento,
las preferencias y los desenlaces, los planos y la síntesis llegarán como secciones nuevas. No los
completes con otras herramientas dentro del reporte.
