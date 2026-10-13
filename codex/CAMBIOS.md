# Cambios · Matrícula de Educación Superior

<!-- Generado al derivar el paquete desde cambios.yaml. No editar a mano. -->

Qué cambia para quien usa este saber, versión por versión. Lo que corre de verdad el servicio lo dice su herramienta `ver_cambios`; esto es la copia del paquete.

## v0.31.0 · 2026-10-13

La matrícula de primer año de una carrera, 2005–2025, por sede y sumada en una región: herramienta nueva primer_anio y su figura, figura_primer_anio. Responde «la evolución de la matrícula de primer año de Enfermería en La Araucanía». La serie es la del CNED, que recibe el reporte de cada institución de forma voluntaria: un año que una sede no reportó no se rellena con otra fuente. Al sumar una región, si la sede que falta pesaba menos del 5% el año se suma sin ella y se dice; si no, queda sin total. La respuesta dice qué tipos de institución trae la serie, que no siempre son todos. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_primer_anio`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `primer_anio`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `figura_primer_anio`, `primer_anio`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-13-lab`

## v0.30.1 · 2026-10-13

Corrección: la figura de la lista de espera existía pero el agente no la encontraba. Al pedirla, tomó la figura de preferencias y concluyó que no había otra. Ahora cada figura del reporte nombra a las demás de su sección, y la definición de la lista de espera dice cómo pedir su figura (figura_region con «lista_espera»).

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-13-lab`

## v0.30.0 · 2026-10-13

Nueva cifra por sede: de quienes la pusieron como primera preferencia y se matricularon en ella, cuántos entraron desde la lista de espera, cuando otros seleccionados no se matricularon (en preferencias, ficha_sede y una figura nueva en la sección 6 del reporte, lista_espera). Mide la presión por el cupo, no rechazo ni calidad; en el país es 18,5%, y subió con la PAES: 14% en 2021–2022 y 20–23% desde 2023. Corrección: los convencidos se cuentan ahora por persona y no por vía de postulación. Quien postuló por varias vías contaba varias veces; el país pasa de 64,9% a 63,8%, ninguna sede se mueve más de 4 puntos, y dos sedes quedan bajo el mínimo de 150. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-13-lab` · antes `2026-10-11b-lab`

## v0.29.0 · 2026-10-13

Las herramientas regionales dicen, sede por sede, si su institución adhiere a la gratuidad (`adhiere_gratuidad` en acceso_equidad, panorama_region y vista_institucion, y en los grupos de la figura de gratuidad). Un 0% de gratuidad se explica como «no adhiere», en vez de quedar como un dato sin causa. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.28.0 · 2026-10-13

Las figuras de matrícula y el panorama regional dicen que su serie es de matrícula total, no de primer año. Ante «la evolución de la matrícula de primer año» de una región, el agente dice que esa serie no está y ofrece la total o los entrantes 2021–2025; para una carrera usa la serie de primer año que sí existe (CNED, 2005–2025, en panorama_carrera). Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.27.3 · 2026-10-13

Corrección: en presencia_institucional, los institutos profesionales quedaban sin comparación con su propio tipo, porque la fuente escribe su tipo con una errata en las filas por institución. Ahora un IP se compara con el promedio de los IP de la carrera, como un CFT con los CFT.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.27.2 · 2026-10-13

presencia_institucional compara la empleabilidad e ingreso de una institución con los de su propio tipo —un CFT con los CFT, un IP con los IP—, y deja el tipo que domina la carrera sólo como contexto. Antes la comparación principal era con el tipo dominante, y en carreras de IP y CFT eso hacía ver a un CFT mucho más lejos de lo que está frente a sus pares. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.27.1 · 2026-10-13

