---
name: reportar-una-region
description: Arma el reporte de la educación universitaria de una región chilena —portada, secciones con sus figuras y las lecturas que las acompañan— y lo entrega como una página. «Hazme el reporte de La Araucanía», «un informe de las universidades del Biobío», «quiero el reporte regional de Ñuble», «arma un documento sobre quiénes estudian en mi región». Hoy cubre la portada y las secciones 1, «Quiénes son», 2, «Con qué llegan», y 3, «El mercado»; las demás secciones llegarán una a una. Para una sola figura, usa graficar-la-matricula.
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

Las figuras de rangos de la sección 2 (la PAES por sede y la carrera que estira la cola) traen su
**`groups`**:

| Clave | Qué es |
|---|---|
| `rank_mid` | Las filas de mayor a menor mediana. En la carrera tope, cada una con su carrera (`detail`). |
| `rank_box_width` | De la caja más ancha a la más angosta: una sede angosta recibe un alumnado parejo en puntaje. |
| `rank_upper_tail` | Cuánto se despega el extremo alto de la caja: la cola larga. |
| `above_reference`, `at_reference`, `below_reference` | Las sedes con mediana sobre, en y bajo la mediana nacional. |
| `not_robust` | Las filas con menos de 30 puntajes: van sin caja y no sostienen lecturas fuertes. |

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

### Cómo leer la sección 2, «Con qué llegan»

- **La PAES describe sólo a quienes la rindieron**, y entraron entre 2023 y 2025. No es el alumnado
  completo de la sede: escribe «quienes rindieron la PAES», no «los estudiantes de la sede». Antes de
  2023 se rendía la PTU, que es otra escala: no la mezcles.
- **El ancho cuenta tanto como el centro.** Dos sedes con la misma mediana pueden tener cajas muy
  distintas. Si hablas de la más pareja o la más dispersa, cópiala de `rank_box_width`.
- **Una cola larga arriba suele ser una carrera, no la sede.** Si el extremo alto de una sede se despega
  (`rank_upper_tail`), mira la figura siguiente antes de leerlo como un rasgo de la institución: el
  candidato natural es Medicina.
- **Medicina tiene un mercado de admisión propio**, más parecido al de Medicina en otra región que al
  del resto de su institución. Cuando la carrera tope es Medicina, no la uses para decir que la sede es
  selectiva: dice qué carreras dicta, no a quién admite.
- **Una fila con «~» (`not_robust`)** tiene menos de 30 puntajes: nómbrala si hace falta, pero sin
  construir el relato sobre ella.
- **El 10% superior es otra vara:** mide el rendimiento relativo al propio colegio, no el puntaje. No
  la sumes ni la compares directamente con la PAES.

### Cómo leer la sección 3, «El mercado»

- **El bloque de cifras lo escribe el servicio**, con su conclusión. Puedes citar sus cifras en tu
  lectura, pero no reescribas la conclusión con otras palabras más fuertes.
- **Es retención universitaria, no acceso.** Cuenta a quienes entraron directo del colegio a una
  universidad. Quien fue a un CFT o un IP, o no siguió estudiando, no está: no escribas «el X% de los
  jóvenes de la región se queda».
- **El balance compara tamaños, no producción.** Dice si las universidades de la región reciben más o
  menos estudiantes de los que la región manda a la universidad. No escribas que la región «forma más
  gente de la que produce»: los entrantes incluyen a quienes vienen de otras regiones.
- **«Adónde se van» y «de dónde vienen» tienen bases distintas.** Los primeros son % de los egresados
  de la región; los segundos, % de quienes entran acá. No los restes ni los compares como si fueran la
  misma cuenta.
- **En las universidades de la capital, el % de colegio pagado describe a quién se va a cada una**, no
  ordena a las universidades. Úsalo para decir que la migración tiene dos tramos, no que una
  universidad es «más elitista».
- **«Cuánto alumnado es de la región» describe la composición de cada sede**, no cuántos se quedan:
  una región puede mandar parte de sus egresados afuera y tener sedes casi enteramente locales.
- **Una región con dos mercados** (la nota lo dice cuando corresponde): no la describas con un solo
  centro, y no compares sedes de una ciudad con las de la otra como competidoras.

## 3 · Compón

    python3 <carpeta de la skill graficar-la-matricula>/assets/construir_figura.py --entrada reporte.json --salida reporte.html

El compositor está en la skill hermana `graficar-la-matricula`, junto a las recetas de las figuras.

- **Si responde con el nombre del archivo**, el reporte está listo. Dice cuántas figuras y lecturas
  lleva, y si alguna figura salió como tabla.
- **Si se niega (código 2)**, dice qué lectura cita qué cifra que no está.
- **Si dice que «esta versión del plugin no conoce la forma»**, el servicio es más nuevo que el plugin
  instalado. No publiques nada: dile a quien preguntó que actualice el plugin y vuelva a pedir el
  reporte. Corrige esa lectura y vuelve
  a componer. Si la negativa es por una sede en retirada en el cuerpo, el spec se tocó: pídelo de nuevo.
- **Una figura que no se puede dibujar sale como tabla** y el reporte sigue: dilo en tu respuesta.

## 4 · Entrega

- **Si puedes publicar una página** (un Artifact), publica `reporte.html` tal cual.
- **Si no puedes**, entrega el archivo.

En tu respuesta, en dos o tres frases, di qué cubre el reporte y qué no todavía. Hoy cubre la portada y
las secciones 1 a 3; el origen escolar, el acceso y el financiamiento, las preferencias y los
desenlaces, los planos y la síntesis llegarán como secciones nuevas. No los
completes con otras herramientas dentro del reporte.
