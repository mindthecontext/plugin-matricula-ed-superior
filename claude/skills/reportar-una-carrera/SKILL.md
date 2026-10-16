---
description: Arma el reporte nacional de una carrera —portada, secciones con sus figuras y las lecturas que las acompañan— y lo entrega como una página. «Hazme el reporte de Psicología», «un informe de Enfermería en Chile», «quiero el reporte de Kinesiología», «arma un documento sobre quién estudia Derecho». Cubre la portada y las secciones 1, «El mercado», 2, «Quién entra», 3, «Quién paga», 4, «En qué termina», y 5, «Territorio y acceso», con una síntesis al principio y las notas de método al final. Se entrega como la página HTML que arma su compositor, publicada tal cual. Para una pregunta puntual sobre la carrera, usa explorar-una-carrera; para el reporte de una región, reportar-una-region; para una sola figura, graficar-la-matricula.
---

# Reportar una carrera

El reporte de una carrera mira **todo el país**: todas las instituciones que la dictan, universidades,
IP y CFT. El servicio entrega todo lo que es dato. **Las lecturas las escribes tú**, y esta skill dice
cómo, porque es lo que hace que el reporte se pueda creer.

## 1 · Pide el reporte

    reporte_carrera(carrera)

Si el nombre no calza con una carrera del saber, la herramienta devuelve los candidatos: pregunta cuál.

La figura «Frente a otra carrera» compara el ritmo con una carrera de control: por defecto, la del mismo tipo de
mercado con el primer año más parecido en 2019 (a Psicología le toca Derecho), y su subtítulo lo dice. Si la persona
pide otra comparación, pásala en `comparar_con`.

Devuelve `spec`: la portada (`cover`), la síntesis, las cinco secciones con sus figuras ya armadas y,
junto a cada figura, un bloque `reading` vacío para su lectura, y al final las notas de método (sin
lectura). Trae además `facts`: cifras de contexto que puedes citar (la matrícula de primer año del último
año, su cambio en el período, cuántas instituciones la dictan y la concentración del mercado).

**Guarda `spec` tal cual en un archivo JSON**, completo, antes de escribir nada: sin resumirlo, sin
redondear, sin reordenarlo y sin copiar sus valores a un script. Las lecturas se escriben después **en ese
mismo archivo**, en los bloques `reading`. El spec viene firmado (`huella`) y el compositor comprueba que
sea el que entregó el servicio: sólo `title`, `subtitle` y el texto de las lecturas son tuyos; cualquier
otro cambio hace que se niegue.

### Los grupos de instituciones

Una carrera grande se dicta en decenas de instituciones: compararlas una por una no se lee. Las figuras de
la sección 2 y los desenlaces de la 4 comparan **grupos de instituciones**, formados por el puntaje y el
origen social de sus entrantes («selectiva acomodada», «puntaje medio, origen vulnerable», «puntaje bajo
(masivas y otras)»…). **No son tipos de institución**: no escribas «las universidades privadas» ni «las
estatales» por un grupo. Escribe el nombre del grupo tal como viene.

La última fila de esas figuras, separada, es el **valor nacional de la carrera**, calculado sobre todos sus
estudiantes: no es el promedio de los grupos.

### Lo que traen los `groups`

Cada figura trae a su lado **`groups`**, con los órdenes y los grupos ya calculados. Son los mismos que en
el reporte regional; aquí las filas son instituciones, grupos de instituciones, regiones o vías, según la figura.

