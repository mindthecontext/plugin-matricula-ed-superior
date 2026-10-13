---
description: Arma el reporte de la educación universitaria de una región chilena —portada, secciones con sus figuras y las lecturas que las acompañan— y lo entrega como una página. «Hazme el reporte de La Araucanía», «un informe de las universidades del Biobío», «quiero el reporte regional de Ñuble», «arma un documento sobre quiénes estudian en mi región». Hoy cubre la portada y las secciones 1, «Quiénes son», 2, «Con qué llegan», 3, «El mercado», 4, «De qué origen vienen», 5, «Cómo entran y quién paga», 6, «Dónde los eligen», 7, «En qué termina», y 8, «La región en tres planos», con una síntesis al principio y las notas de método al final. Por defecto se entrega como la página HTML que arma su compositor, publicada tal cual; si la persona pide expresamente un dashboard, se arma siguiendo la receta del saber (si_armas_un_dashboard). Para una sola figura, usa graficar-la-matricula.
---

# Reportar una región

Un reporte es más que una figura: tiene una portada que dice qué sedes hay y cuáles están en retirada,
y secciones donde cada figura viene con su **lectura**. El servicio entrega todo lo que es dato. **Las
lecturas las escribes tú**, y esta skill dice cómo, porque es lo que hace que el reporte se pueda creer.

## 1 · Pide el reporte

**Antes: ¿qué universo pidieron?** Este reporte es de universidades. Una región tiene además sus IP y
CFT, que en cinco regiones pesan más que las universidades.

- **Nombró las universidades:** sigue con este reporte.
- **Nombró los IP, los CFT o el técnico:** este reporte no es; usa `panorama_tecnico_region` (skill
  analizar-el-tecnico-de-una-region).
- **No nombró un universo** («el reporte de la educación superior de…», «el reporte de la región»): pide
  primero **`portada_region(region)`**, redacta sus dos lecturas y entrégala **antes** del reporte. Después
  va este reporte y, al final, la oferta del técnico-profesional. `reporte_que_va_primero` dice cuál pesa
  más en la región; si es «tecnico», dilo en la entrega: el reporte técnico completo está en preparación, y
  mientras tanto el técnico se responde con `panorama_tecnico_region`.

    reporte_region(region)

Devuelve `spec`: la portada (`cover`), la síntesis, las secciones con sus figuras ya armadas y, junto a
cada figura, un bloque `reading` vacío para su lectura, y al final las notas de método (sin lectura). Trae además `facts`: cifras de contexto que puedes citar
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

Las figuras partidas de las secciones 6 y 7 (cada sede partida en tramos que suman 100%) traen su
**`groups`**:

| Clave | Qué es |
|---|---|
| `rank_<tramo>` | Las sedes de mayor a menor en ese tramo: `rank_conv`, `rank_desp`; `rank_titula`, `rank_otra_carrera`, `rank_sigue`, `rank_sin_titulo`. |
| `above_reference`, `below_reference` | Por tramo, las sedes sobre y bajo el país (la última fila de la figura). |
| `small_sample`, `no_data` | Las sedes con muestra chica y las que no tienen dato (sin preferencias registradas o sin cohortes). |
| `displaced_top_origin` | Sección 6: por sede, la institución que más de sus desplazados había puesto primero, y qué parte (`pct`). |
| `magnet` | Sección 6: la institución que más desplazados de las sedes de la región había puesto primero. |

Los planos de la sección 8 (una burbuja por sede, dos ejes contra el país) traen su **`groups`**:

| Clave | Qué es |
|---|---|
| `quadrants` | Las sedes de cada cuadrante, de la más grande a la más chica: `x_above_y_above`, `x_above_y_below`, `x_below_y_above`, `x_below_y_below`. El nombre de cada uno está en `quadrant_labels` de la figura. |
| `on_reference` | Las sedes que caen justo sobre una línea del país: no están en ningún cuadrante. |
| `rank_x`, `rank_y` | Las sedes de mayor a menor en cada eje. |
| `small_sample` | Las sedes con pocos entrantes. |

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
8. **Cada cifra tiene su fuente y sus años, y no todas son iguales.** Cada figura dice al pie de qué base
   sale y su subtítulo, qué años cubre: la matrícula es 2021–2025, la PAES 2023–2025, primera
   generación 2021–2022, el 10% superior llega a egresos de 2023. Si en tu respuesta citas una cifra
   fuera del reporte, di de qué base y de qué años es; no la presentes como «hoy».
9. **Coma decimal y punto de miles**, como en Chile: 12,1% y 11.426. Si el nombre de la sede ya lleva
   paréntesis, no le agregues otro con la cifra: «U. de Los Lagos (Castro), con 567,3», no «U. de Los
   Lagos (Castro) (567,3)».
