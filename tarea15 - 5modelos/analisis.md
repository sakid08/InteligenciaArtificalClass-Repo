# 🔍 Estudio de Desempeño en Modelos Compactos de Inteligencia Artificial

## Propósito del Ejercicio

Esta actividad tuvo como finalidad analizar las competencias de 5 sistemas de IA de escala reducida (phi3:mini, gemma:2b, tinydolphin, tinyllama, qwen:0.5b) para interpretar y generar respuestas a interrogantes concretas derivadas de un programa académico de educación superior (Materia: Inteligencia Artificial, Código: SCC-1012).

La valoración se enfocó en tres dimensiones principales: **exactitud de contenido**, **cumplimiento de directrices** y **consistencia lógica** en las salidas proporcionadas.

---

## Cuadro Resumen de Resultados

Para facilitar una revisión visual expedita del comportamiento en cada ítem, se adoptó un esquema de colores semafóricos.

| Modelo | P1 (Propósito) | P2 (Algoritmo A*) | P3 (Inferencia) | P4 (SBR) | P5 (Usos) | Resultado Final |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **phi3:mini** | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | **Desempeño Sobresaliente** |
| **gemma:2b** | 🟡 | 🟡 | 🔴 | 🔴 | 🟢 | **Resultados Heterogéneos** |
| **tinyllama** | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | **Falla Severa (Alucinaciones)** |
| **tinydolphin** | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | **Falla Severa (Estructura)** |
| **qwen:0.5b** | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | **Falla Severa (Sin Respuesta)** |

**Significado de los colores:**
* 🟢 **Verde:** Respuesta ajustada al contexto y precisa según el contenido temático.
* 🟡 **Amarillo:** Respuesta aceptable en parte, imprecisa o demasiado general.
* 🔴 **Rojo:** Respuesta errónea, con invenciones (alucinaciones), o ausencia de respuesta pertinente.

---

## Evaluación Pormenorizada por Sistema

### 🥇 Mejor Desempeño Global: phi3:mini

Este modelo evidenció una habilidad notable para incorporar el marco de referencia del programa y contestar con adecuación.

* **P1 (Propósito):** Interpretó de manera integral la finalidad del curso ("formar al profesional", "modelado matemático", "solución de problemas complejos").
* **P2 (A*):** Ofreció la definición más completa, incorporando nociones de "búsqueda", "trayectoria", "heurística" y "reducción de coste".
* **P3 (Inferencia):** Diferenció acertadamente: la inferencia no monótona admite que las conclusiones se modifiquen ante datos novedosos.
* **P4 (SBR):** Reconoció los elementos principales ("base de conocimiento" y "reglas"), si bien no citó explícitamente el "mecanismo de control".
* **P5 (Usos):** Enumeró las 6 aplicaciones esperadas y las complementó con breves explicaciones (a pesar de ciertos errores de escritura).

---

### 🥈 Resultados Desiguales: gemma:2b

Este sistema completó adecuadamente ciertas actividades sencillas de recuperación de información, pero mostró limitaciones en la explicación de nociones abstractas.

* **P1 (Propósito):** Proporcionó una respuesta válida pero genérica, menos adaptada al programa que `phi3`.
* **P2 (A*):** Explicación demasiado breve ("hallar las rutas más cortas"). Aunque correcta, careció de la profundidad esperada en un contexto universitario.
* **P3 y P4 (Inferencia y SBR):** Sus respuestas fueron imprecisas y conceptualmente equivocadas (por ejemplo, asociar "múltiples lógicas" a la inferencia no monótona).
* **P5 (Usos):** **Logro completo**. Listó las 6 aplicaciones de manera clara y exacta.

---

### ❌ Falla Grave (Alucinaciones): tinyllama

Este modelo no solo erró en sus respuestas, sino que **generó información ficticia** (alucinó) ajena por completo al contenido del programa.

* **P2 (A*):** Error significativo. Describió A* como una técnica para "configuración de ventanas" y lo mezcló con conceptos de inferencia no monótona.
* **P3 (Inferencia):** Omitió por completo la pregunta.
* **P4 (SBR):** Alucinación notable. Creó una noción de "siete símbolos" y la vinculó con "HTML" y "sitios web".
* **P5 (Usos):** Mencionó 6 ítems, pero *ninguno* coincidía con la lista del Tema 4. Generó una enumeración inventada.


---

### Falla Grave tinydolphin y qwen:0.5b

Ambos sistemas fracasaron en el requisito más elemental: seguir la instrucción de "responder las 5 preguntas".

* **tinydolphin:** No contestó las preguntas. En su lugar, produjo un resumen del programa, pero lo hizo de manera incorrecta, combinando contenidos de distintos temas (ejemplo: ubicó "reglas y búsqueda" en el Tema 2, correspondiente al Tema 3).
* **qwen:0.5b:** No generó respuestas. Simplemente repitió las preguntas y, además, asignó de modo erróneo los números de los temas (por ejemplo, indicó que A* correspondía al Tema 2).

**Síntesis:** Estos modelos no lograron procesar la consigna (Preguntas + Contexto) y no superaron la evaluación.

---

## 📌 Reflexiones Finales del Ejercicio

1.  **La Disparidad entre Modelos es Notable:** No todos los sistemas "compactos" poseen las mismas capacidades. `phi3:mini` mostró habilidades de razonamiento contextual que lo sitúan muy por encima del resto.
2.  **Alucinación versus Ambiguidad:** Resulta más sencillo identificar un modelo "deficiente" (como `tinyllama`) que inventa respuestas incongruentes, que uno "mediocre" (como `gemma:2b`) que ofrece salidas vagas pero aparentemente válidas.