| Figura | Claves |
|---|---|
| Barras (`reparto`, `vias`, `conviven`, `primera_gen`, `carreras_previas`, `reconversion`, `ingresos`, `retencion`) | `rank`; `above_reference`, `at_reference`, `below_reference` cuando hay valor nacional; `zero`, `no_data`, `small_sample`. |
| Series (`primer_anio`, `ritmo`, `control`, `dependencia`, `financiamiento`, `arancel`, `canales`) | `sites[]` (cada serie con `first`, `last`, `peak`, `low`, `change_full`, `change_window`, `largest_rise`, `largest_fall`, `runs`), `window`, `rank_change_*`, `rank_longest_run`. |
| Pares (`origen_social`: colegio pagado arriba, prioritario abajo) | `rank_a`, `rank_b`; `above_reference` y `below_reference`, cada uno con su lista para `a` y para `b`. |
| Partidas (`genero`, `nivel_socioeconomico`, `edad`, `desenlaces`) | `rank_<tramo>` (`rank_mujeres`; `rank_joven`, `rank_medio`, `rank_adulto_25_29`, `rank_mayor_30`; `rank_titula`, `rank_otra_carrera`, `rank_sigue`, `rank_sin_titulo`), `above_reference`, `below_reference`, `small_sample`. En el nivel socioeconómico las filas son años. |
| Rangos (`escalera`) | `rank_mid`, `rank_box_width`, `rank_upper_tail`, `not_robust`. |
| Plano (`mapa_social`) | `quadrants` (las instituciones de cada cuadrante, de la más grande a la más chica; el nombre de cada uno en `quadrant_labels`), `on_reference`. |

En una serie, cada línea de `sites` es una serie de la figura, aunque no sea una sede: en «De qué colegios
vienen» es una dependencia; en «Cuánto cuesta», un tipo de institución.

**No toques la portada ni las figuras.** Tu trabajo son los bloques `reading`.

## 2 · Escribe las lecturas

Cada bloque `reading` tiene dos campos, y la diferencia entre ellos es la regla más importante:

- **`text`: lo que las cifras muestran.** Hechos que se leen en la figura de al lado, con sus números.
- **`compatible`: una explicación que las cifras no prueban**, si hace falta. Se publica separada y
  rotulada como «Explicación compatible». Nunca la mezcles con `text`.

Si para una figura no hay nada que decir que la figura no diga ya, **deja el bloque vacío**: no se publica.

### Los títulos son neutros; el titular va en la lectura

Las secciones y las figuras traen títulos fijos y neutros («Quién reúne la matrícula», «Cuánto cuesta»).
**No los cambies.** Lo que la figura dice —el titular— va en la **primera frase de su lectura**: «Tres
instituciones reúnen una cuarta parte de la matrícula de primer año» y no un título nuevo. Así el titular
pasa por el control de cifras del compositor, y el título no promete algo que la figura no muestra.

### Las reglas editoriales

1. **Toda cifra sale del spec.** El compositor revisa cada número de tus lecturas contra los datos que
   entregó el servicio, y **se niega** si encuentra uno que no está. Un número redondeado («9» por 9,3) no
   pasa: escribe el valor tal como viene. No calcules diferencias, sumas ni razones por tu cuenta.
   **La cifra va con su institución, grupo o región**, escrito tal como viene en la figura.
2. **Los órdenes y los grupos se copian de `groups`; no se deducen.** «Las tres que más reúnen», «los
   grupos sobre el país», «la región que menos retiene»: cada frase así nombra un grupo, y las filas que
   pones en él son las de `groups`, en ese orden. Dos filas con el mismo valor comparten puesto: dilo.
3. **Lo que dices de una serie también se copia de `groups`.** «Creció todos los años» sólo si hay un
   tramo en `runs`; «su máximo fue en 2021», de `peak`; «la que más creció» dice en qué (número o
   porcentaje) y en qué período.
4. **Muestras chicas, sin lecturas fuertes.** Una fila en `small_sample` o con «~» (`not_robust`) se puede
   nombrar, pero no sostiene el relato.
5. **La referencia es el país**, no el promedio de las filas.
6. **El universo es la carrera en todas las instituciones que la dictan.** Una figura que sólo cuenta a
   quienes rindieron la PAES o entraron por la admisión centralizada lo dice en su subtítulo: repítelo en
   la lectura («de quienes entraron por la admisión centralizada»).
7. **Cada cifra tiene su fuente y sus años.** El subtítulo dice qué años cubre; cítalos de ahí. Una cifra de
   un año dice su año, no «hoy».
8. **Coma decimal y punto de miles**, como en Chile: 12,1% y 11.426.
9. **Sin jerga de la casa.** Nada de «pack», «artefacto», nombres de reglas ni códigos de criterio.

