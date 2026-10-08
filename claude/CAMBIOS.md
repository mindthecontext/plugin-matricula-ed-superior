# Cambios · Matrícula de Educación Superior

<!-- Generado al derivar el paquete desde cambios.yaml. No editar a mano. -->

Qué cambia para quien usa este saber, versión por versión. Lo que corre de verdad el servicio lo dice su herramienta `ver_cambios`; esto es la copia del paquete.

## v0.9.0 · 2026-10-08

Las lecturas de la serie de matrícula, también calculadas. Junto a la figura «Cómo han cambiado», el servicio entrega ahora lo que una lectura dice con palabras: cuánto cambió cada sede —en número y en porcentaje, en todo su período y entre 2019 y 2025—, su máximo y su mínimo, su mayor alza y su mayor caída, los años en que subió o bajó todos los años, y quién cambió más. El asistente lo copia en vez de deducirlo: «la que más creció» dice si es en número o en porcentaje, y «sin pausa» sólo se escribe si fue así año a año. Un registro que no calza no cuenta como máximo ni como salto, y una sede que partió de muy pocos estudiantes no aparece como la que más creció en porcentaje.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.8.0 · 2026-10-08

Lecturas más confiables en el reporte regional. Junto a cada figura de barras, el servicio entrega ahora los órdenes y los grupos ya calculados —qué sedes reciben más, cuáles quedan sobre, en o bajo el valor del país, cuáles valen cero y cuáles tienen pocos estudiantes—, y el asistente los copia en vez de deducirlos. Era la forma en que una lectura podía decir algo falso con todas sus cifras correctas: «las tres sedes con más entrantes» nombraba una que no lo era. Además, cada sede se llama igual en todo el reporte; en las regiones con ciudades partidas, la serie y las barras la nombraban distinto.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.7.0 · 2026-10-08

El primer reporte: la nueva skill `reportar-una-region` arma una página con la portada de la región —sus sedes universitarias y, declaradas una sola vez, las que están en retirada— y la primera sección, «Quiénes son», con siete figuras: cuántos entran, en cuántas carreras, cómo cambió la matrícula de cada sede, a qué edad llegan y en qué jornada estudian, cada una contra el valor del país. Las cifras son las mismas del reporte regional que existía antes. Las lecturas que acompañan a cada figura las escribe el asistente, separando lo que las cifras muestran de lo que sólo es una explicación posible, y ningún número del texto puede ser uno que el servicio no entregó: si lo es, el reporte no se publica. Las demás secciones llegarán una a una. La herramienta nueva es `reporte_region`.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `reporte_region`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region` · aparece `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.6.0 · 2026-10-08

Una segunda figura: la matrícula de una región entera desde 2007, con una línea para el total y una banda para lo que aportaban las sedes que están en retirada. Se ve cuánto pesaban y cómo se fueron cerrando, y por eso la región crece más sin ellas (en Ñuble, +2,1% con todas y +14,1% sin las en retirada, entre 2019 y 2025). Un año que se sumó sin una sede va con el punto hueco, y uno en que faltaba demasiado queda sin punto; el pie dice qué sede faltó y cuánto pesaba. La herramienta nueva es `figura_matricula_region`.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `figura_matricula_region`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`
- Datos: `2026-10-07-lab`

## v0.5.0 · 2026-10-08

Las figuras de matrícula las arma ahora el servicio: la nueva herramienta `figura_matricula` entrega la serie de las sedes de una región —o de las instituciones que se pidan— lista para dibujar, con los años sin registro y los valores que no calzan ya declarados, las sedes en retirada marcadas y los nombres de las instituciones escritos como se escriben. Quien pregunta recibe la misma figura que antes, pero ya no depende de que el asistente copie bien diecinueve cifras por sede.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `figura_matricula`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`
- Datos: `2026-10-07-lab`

## v0.4.0 · 2026-10-08

La evolución de una región, ahora entregada por el servicio: `panorama_region` trae la serie de matrícula regional desde 2007, con todas las sedes y sin las que están en retirada, y el crecimiento de cada una (en La Araucanía, 2019→2025: +11,8% con todas, +14,5% sin las en retirada). Un año en que a una sede le falta el registro no se suma en silencio: si lo que falta pesa, queda sin total; si no, se suma y se dice. Cada sede trae su serie, así que la figura de una región se arma con una sola consulta. «En retirada» pasa a significar lo que dice el registro —una sede que ya casi no recibe estudiantes nuevos— y no «una sede chica», que ahora es un aviso aparte; cambia la marca en tres regiones (Arica, Metropolitana y Los Lagos). Las respuestas declaran sus ventanas, la matrícula trae su propia fuente y ninguna respuesta lleva ya vocabulario interno.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`
- Datos: `2026-10-07-lab`

## v0.3.0 · 2026-10-07

La primera figura: la nueva skill `graficar-la-matricula` dibuja cómo evolucionó la matrícula de una o varias sedes universitarias entre 2007 y 2025, y la entrega como una página que se lee en claro, en oscuro y en un teléfono. Una serie con años sin registro se dibuja cortada, sin unir el hueco, y un valor que no calza con sus años vecinos se muestra aparte y se declara, sin tratarlo como tendencia. Si algo de eso no viene declarado, la figura no se dibuja y se entrega la tabla. Las sedes en retirada no se comparan: se nombran al pie. La fuente se toma de la herramienta y nunca se escribe a mano. Las herramientas y los datos no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula` · aparece `graficar-la-matricula`
- Datos: `2026-10-07-lab`

## v0.2.0 · 2026-10-07

El saber trae ahora tres skills que ordenan cómo se responde, en vez de una plantilla: `empezar-aqui` presenta lo que cubre con la cobertura consultada en vivo y dice desde la primera respuesta lo que no cubre; `explorar-una-carrera` empieza por el tipo de mercado —universitario, mixto o de institutos profesionales y CFT— antes de cualquier cifra, pone la cobertura antes del dato y lee la matriz de sustitución como lo que es, los flujos mayores del país y no todos; `analizar-una-region` recorre el mercado universitario de un territorio sin promediar percentiles entre sedes ni rellenar los huecos de una serie. Las herramientas y los datos no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera` · aparece `analizar-una-region`, `explorar-una-carrera`
- Datos: `2026-10-07-lab`

## Línea base · v0.1.0 · 2026-10-07

Primera versión del saber. Responde quién estudia qué en la educación superior chilena, dónde, con qué perfil y en qué termina, sobre registros administrativos públicos —SIES, DEMRE, MINEDUC y el retorno laboral de mifuturo—, con la procedencia y el universo declarados en cada respuesta. Tiene dos puertas con universos distintos: por REGIÓN, el mercado universitario de un territorio (16 regiones, nueve herramientas); por CARRERA, la educación superior completa, con institutos profesionales y CFT (69 carreras, seis herramientas), incluida la matriz de sustitución —de quienes dejaron una institución, a cuál llegaron—. Además expone sus criterios de interpretación y las preguntas que declara no poder decidir. Lo que no es derivable se dice en vez de aproximarse. Advertencia de esta versión: el retorno laboral de las carreras de IP y CFT puede venir sobreestimado (~11%) porque la evidencia se compiló antes de un arreglo; la herramienta lo avisa en la propia respuesta.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `empezar-aqui`
- Datos: `2026-10-07-lab`

Antes de v0.1.0 no hay registro de cambios.
