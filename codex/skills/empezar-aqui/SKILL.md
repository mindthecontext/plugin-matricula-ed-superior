---
name: empezar-aqui
description: Orienta a quien acaba de instalar Matrícula de Educación Superior y no sabe qué pedirle — «¿qué puedes hacer?», «¿por dónde empiezo?», «ayuda». Presenta lo que este saber responde y dice desde el principio lo que NO cubre.
---

# Empezar aquí

Esta skill es el esqueleto que `crear_saber.py` dejó al crear «matricula-ed-superior». Sustitúyela por lo que
este saber sepa hacer de verdad.

## Lo que conviene que diga una primera skill

**Qué responde**, en el idioma de quien pregunta y no en el del sistema.

**Qué NO responde**, dicho desde el principio y no cuando alguien se estrella. Una frontera
declarada temprano ahorra la conversación de después.

**Con qué se responde** — de dónde sale lo que afirma, para que quien lo lea pueda juzgarlo.

## Cómo se publica un cambio

Editas, abres un PR, lo fusionas, y etiquetas:

    git tag v0.2.0 && git push origin v0.2.0

El tag comprueba la convención, comprueba que `paquete/` coincide con su fuente, y publica. El
catálogo NO se mueve solo: publicar no promueve.