### Cómo escribir la síntesis

Escríbela al final. Su bloque `findings` trae los hechos candidatos, cada uno con su sección:

| Hecho | Qué dice |
|---|---|
| `tamano` | Cuánto cambió la matrícula de primer año en la ventana (`change_window`). |
| `reparto` | Las instituciones que más matrícula reúnen, con su puesto. |
| `desenlaces` | Cuántos se titulan en la carrera en el país, y de qué cohortes. |
| `retencion` | La retención nacional y las regiones que menos retienen. |

- **De 3 a 5 viñetas**, cada una en una línea que empieza con «- » y termina con su sección: «(§1)».
- **Sólo hechos de `findings`** o de `facts`, con sus cifras tal como vienen. Si un hecho no viene, no lo
  reemplaces con otro.
- **Sin interpretación**: la síntesis no lleva `compatible`.

### Cómo leer la sección 1, «El mercado»

- **Dos fuentes que no se suman.** La serie de cuántos entran es la del CNED, un conteo por programa; el
  reparto y las vías cuentan personas, desde los registros del MINEDUC/SIES. No compares una cifra de una
  con una de la otra.
- **El reparto es de toda la ventana** (lo dice el subtítulo), no del último año, y muestra sólo las
  mayores: el resto de las instituciones no está en la figura.
- **Un índice dice ritmo, no tamaño.** «El ritmo frente al sistema» y «Frente a otra carrera» ponen a cada serie
  en 100 el año base (lo dice el subtítulo): una curva más alta creció más en proporción, no tiene más
  estudiantes. Cita los valores del índice tal como vienen («llegó a 255»); no escribas cuántas veces creció una
  más que otra: es una razón que el spec no trae.
- **La carrera de control no es una competidora:** es una vara del mismo contexto. Si las dos curvas se separan,
  el crecimiento es propio de la carrera; por qué, va en `compatible`.
- **Las vías son excluyentes:** cada entrante está en una sola, y por redondeo pueden sumar 99 o 101. «Ya
  titulados de otra carrera», «de otra carrera, misma institución» y «de otra institución» no vienen del
  colegio: no los cuentes como recién egresados.

### Cómo leer la sección 2, «Quién entra»

- **El plano dice dónde cae una institución, no qué vale.** Usa el nombre de `quadrant_labels` y las
  instituciones de `quadrants`. No escribas «la más exigente» ni «la mejor».
- **«Cuántos entran a cada grupo» reparte a los entrantes de las instituciones agrupadas** (lo dice el
  subtítulo); suma 100 entre los grupos y no incluye a las pocas instituciones sin grupo.
- **«Origen social por grupo» pone dos cifras por fila:** arriba el % de colegio pagado, abajo el % prioritario.
  Son dos porcentajes de los mismos entrantes, que no se suman ni se restan en la lectura.
- **El nivel socioeconómico cubre sólo a los recién egresados**: quienes entraron el año siguiente a salir del
  colegio, que son la parte de los entrantes que dice el subtítulo. Escríbelo así; no es el alumnado completo.
- **El eje del origen social es una resta:** % de colegio pagado menos % prioritario, en puntos (pp). Un
  valor negativo dice que tiene más prioritarios que alumnos de colegio pagado, no que «es pobre».
- **«Particular pagado» es una categoría administrativa**, no un nivel de ingreso. **Prioritario y primera
  generación no se suman.**
- **Primera generación es de los años que dice el subtítulo** y de quienes respondieron la ficha DEMRE:
  escribe esos años, nunca «hoy».
- **Una asociación no es un mecanismo:** que un grupo tenga más prioritarios y menos puntaje no dice por
  qué. Si quieres proponer una razón, va en `compatible`.
- **Las cuatro dependencias de «De qué colegios vienen» no suman 100%**: faltan las de menos peso y los colegios sin dato. No completes la diferencia ni la atribuyas a una de ellas.
- **Cuántos entran ya titulados lo dice «Por dónde entran»**; «Quién recibe a los ya titulados» sólo los
  reparte entre instituciones. No compares sus cifras: se calculan con ventanas y registros distintos.
