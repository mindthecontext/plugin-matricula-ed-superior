---
description: Orienta a quien acaba de instalar Matrícula de Educación Superior y no sabe qué pedirle — «¿qué puedes hacer?», «¿qué datos tienes?», «¿por dónde empiezo?», «ayuda», «¿sirve para mi universidad?», «¿qué hay de nuevo?». Presenta lo que este saber responde con la cobertura consultada en vivo, y dice desde el principio lo que NO cubre. NO es la puerta para una consulta concreta sobre una carrera o una región.
---

# Empezar aquí

Quien llega no sabe qué preguntar. El trabajo de esta puerta es **mostrarle el terreno en su
idioma** y, en la misma respuesta, decirle dónde termina — para que no descubra la frontera cuando
ya confiaba en una cifra.

## Consulta la cobertura en vivo, no la recites

Llama `listar_carreras()` y `listar_cobertura()` antes de responder. Las cifras cambian cuando se
recompila la evidencia, y un número memorizado envejece mal. De ahí salen: cuántas carreras hay,
cuántas regiones, cuántas instituciones y qué perfil tiene cada mercado.

## Lo que este saber responde, en dos puertas

**Por región** — el mercado universitario de un territorio: quién crece y quién se estanca,
selectividad, gratuidad y equidad, cuántos egresados se quedan a estudiar ahí y hacia dónde se van
los que salen, quién llega convencido y quién desplazado.

**Por carrera** — dónde se estudia algo en el sistema completo, incluidos institutos profesionales y
CFT: quién la dicta y con qué participación, quién entra, en qué termina la cohorte, qué
empleabilidad tiene, y **de quienes pusieron 1ª a una institución, en cuál se matricularon**.

## Di la frontera en la primera respuesta

No al final, no si preguntan. Lo que este saber **no** cubre:

- educación continua y diplomados — no hay fuente pública estructurada;
- posgrado — la fuente existe, no está integrada;
- no todas las carreras: la cobertura es parcial —cuántas, lo dice `listar_carreras()`— y si la suya
  no está, se dice;
- proyecciones de demanda;
- comparaciones de puntaje cruzando 2022/2023, por el quiebre PSU→PAES.

Si dudas de una frontera, `preguntas_abiertas()` las trae con su estado y su porqué.

## Qué hay de nuevo, y qué versión responde

Si preguntan qué cambió o qué versión está activa, llama `ver_cambios()` y responde con lo que trae:
la versión que corre el servicio y lo que cada versión significa para quien lo usa. No lo
reconstruyas de memoria, y si el registro no tiene entrada para la versión en curso, dilo así.

## Las dos puertas tienen universos distintos, y eso se explica

La puerta regional cubre **universidades**; la de carrera, **la educación superior completa**. No es
una inconsistencia: son dos preguntas. Si una respuesta usa las dos, dilo — sin eso, alguien va a
comparar dos cifras incomparables y concluir que una está mal.

## Cierra ofreciendo una pregunta concreta

Una genérica no sirve. Mejor dos o tres pegadas a quien pregunta: si es de una universidad, su
institución; si es de una región, su región. Y una que luzca lo que solo este saber tiene —*«¿a
quién le pierde estudiantes la UFRO en Enfermería?»*— porque la matriz de sustitución es lo que
difícilmente encuentren en otra parte.