presencia_institucional muestra también las carreras donde la institución tuvo estudiantes y ya no recibe nuevos, marcadas como presencia sólo en cohortes antiguas; separa las sedes con entrantes recientes de las sedes con cohortes antiguas, porque son periodos distintos; y dice cómo calcula la titulación, para que el asistente cite esa cifra y no otra. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.27.0 · 2026-10-13

Herramienta nueva, presencia_institucional: para una institución de cualquier tipo —también un instituto profesional o un CFT, que hasta ahora el saber no podía mirar como institución—, en qué carreras está, su puesto y participación en el mercado cuando está entre las cinco primeras, cuántas sedes tiene, su titulación frente a la de la carrera y su empleabilidad e ingreso frente al tipo de institución que domina la carrera. Un nombre que corresponde a varias (la universidad, el IP y el CFT de un mismo grupo) devuelve las opciones en vez de elegir. Cubre las 69 carreras del saber, no toda la oferta de la institución.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `presencia_institucional`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `presencia_institucional`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.26.2 · 2026-10-13

Si pides el reporte de una región con el conector pero sin el plugin, en claude.ai el asistente arma un dashboard de la región con la receta del saber —datos en vivo, huecos y avisos a la vista, sin conclusiones escritas a mano— en vez de mostrar figuras sueltas. Lo presenta como un dashboard, no como el reporte, y avisa que el reporte con lecturas verificadas requiere el plugin y que cada lector necesita su propio acceso. Donde el cliente no arma dashboards, sigue mostrando las figuras una a una. Y con el plugin instalado, si pides expresamente un dashboard, también lo arma con esa receta —antes se negaba—; pedir «el reporte» sigue entregando la página del plugin. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.26.0 · 2026-10-12

Si pides expresamente un dashboard (o cualquier gráfico propio) con los datos de una región, el asistente recibe junto a los datos lo que ese gráfico tiene que conservar: cada cifra consultada en vivo al saber, los años sin dato como huecos y no unidos, los valores que no calzan marcados aparte, los avisos de cada figura a la vista, las sedes en retirada fuera de las comparaciones y ninguna conclusión escrita a mano —«crece», «la mayor»— que no salga del dato. El reporte regional sigue siendo la página del plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.25.2 · 2026-10-12

El reporte regional le dice al asistente cómo entregarse: como la página que arma el plugin, publicada tal cual. En claude.ai, donde el cliente ofrece un formato de «dashboard» para los reportes, una vez se rehízo el reporte con ese formato y perdió el control de cifras y los avisos de cada figura. Sin el plugin instalado, el asistente muestra las figuras una a una en la conversación y explica que el reporte completo requiere el plugin. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.25.1 · 2026-10-12

Corrección: al preguntar por «Técnico en Enfermería», «Técnico en Administración de Empresas», «Pedagogía en Historia» o «Pedagogía en Filosofía y Religión», el saber respondía en silencio con los datos de otra carrera —Enfermería, Administración de Empresas, Historia, Filosofía—. Ahora cada nombre llega a su carrera, también con «en» o «de» de por medio, y si la pregunta tiene palabras que ninguna carrera calza exacto, el saber muestra las candidatas en vez de elegir una.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab`

## v0.25.0 · 2026-10-11

La empleabilidad y los ingresos de cada carrera son ahora los del tipo de institución que domina su matrícula, y no siempre los de las universidades. En 18 carreras, sobre todo técnicas, pasan a ser los de los institutos profesionales; en Técnico en Enfermería el ingreso al primer año baja de $0,86 a $0,80 millones. La respuesta trae además los tres tipos que publica mifuturo —universidades, institutos profesionales y CFT—, cada uno con su peso en la carrera, y deja de advertir que el dato podía venir del grupo equivocado. Animación Digital y Mecánica Automotriz tienen retorno laboral por primera vez. Las carreras universitarias mantienen sus cifras. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11b-lab` · antes `2026-10-11-lab`

## v0.24.0 · 2026-10-11