10. **Sin jerga de la casa.** Nada de «pack», «artefacto», nombres de reglas ni códigos de criterio.

### Cómo escribir la síntesis

La síntesis abre el reporte, pero **escríbela al final**, cuando ya escribiste las demás lecturas. Su bloque
`findings` trae los hechos candidatos, cada uno con su sección (`section`), calculados de las mismas figuras:

| Hecho | Qué dice |
|---|---|
| `tamano` | La sede con más matrícula el último año y la que más entrantes recibe; `same_site` dice si son la misma. |
| `puntajes` | Las sedes que concentran los mejores puntajes, con la regla (`rule`). Si la lista está vacía, ninguna. |
| `mercado` | La retención universitaria y el balance: si el sistema local es mayor o más chico que lo que la región aporta. |
| `colegio` | La brecha de puntaje según el colegio de egreso. |
| `gratuidad` | Las sedes que no adhieren a la gratuidad y cuántos entrantes reciben. |
| `preferencias` | La sede con el alumnado más convencido y la con más desplazados, y el imán de la región. |
| `desenlaces` | Dónde más y dónde menos se titulan en la carrera de entrada, y el país. |
| `planos` | Las sedes sobre el país en puntaje y en prioritarios a la vez. |

- **De 4 a 6 viñetas**, cada una en una línea que empieza con «- » y termina con su sección: «(§3)».
- **Sólo hechos de `findings`**, con sus cifras tal como vienen. Un hecho que la región no permite (una sola
  sede, sin cohortes) no viene: no lo reemplaces con otro.
- **Elige lo que distingue a la región**, no lo que se repite en todas. Una lista vacía (`concentrates_top_scores: []`)
  también es un hecho, pero rara vez vale una viñeta.
- **Sin interpretación**: la síntesis no lleva `compatible`. Las explicaciones ya están en sus secciones.

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

### Cómo leer la sección 4, «De qué origen vienen»

- **Es una asociación, no un mecanismo.** El colegio de egreso se asocia con el puntaje y con la
  migración, pero estos datos no dicen por qué. No escribas que el colegio «causa» o «explica» la
  diferencia; si quieres proponer una razón, va en `compatible`.
- **«Particular pagado» es una categoría administrativa**, no un nivel de ingreso. No escribas «los
  estudiantes de mayores ingresos» ni «los más ricos».
- **El porcentaje y las personas responden preguntas distintas.** El porcentaje dice cómo es el aula; las
  personas, dónde está esa población. Si el orden cambia entre las dos figuras, ése es el hallazgo; cópialo
  de los `groups` de cada una. Las personas son una estimación: no las presentes como un conteo exacto.
- **Prioritario y primera generación no se suman**: un mismo estudiante suele ser las dos cosas.
- **Primera generación es de 2021–2022, no del alumnado actual.** El DEMRE dejó de preguntar la educación
  de los padres desde 2023, y la cifra cubre sólo a quienes entraron esos dos años y respondieron la
  ficha. Escribe «entre quienes entraron en 2021 y 2022», nunca «hoy» ni «2021–2025».
- **La caja de puntaje por tipo de colegio cubre sólo a quienes rindieron la PAES**, como en la sección 2.

### Cómo leer la sección 5, «Cómo entran y quién paga»

- **Los ejes de la vía no se suman.** La vía centralizada incluye a la de equidad, y el PACE es una parte de
  la equidad. No escribas «el 88% entra por la vía centralizada y otro 4% por equidad».
- **Equidad y PACE son de 2024–2025**, no de toda la ventana: antes no se registraba la vía.
- **Gratuidad 0% no es un error ni una exclusión:** la institución no adhiere, y es una decisión de modelo
  de financiamiento. No escribas que «sus estudiantes no acceden a la gratuidad» como si fuera un juicio
  sobre ellos. Quiénes no adhieren lo dicen los `groups` de la figura (`does_not_adhere`):
  nómbralas desde ahí, y no escribas que «los datos no explican la causa».
- **El arancel y la gratuidad son de un solo año, el último con entrantes** (hoy 2025; lo dice el subtítulo): el
  arancel es la mediana de quienes entraron ese año, en pesos de ese año, con lo informado en UF convertido con la
  UF del 1 de enero. Escribe el año («el arancel mediano de quienes entraron en 2025»), no «el arancel de hoy»; y no
  lo compares con cifras de otros años como si fueran la misma serie.
- **Un 0% de PACE en una privada fuera del Consejo de Rectores es lo normal de su grupo**; la nota lo dice con
  la cifra del país. No lo leas como falta de compromiso con la equidad.

### Cómo leer la sección 6, «Dónde los eligen»

- **Convencido y desplazado se miden sólo en la admisión centralizada.** Quien entró por otra vía no está.
  Escribe «de quienes entraron por la admisión centralizada», no «de sus estudiantes».
