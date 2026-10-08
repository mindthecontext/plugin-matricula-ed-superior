# Cambios · Matrícula de Educación Superior

<!-- Generado al derivar el paquete desde cambios.yaml. No editar a mano. -->

Qué cambia para quien usa este saber, versión por versión. Lo que corre de verdad el servicio lo dice su herramienta `ver_cambios`; esto es la copia del paquete.

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