La ficha de una sede ya no trae el indicador «primera opción por vía regular», que parecía decir cuántos pusieron la sede en primer lugar y medía otra cosa: cuántos quedaron en la lista de seleccionados de su primera preferencia, sin contar a quienes la pusieron primera y entraron desde la lista de espera (en la U. de la Frontera daba 66,8% contra 87,8% de convencidos). Para saber cuántos eligieron una sede primero, la cifra es la de convencidos, con su definición y sus límites. Los demás indicadores no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-11-lab` · antes `2026-10-10b-lab`

## v0.23.0 · 2026-10-10

El arancel y la gratuidad de cada sede son ahora los de quienes entraron en 2025, el último año disponible, y no una mediana de cinco años que mezclaba pesos de años distintos. Las dos figuras y el plano del precio dicen ese año, y los dos ejes del plano son del mismo año. El arancel que la institución informa en UF se convierte a pesos con la UF del 1 de enero, así que la U. del Desarrollo, la U. de los Andes y la U. Adolfo Ibáñez —que cobran todo en UF— tienen su arancel de 2025 en vez del de 2021. En el país el arancel mediano pasa de 4,68 a 5,52 millones y la gratuidad de 48,3% a 54,7%; algunas sedes que adhirieron hace poco a la gratuidad, como la U. de las Américas, suben mucho. Los demás indicadores no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-10b-lab` · antes `2026-10-10-lab`

## v0.22.0 · 2026-10-10