- **«De qué carreras vienen» cuenta personas**, no porcentajes: compara las carreras entre sí, no con otra figura.

### Cómo leer la sección 3, «Quién paga»

- **Gratuidad y «algún beneficio» no se suman:** el segundo incluye al primero.
- **El arancel está en pesos del último año de la serie** (lo dice el subtítulo), así que los años se
  pueden comparar entre sí. Es la mediana de cada tipo de institución, no el arancel de una en particular.

### Cómo leer la sección 4, «En qué termina»

- **La escalera cubre a quienes entraron por la admisión centralizada** con PAES. Una institución con
  «~» tiene menos de 30 puntajes: va sin caja.
- **Los desenlaces describen a quienes entraron hace una década** (las cohortes del subtítulo). Escribe
  «de quienes entraron entre…», nunca «hoy se titula el X%». **Titularse en otra carrera** es cambiar de
  rumbo sin abandonar: no lo leas como fracaso.
- **Todos los grupos pueden quedar sobre el país (o bajo él).** El valor nacional cuenta a todos los
  estudiantes, también a los de instituciones que no caen en ningún grupo: no es el promedio de las filas.
- **Una titulación baja no prueba una admisión menos selectiva**: también son compatibles las carreras
  más largas, el trabajo en paralelo y el cambio de institución. Eso va en `compatible`.
- **Los ingresos son de mifuturo**, un promedio de quienes se titularon de la carrera en el tipo de
  institución que dice el subtítulo, con su corte: no es lo que ganará quien entra hoy.

### Cómo leer la sección 5, «Territorio y acceso»

- **La retención es por región de egreso:** de los egresados de cada región que entran a la carrera,
  cuántos la estudian en su región. Una retención baja puede ser falta de oferta en la región; los datos
  no dicen cuál es la causa.
- **Los canales suman 100% cada año**: un canal que sube le quita peso a otro, aunque no pierda estudiantes.

## No proyectes como si fuera dato

- **No proyectes como si fuera dato.** El saber describe lo registrado. «Si sigue la tendencia, X pasará a
  Y» sólo va declarado como supuesto —qué ritmo, de qué años, y que no es un dato del saber—, nunca en la
  primera frase ni como conclusión.

## 3 · Compón

**Primero, comprueba el compositor:** `python3 construir_figura.py --version` tiene que responder la
versión que pide el spec (`requires_composer`) o una mayor. Si no, el plugin está desactualizado: dilo,
pide actualizarlo y **no publiques** la página.

    python3 <carpeta de la skill graficar-la-matricula>/assets/construir_figura.py --entrada reporte.json --salida reporte.html

- **Si responde con el nombre del archivo**, el reporte está listo.
- **Si se niega (código 2)**, dice qué lectura cita qué cifra que no está. Corrige esa lectura y vuelve a
  componer.
- **Si dice que «el spec no es el que entregó el servicio»**, el archivo no es copia fiel del spec: vuelve a
  pedir la herramienta, guarda su `spec` tal cual y escribe las lecturas otra vez sobre él.
- **Si dice que «esta versión del plugin no conoce la forma»**, el servicio es más nuevo que el plugin: no
  publiques nada y pide actualizar el plugin.
- **Una figura que no se puede dibujar sale como tabla** y el reporte sigue: dilo en tu respuesta.

## 4 · Entrega

- **Si puedes publicar una página** (un Artifact), publica `reporte.html` tal cual.
- **Si no puedes**, entrega el archivo.

No lo conviertas en un dashboard ni redibujes sus figuras: el compositor verifica las cifras de las
lecturas y cada figura lleva sus avisos.

En tu respuesta, en dos o tres frases, di qué cubre el reporte y qué deja fuera: las notas de método lo
dicen (la titulación de cohortes recientes, la competencia entre instituciones y los colegios que se
disputan). Para la competencia, ofrece `competencia_carrera`, que trae la matriz de sustitución, fuera del
reporte.
