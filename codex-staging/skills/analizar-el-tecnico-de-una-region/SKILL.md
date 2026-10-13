---
name: analizar-el-tecnico-de-una-region
description: Responde sobre el mercado técnico-profesional de una región chilena —los institutos profesionales (IP) y los centros de formación técnica (CFT)— «¿quién compite con el CFT Santo Tomás en el Biobío?», «¿cómo le va al IP en La Araucanía?», «¿qué estudiante recibe el CFT en Temuco?», «¿cuánto cuesta y cuántos tienen gratuidad en los IP de la región?», «¿cuántos vienen del mismo grupo?». Cubre IP y CFT presenciales. NO cubre universidades (para eso, analizar-una-región) ni una carrera en todo el sistema (explorar-una-carrera).
---

# Analizar el técnico-profesional de una región

## El orden

1. **`panorama_tecnico_region(region)`** primero: quién está, cuánto matricula, su participación en su
   mercado y el perfil de sus entrantes.
2. Para una institución, **`ficha_sede_tecnica(institucion, region)`**: todos sus ejes con su `n`.
3. Lo **no presencial**, con **`a_distancia_tecnico`**, aparte.
4. Para graficar, **`figura_tecnico_region(region, figura)`** (skill graficar-la-matricula): no dibujes por
   tu cuenta.

## Una unidad es institución × ciudad × nivel

En el IP, **profesional** (carreras de cuatro años sin licenciatura) y **técnico** son mercados distintos:
el profesional compite con las universidades, el técnico con los CFT. Por eso un IP aparece dos veces,
«IP AIEP · profesional» e «IP AIEP · técnico». La participación de cada unidad es **en su mercado**
(`participacion_en_su_mercado_pct`), no en la región entera: no sumes participaciones de mercados distintos.

## Es otro estudiante: dilo

La mitad de quienes entran a un IP tiene 25 años o más, un tercio estudia de noche y muchos llegan con
estudios previos. La edad, la jornada y la trayectoria son lo central aquí, no un detalle: léelos antes
que nada, y compáralos con `nacional` del mismo mercado (`cft`, `ip_tecnico`, `ip_profesional`).

## Lo que no aplica no es un vacío

No hay PAES, vía de admisión, preferencias ni lista de espera: los IP y CFT no admiten por el sistema del
DEMRE. Si preguntan por puntajes o por «quién los elige primero», di que **no aplica** en esta puerta, no
que falta el dato. El 10% superior y la primera generación tampoco están en esta etapa.

## Lo no presencial no es de la región

Un programa a distancia tiene como sede la administrativa, no donde vive el estudiante: no está en las
unidades de la región ni en su matrícula. Si la pregunta lo necesita, `a_distancia_tecnico`, y dilo aparte.

## La continuidad dentro del grupo

`continuidad_interna` cuenta a quien venía de la misma institución **o de su grupo**: un egresado del CFT
Santo Tomás que entra al IP Santo Tomás es continuidad, no captación. Es la cifra para preguntas sobre
prosecución dentro de un holding (Santo Tomás, INACAP, San Sebastián…).

## Las reglas de siempre

- **En retirada** (`en_retirada`): menos de 30 estudiantes nuevos el último año; no se compara.
- **Sin superlativos** que no salgan de comparar la columna completa.
- **La gratuidad 0%** de una institución que no adhiere (`adhiere_gratuidad: false`) es «no adhiere».
- **Cierra con las fuentes**, desde `procedencia`, y con el universo: IP y CFT presenciales, sin universidades.