El 10% superior de las sedes («Los primeros de su curso» y su plano) se calcula ahora con el percentil del registro de notas de enseñanza media, no con la marca de la Beca de Excelencia Académica. Esa marca no existe para quienes egresaron antes de 2016 y los contaba como «no», lo que subestimaba a las sedes con más estudiantes adultos. Desde 2016 ambas coinciden casi exactamente. En el país la cifra pasa de 16,8% a 17,8%; ninguna sede baja, y algunas con muchos adultos suben más de diez puntos. Los demás indicadores no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-10-lab` · antes `2026-10-08-lab`

## v0.21.1 · 2026-10-10

Al pasar el cursor por un gráfico aparece su cifra en todas las figuras, también dentro de la conversación en Claude Desktop y claude.ai (antes dependía del tooltip del navegador, que ahí no se ve). Y cuando piden un gráfico, el saber le indica al asistente que use su propia figura —con sus huecos, sus sedes en retirada y su fuente— en vez de dibujar por su cuenta. Hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.21.0 · 2026-10-09

Las figuras se pueden ver dentro de la conversación en claude.ai, Claude Desktop y los móviles: la serie de matrícula por sede, la de la región entera y, con la herramienta nueva figura_region, cualquier figura del reporte regional por separado —la PAES por sede, las preferencias, el plano del precio…—, cada una con sus notas completas. El reporte entero sigue siendo una página. En Claude Code no cambia nada. Hay que actualizar el plugin para las skills.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `figura_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion` · aparece `figura_region`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.20.1 · 2026-10-09

Sin cambios para quien lo usa: el servicio registra qué herramienta y qué recurso se llaman, y qué cliente se conecta y si anuncia gráficos dentro de la conversación, sin guardar los argumentos. Sirve para diagnosticar las pruebas sin depender de capturas.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.20.0 · 2026-10-09

Piloto de gráficos dentro de la conversación: en claude.ai, el chat de Claude Desktop y los móviles, la serie de matrícula por sede aparece dibujada en la respuesta, sin pasar por una página aparte. Es el mismo gráfico del reporte, con la misma receta y la misma validación. En Claude Code y en cualquier cliente que no muestre estas figuras no cambia nada: el agente sigue componiendo la página como hasta ahora.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.19.4 · 2026-10-09

Sin cambios para quien lo usa en una conversación: el plugin trae ahora sus palabras clave, su categoría (educación) y una descripción larga que cuenta qué responde el saber —las dos puertas, el reporte regional y cómo trata la procedencia—, para que se encuentre y se entienda en el catálogo. El retorno laboral no se anuncia todavía: sus cifras de IP y CFT se están corrigiendo.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.19.3 · 2026-10-09

Pedir sólo algunas secciones del reporte regional, o sólo algunas instituciones en la figura de matrícula, funciona como se espera: se aceptan como lista o como texto con nombres separados por coma. Antes, un texto como «con_que_llegan» se leía letra por letra y el reporte respondía con un error por cada una. La descripción del reporte dice ahora qué secciones tiene.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.19.2 · 2026-10-09

La figura de «Los primeros de su curso» dice qué es estar en el 10% superior: la marca del registro «NEM y Percentil» que indica si el estudiante egresó en el 10% de mejor rendimiento de su promoción en su establecimiento —la misma que usa la Beca de Excelencia Académica—. Las respuestas en texto lo citan igual. Las cifras no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.19.1 · 2026-10-09

El arancel dice cómo se calcula: es la mediana del arancel de cada estudiante que entró entre 2021 y 2025, el de su carrera en su año de entrada —no el del último año ni un promedio de años—, así que cada año pesa según cuántos entraron; está en pesos nominales y deja fuera los aranceles informados en UF. Lo dicen las dos figuras que lo usan y las respuestas en texto.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.19.0 · 2026-10-09

El reporte regional queda completo. Abre con «En síntesis»: de cuatro a seis viñetas con lo principal de la región, cada una con la sección que la sostiene, escritas sobre hechos que calcula el servicio a partir de las mismas figuras. Cierra con las notas de método: por qué el género queda fuera (con su rango calculado del dato), para quién es el reporte, qué lenguaje usa, qué unidad mide y qué no responde todavía. Hay que actualizar el plugin para que la síntesis se publique como lista.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.18.0 · 2026-10-09

El reporte regional suma su octava sección, «La región en tres planos»: tres figuras que cruzan dos ejes a la vez —el puntaje PAES y el 10% superior contra el % de alumnos prioritarios, y el arancel contra la gratuidad—, con una burbuja por sede del tamaño de sus entrantes y las líneas del país partiendo el plano en cuatro cuadrantes. Los cuadrantes dicen dónde cae cada sede respecto del país, sin calificarla. Cada plano declara sus dos fuentes y sus años; uno con menos de tres sedes no se dibuja y se dice. Al pasar el cursor por una burbuja se ve la sede y sus valores. Es una figura nueva: hay que actualizar el plugin.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.17.2 · 2026-10-09

Las figuras de puntaje rotulan cada mediana con su decimal, también cuando es cero («609,0» y no «609»), como ya lo hacían las barras con los porcentajes: la figura y la lectura muestran la misma precisión. Sólo cambia el dibujo, que hace el plugin; hay que actualizarlo.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.17.1 · 2026-10-09

Los puntajes de las figuras de rangos llegan con un decimal, redondeados como los dibuja la figura: la lectura y el gráfico muestran la misma cifra (antes una lectura podía decir 567,25 donde la figura mostraba 567,3). Las lecturas tampoco encadenan paréntesis cuando el nombre de la sede ya trae la ciudad.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.17.0 · 2026-10-09

El reporte regional suma dos secciones. «Dónde los eligen» muestra, por sede, cuántos de quienes entraron por la admisión centralizada la habían puesto como primera preferencia y cuántos llegaron desplazados, y a qué institución habían puesto primero esos desplazados. «En qué termina» muestra los cuatro desenlaces de las cohortes que entraron entre 2011 y 2016: se tituló en su carrera, se tituló en otra, sigue estudiando o salió sin título. Las dos usan una figura nueva, la barra partida al 100%, con el país como última fila de referencia, y hay que actualizar el plugin para verla. Cada sección declara su fuente: las postulaciones del DEMRE y las trayectorias de titulación. La herramienta de preferencias también cita ahora esa fuente, en vez de la genérica.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.16.1 · 2026-10-09

Las barras del reporte se leen mejor: el valor de cada barra ya no queda tachado por la línea punteada del valor nacional, el eje del arancel marca «$2 M» en vez de «$2,00 M», y los porcentajes de las barras llevan siempre un decimal («76,0%»), como los escriben las lecturas. Sólo cambia el dibujo, que lo hace el plugin: hay que actualizarlo. Las cifras no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.16.0 · 2026-10-09

El reporte regional suma su quinta sección, «Cómo entran y quién paga»: por qué vía entran a cada sede —la centralizada, la de equidad y, dentro de ella, el PACE—, cuántos llegan desde la misma institución o con un título previo, cuánto cuesta y cuántos estudian con gratuidad. Cada figura dice su fuente y sus años: la equidad y el PACE sólo se registran desde 2024, y el arancel está en pesos nominales de cinco años, sin ajustar por inflación. La presencia del PACE por tipo de institución se calcula del dato: hoy la tiene el 87% de las sedes estatales del Consejo de Rectores, el 86% de las privadas del Consejo y el 15% de las privadas fuera de él.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.15.1 · 2026-10-08

Las respuestas sobre una región dejan fuera de cualquier comparación a las sedes en retirada —también de los rangos del tipo «va de X a Y»—, saben que cada indicador trae el número de estudiantes con dato y por eso su cobertura, y citan la fuente y los años de cada indicador.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab`