- **Desplazado no es segunda opción**: pudo ser la cuarta. No escribas «su segunda opción».
- **No es prestigio.** Si el postulante pone primero lo que cree alcanzable, la cifra mide deseabilidad
  filtrada por expectativa. No escribas que una sede es «la más deseada» o «la preferida de la región».
- **A quién habían puesto primero** sale de `displaced_top_origin`, y **el imán de la región**, de `magnet`.
  Pueden ser instituciones de afuera: escribe el nombre tal como viene, con su región entre paréntesis.
- Las razones de una elección —calidad percibida, pares, distancia, costo— no están en este registro: si
  quieres proponer una, va en `compatible`.
- **La lista de espera (`lista_espera`) mide presión por el cupo, no rechazo ni calidad.** De quienes la
  pusieron primera y se matricularon, cuántos entraron desde la lista de espera, cuando otros seleccionados no
  se matricularon: siguen siendo convencidos. No escribas «no los aceptaron» ni «entraron de segunda». Una
  cifra alta dice que la sede llena más cupos de los que selecciona de entrada; una de 0%, que todos los que la
  pusieron primera quedaron seleccionados.
- **El nivel subió con la PAES** (los avisos traen el del país por año). Compara sedes entre sí con la cifra de
  la ventana, no una sede contra el país de un año.

### Cómo leer la sección 7, «En qué termina»

- **Describe a quienes entraron hace una década** (cohortes 2011–2016), no a la sede de hoy. Escribe
  «de quienes entraron entre 2011 y 2016», nunca «hoy se titula el X%».
- **Los cuatro tramos suman 100% y el del medio importa:** titularse en otra carrera es cambiar de rumbo
  sin abandonar. No leas sólo «se tituló» contra «sin título».
- **Una titulación baja no prueba una admisión menos selectiva**: también son compatibles las carreras más
  largas, el trabajo en paralelo y el cambio de institución. Eso va en `compatible`, no en `text`.
- **Si la región no tiene cohortes observables**, la sección trae sólo la nota que lo explica: no hay
  lectura que escribir.

### Cómo leer la sección 8, «La región en tres planos»

- **Un cuadrante dice dónde cae una sede, no qué vale.** Usa el nombre descriptivo de `quadrant_labels` («más
  puntaje y más prioritarios que el país») y las sedes de `quadrants`. No escribas «la esquina más exigente», «la
  más meritoria» ni «la mejor»: una interpretación así, si hace falta, va en `compatible`.
- **Los dos ejes de un plano no siempre son del mismo período.** La PAES es de 2023–2025; prioritarios y 10%
  superior, de 2021–2025: no escribas que una sede «hoy» combina las dos cosas. El plano del precio sí tiene sus dos
  ejes en el mismo año (arancel y gratuidad del último año), y ahí sí se leen juntos.
- **El tamaño de la burbuja es el número de entrantes**, no un resultado: no digas que una sede «pesa más» en el
  plano por su posición.
- **Si un plano no se dibujó** porque la región no tiene tres sedes con los dos ejes, la nota de la sección lo
  dice: no hay lectura que escribir para él.

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

- **Si puedes publicar una página** (un Artifact), publica `reporte.html` tal cual, como una página HTML
  simple.
- **Si no puedes**, entrega el archivo.

**Por defecto, no lo conviertas en un dashboard ni en otro tipo de artefacto del cliente, y no redibujes sus
figuras**, aunque el cliente lo ofrezca para «reportes» o «visualizaciones de datos». El reporte es el
`reporte.html` del compositor por dos razones que se pierden al rehacerlo: el compositor **verifica que
toda cifra de las lecturas esté en el dato** —y se niega si no—, y cada figura lleva **sus avisos**
(años, cobertura, sedes en retirada, cómo se calcula).

**Si la persona pide expresamente un dashboard** («arma un dashboard», «quiero un panel»), ármalo, pero
**con la receta del saber**: `panorama_region`, `flujos_region` y las herramientas de figura traen
`si_armas_un_dashboard`, y la sigues entera —cada cifra una consulta en vivo a esas herramientas, los
años sin valor como huecos, los valores inconsistentes marcados aparte, los avisos a la vista, las sedes
en retirada fuera de las comparaciones, ninguna conclusión escrita a mano, la fuente de cada gráfico—.
Dile en dos líneas qué gana y qué pierde frente al reporte: datos en vivo y su procedencia a la vista, a
cambio de que las lecturas no pasen por el control de cifras del compositor. Pedir «el reporte» o «un
informe» no es pedir un dashboard.

En tu respuesta, en dos o tres frases, di qué cubre el reporte y qué deja fuera: las notas de método al final
lo dicen (la acreditación, la titulación de cohortes recientes, las preferencias fuera de la admisión
centralizada). No lo completes con otras herramientas dentro del reporte.
