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
2. **Sin ranking de uno.** «La más grande», «la que más» sólo si comparaste **todas** las barras de la
   figura. Con una sola sede no hay ranking: se describe.
3. **Muestras chicas, sin lecturas fuertes.** Una sede con pocos entrantes (mira la figura «Cuántos
   entran» y el `n` de cada barra) puede tener porcentajes extremos por azar. Nómbrala si hace falta,
   pero no construyas el relato sobre ella.
4. **La referencia es el país, no el promedio de las sedes.** La línea punteada es el valor nacional,
   calculado sobre todos los estudiantes. Compara contra ella, no contra «el resto de la región».
5. **Las sedes en retirada se declaran una vez, en la portada**, y no vuelven a aparecer. No las nombres
   en las lecturas de las secciones.
6. **El universo son las universidades**, en pregrado. Si una lectura podría leerse como «todos los que
   estudian en la región», di que son universidades: los institutos profesionales y los CFT no están.
7. **Coma decimal y punto de miles**, como en Chile: 12,1% y 11.426.
8. **Sin jerga de la casa.** Nada de «pack», «artefacto», nombres de reglas ni códigos de criterio.

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