## v0.15.0 · 2026-10-08

Tres indicadores de las sedes se calculan ahora mejor. Alumnos prioritarios: quien egresó de un colegio subvencionado sin ficha SEP ya no cuenta como «no prioritario», porque no se sabe; el egresado de colegio particular pagado sí cuenta como «no», porque ahí la SEP no existe. En el país la cifra pasa de 39,9% a 51,1%, y el pie advierte que, si los colegios sin ficha tuvieran menos prioritarios, estaría algo sobreestimada. Primera generación ya no cuenta como tal a quien respondió «no sé» por la educación de ambos padres (56,9% a 56,1%). Y el número de estudiantes que acompaña a cada barra del 10% superior, del colegio pagado, del alumnado de la región y de los prioritarios es el de quienes tienen el dato, no el de toda la sede. Los demás indicadores no cambian.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-08-lab` · antes `2026-10-07-lab`

## v0.14.1 · 2026-10-08

Las figuras que salen del registro de egreso de enseñanza media —colegio pagado y alumnado de la región— dicen ahora su cobertura, egresos 2002–2025, que alcanza a todos los entrantes del período. La del 10% superior advierte que su registro llega a 2023; sin decirlo también aquí, no se sabía si faltaba el aviso o no había límite.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.14.0 · 2026-10-08

Cada dato dice ahora de dónde sale. Las figuras del reporte estampan la fuente de su propio indicador —el registro de egreso de enseñanza media para el colegio pagado, la ficha SEP para los prioritarios, el registro NEM del DEMRE para el 10% superior, el historial de matrícula para quienes llegan directo del colegio— en vez de una fuente genérica, y el pie del reporte las lista todas. Lo que todavía está calculado de forma imperfecta se dice en la propia figura: que el n es el de la sede completa, que quien no tiene ficha SEP cuenta como no prioritario, que el registro NEM llega a los egresos de 2023. Las respuestas en texto traen la misma información: la fuente y los años de cada indicador.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.13.1 · 2026-10-08

Corrección: la figura de primera generación en la universidad decía cubrir a quienes entraron entre 2021 y 2025, y cubre sólo 2021–2022. El dato sale de la ficha socioeconómica del DEMRE, que dejó de preguntar la educación de los padres desde el proceso 2023. Ahora la figura dice sus años, su fuente propia y que mide sólo a quienes respondieron la ficha, y la lectura no puede presentarla como el alumnado actual.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.13.0 · 2026-10-08

El reporte regional suma su cuarta sección, «De qué origen vienen»: cuántos puntos de PAES separan a quienes egresaron de colegio particular pagado del resto, cuántas veces más se van a la Metropolitana, y por sede cuántos vienen de colegio pagado —en porcentaje y en personas, que ordenan distinto—, cuántos fueron prioritarios y cuántos son primera generación en la universidad. Las comparaciones con el país se calculan del dato en vez de escribirse: la brecha de puntaje va hoy de 68 a 157,5 puntos según la región, y no «nunca baja de 85» como decía el reporte anterior. Dice que es una asociación y no un mecanismo, y que «particular pagado» es una categoría administrativa, no un nivel de ingreso.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.12.0 · 2026-10-08

El reporte regional suma su tercera sección, «El mercado»: cuántos egresados de la región se quedan a estudiar en ella, adónde se van los demás, de dónde llegan los que vienen, a qué universidades de la capital se va cada tramo de la migración y de dónde es el alumnado de cada sede. Abre con un bloque de cifras —la retención, los entrantes contra los egresados que siguen a la universidad y el balance entre ambos, con su conclusión— que escribe el servicio y no el asistente. Dice cómo se cuentan las cifras y qué queda fuera, y en una región con dos mercados (Los Lagos) lo advierte. Las cifras son las del reporte regional que existía antes.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.11.0 · 2026-10-08

La evolución de la matrícula de muchas sedes se lee ahora en un solo gráfico: todas las sedes en el mismo eje, con el nombre de cada una al final de su línea, en vez de un panel por sede que impedía compararlas. Las líneas son rectas —no se suavizan entre años— y siguen cortándose donde falta un año. En una región con más de quince sedes se nombran las quince más grandes y el pie dice cuántas quedan sin nombre.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.10.2 · 2026-10-08

Una figura en que todas las sedes valen cero ya no deja una caja vacía con un pie que habla de una línea que no se dibuja: dice en una línea que no hay barras y cuál es el valor del país.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.10.1 · 2026-10-08

Correcciones que encontró el primer uso de la sección 2. Si el plugin instalado es más antiguo que el servicio y no conoce una figura nueva, el reporte ya no se publica a medias con tablas vacías: dice que hay que actualizar el plugin. La portada ya no repite la ciudad de una sede que la trae en el nombre («U. de Concepción (Concepción) (Concepción)»), y una figura en que todas las sedes valen cero lo dice así, sin dibujar un eje vacío.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

## v0.10.0 · 2026-10-08

El reporte regional suma su segunda sección, «Con qué llegan», con tres figuras: el puntaje PAES de quienes entraron a cada sede —no el promedio, sino la distribución completa, contra la mediana del país—, la carrera de mayor puntaje en cada sede, que suele ser Medicina y explica por qué el extremo alto se despega, y cuántos venían entre el 10% superior de su colegio. La PAES se declara como lo que es: cubre a quienes la rindieron y entraron desde 2023, no al alumnado completo. Las cifras son las mismas del reporte regional que existía antes, y los órdenes que una lectura cita —la mediana más alta, la caja más angosta— vienen calculados.

- Herramientas: `acceso_equidad`, `carreras_tope`, `competencia_carrera`, `desenlaces_carrera`, `ficha_sede`, `figura_matricula`, `figura_matricula_region`, `flujos_region`, `listar_carreras`, `listar_cobertura`, `obtener_criterios`, `panorama_carrera`, `panorama_region`, `perfil_migrante`, `preferencias`, `preguntas_abiertas`, `quien_entra`, `reporte_region`, `sedes_de_la_carrera`, `ver_cambios`, `vista_institucion`
- Skills: `analizar-una-region`, `empezar-aqui`, `explorar-una-carrera`, `graficar-la-matricula`, `reportar-una-region`
- Datos: `2026-10-07-lab`

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
