# Cambios · Matrícula de Educación Superior

<!-- Generado al derivar el paquete desde cambios.yaml. No editar a mano. -->

Qué cambia para quien usa este saber, versión por versión. Lo que corre de verdad el servicio lo dice su herramienta `ver_cambios`; esto es la copia del paquete.

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
