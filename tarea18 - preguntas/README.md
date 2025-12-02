# 1. Preguntas a pasar por modelo


### 1.1. 01 - ¿Cuál es la proporción exacta de registros sobre "Generacion Z" frente a "Frankenstein" en el dataset (porcentaje de cada categoría)?

#### 1.1.1. Resultados Modelo 3b

Según los datos proporcionados, el porcentaje de registros sobre “Generación Z” es del 72.31% y el porcentaje de registros sobre “Frankenstein” es del 27.69%.

#### 1.1.2. Resultados Ghat gpt

	La proporción es exactamente del 50% para cada categoría, lo que indica un dataset perfectamente balanceado. 
	Tras analizar el archivo y corregir manualmente dos registros que presentaban errores de formato (líneas 85 y 185, ambas pertenecientes a "Frankenstein"), la distribución final de los 200 registros es la siguiente:

Generacion Z: 100 registros (50%)

Frankenstein: 100 registros (50%)

### 1.2. 02 -  Sin incluir los registros de El País, identifique los tres medios de comunicación que tienen la mayor cantidad de registros.

#### 1.2.1. Resultados Modelo 3b

Según los datos proporcionados, los tres medios de comunicación con la mayor cantidad de registros (sin incluir los registros de El País) son:

Aristegui Noticias: 4 registros
W Radio: 1 registro
Netflix Data: 1 registro


#### 1.2.2. Resultados Chatgpt


El medio de comunicación con la mayor cantidad de registros (excluyendo "El País") es **Milenio** con 6 registros, seguido por un empate en el segundo lugar entre cuatro medios con 4 registros cada uno.

Los tres principales medios de comunicación (con el mayor número de registros) son:
1. **Milenio** (6 registros)
2. **Reuters** (4 registros)
3. **El Universal** (4 registros)


## 03 - Determine cuál fue el día de mayor actividad noticiosa (mayor número de registros publicados) en todo el dataset y cuántos registros se publicaron ese día.

#### Ollama 3b

Según los datos proporcionados, el día de mayor actividad noticiosa fue el 16 de noviembre de 2025, con un total de 13 registros publicados.


#### Chat gpt

El día de mayor actividad noticiosa en todo el _dataset_ fue el **16 de noviembre de 2025**, con un total de **28 registros publicados**.

Este resultado se mantiene como el pico de actividad incluso tras incluir y ajustar los dos registros que inicialmente presentaron errores de formato en el archivo (los cuales estaban fechados el 9 de noviembre de 2025).


## 04 - Para la categoría "Frankenstein", calcule cuántos registros tienen una fecha de publicación anterior al 7 de noviembre de 2025.

#### LLM  3b

Según los datos proporcionados, para la categoría “Frankenstein” con una fecha de publicación anterior al 7 de noviembre de 2025, se presentan los siguientes conteos:

Twitter Trends: 1 registro (publicado el 8 de noviembre de 2025)
Entrevista Backstage: 1 registro (publicado el 7 de noviembre de 2025)
#### Chat gpt

El número de registros para la categoría **"Frankenstein"** con una fecha de publicación **anterior al 7 de noviembre de 2025** es de **34**.


## 05 - Considerando solo los registros donde el Medio es El Financiero, muestre el conteo de registros para cada categoría ("Generacion Z" y "Frankenstein").

#### Ollama 3b

Según los datos proporcionados, para el medio El Financiero, se presentan los siguientes conteos:
Generación Z: 1 registro
Frankenstein: 2 registros

#### GPT

Considerando solo los registros donde el Medio es El Financiero, muestre el conteo de registros para cada categoría ("Generacion Z" y "Frankenstein").
Frankenstein - 4
Generacion Z - 0


## 06 - Cree un string combinado con el texto de las columnas Título y Resumen solo para "Generacion Z". Muestre las cinco palabras clave más frecuentes (después de eliminar stopwords comunes en español).


#### Llama 3b

 palabra = Generación Z 
  -Generación- (3)

 palabra = to
 frecuencia = 2

 palabra = Frankenstein
  -Frank-   (1)

 palabra = tensión
 frecuencia = 2

#### chat GPT

| **Palabra Clave** | **Frecuencia** |     |
| ----------------- | -------------- | --- |
| **jóvenes**       | 18             |     |
| **análisis**      | 14             |     |
| **uso**           | 14             |     |
| **juvenil**       | 10             |     |
| **tras**          | 8              |     |

## 07 - Calcule cuántos registros de "Frankenstein" mencionan términos relacionados con la producción visual (busque "maquillaje", "vestuario", "diseño" o "estética") en su Resumen o Comentario_Reaccion.


#### Llama 3b

En el resumen, se menciona que la paleta de colores es “sombría y hermosa”, lo cual indica que se refiere al uso del tono de color en la película.

En el comentario-reaccion, no se menciona directamente el uso visual del director de fotografía, pero se puede inferir que se hace referencia a la producción visual general, ya que se describe cómo se utiliza el maquillaje, vestuario y estética en la película.
#### Chat gpt

Un total de **13 registros** de la categoría **"Frankenstein"** mencionan términos relacionados con la producción visual (**"maquillaje"**, **"vestuario"**, **"diseño"** o **"estética"**) en sus columnas de **Resumen** o **Comentario_Reaccion**.


## 08 - Con base a la informacion del archivo, responde Encuentre la diferencia neta entre: a) el número de veces que se menciona la palabra “dolor” o “tragedia” en los comentarios de Frankenstein, y b) el número de veces que se menciona “esperanza” e los comentarios de “Generacion Z”.

#### Ollama 3.2 1b

a) El número de veces que se menciona la palabra “dolor” o “tragedia”:

La palabra “dolor” se menciona una vez en el comentario de Frankenstein (relatado a Del Toro: “El dolor como motor de la monstruosidad”).
La palabra “tragedia” se menciona dos veces en los comentarios de Frankenstein (relatados a Del Toro: “La tragedia dominante de la criatura”, y también a Del Toro elogia la actuación de Actor 4 como Henry Clerval, donde se utiliza la frase “El dolor como motor de la monstruosidad”).
Por lo tanto, el número total de menciones de la palabra “dolor” o “tragedia” es 3.

b) El número de veces que se menciona el término “esperanza”:

La palabra “esperanza” se menciona dos veces en los comentarios de Frankenstein (relatados a Del Toro: “La ciencia: Es la ambición humana”, y también a Del Toro elogia la actuación de Actor 4 como Henry Clerval, donde se utiliza la frase “La voz de la generación Z en los medios tradicionales”).
Por lo tanto, el número total de menciones del término “esperanza” es 2.

#### Chat GPT

La diferencia neta entre el número de veces que se mencionan los términos relacionados con el sufrimiento en los comentarios de "Frankenstein" y el término "esperanza" en los comentarios de "Generacion Z" es de **4**.

A) Menciones de "dolor" o "tragedia" en comentarios de Frankenstein
Se encontraron 4 menciones en los 98 registros limpios.

Se añadieron 2 menciones de la palabra "dolor" provenientes de los dos registros malformados que se recuperaron.

B) Menciones de "esperanza" en comentarios de Generacion Z
Se encontraron 2 menciones de la palabra "esperanza" en los comentarios de la categoría.


## 09 - Considerando ambas categorías, determine el número total de registros que mencionan específicamente la plataforma "TikTok" en cualquier columna de texto.

#### Ollama 3.2 3b

En cuanto a la plataforma “TikTok”, se menciona la siguiente información:

- En el comentario de Frankenstein (ID: 73), no se mencionó específicamente TikTok.
- En el comentario de Generación Z (ID: 56), no se mencionaron los términos “boicot” ni “marcas que no se pronuncian”, pero se mencionó la plataforma “TikTok”.
- En el comentario de Influencers (ID: 123), se mencionó específicamente “denunciar intimidación tras apoyar las protestas” relacionado con la plataforma “TikTok”.

Por lo tanto, hay un total de 1 registro que menciona específicamente TikTok.

#### Chat GPT

El **número total de registros** que mencionan específicamente la plataforma **"TikTok"** en cualquiera de las columnas de texto es **4**.

## 10 - Calcule el número total de menciones de los actores (busque las strings "[Actor 1]", "[Actor 2]", "[Actor 3]", "[Actor 4]") en todas las columnas de texto combinadas.


#### Ollama 3.2 1b

Después de analizar la información del archivo, puedo presentar las siguientes conclusiones:

Se mencionan los siguientes actores:

- [Actor 1]: se menciona una vez en el comentario de Frankenstein (relatado a Del Toro: “El papel de las mujeres en la nueva adaptación”).
- [Actor 2]: se menciona una vez en el comentario de Generación Z (ID: 17), que es Actor 4, relato sobre “La nueva visión de la criatura de Del Toro”.
- [Actor 3]: no se mencionó.
- [Actor 4]: se menciona dos veces en los comentarios de Frankenstein (relatados a Del Toro elogia la actuación de Actor 2 como Monstruo), y también en el comentario de Generación Z, que es un registro sobre “El papel del actor Dr. Frankenstein”.

Por lo tanto, hay un total de 3 registros que mencionan los actores [Actor 1], [Actor 4] e [Actor 2].

#### ChatGPT

El **número total de menciones** de los actores específicos (`[Actor 1]`, `[Actor 2]`, `[Actor 3]`, y `[Actor 4]`) en todas las columnas de texto combinadas es **47,765**


## 11 - Identifique qué medio de comunicación tiene el Tono Promedio más bajo (más negativo) en la categoría "Generacion Z" (asumiendo que ya se calculó la columna Tono_Sentimiento).


#### Ollama 3.2 1b

En la categoría “Generación Z”, el medio de comunicación con tono promedio más bajo es Twitter Trends (ID: 48), que tiene un tono sentimiento de 1,5.

#### ChatGPT

El medio de comunicación identificado con el **Tono Promedio más bajo (más negativo)** en la categoría "Generacion Z", basado en la **columna `Tono_Sentimiento` simulada**, es **TikTok**.

| **Medio**  | **Tono Promedio (Simulado)** |
| ---------- | ---------------------------- |
| **TikTok** | **$-0.9779$**                |

## 12 - Para los registros de "Frankenstein", compare el Tono Promedio deaquellos que mencionan explícitamente a Guillermo del Toro (GDT) en el Comentario_Reaccion con el Tono Promedio de aquellos que no lo mencionan.

#### Ollama 3.2 1b

Se menciona explícitamente a GDT en los comentarios del siguiente registro:
- Frankenstein (ID: 51) - Tono Sentimiento: 0,9
- Frankenstein (ID: 123) - Tono Sentimiento: 0,8

#### Chat GPT

El **Tono Promedio** de los comentarios que **mencionan explícitamente a Guillermo del Toro (GDT)** es **significativamente más alto ($0.2903$)** que el tono promedio de aquellos que no lo mencionan ($0.0189$).


## 13 - Para los registros de "Generacion Z", determine qué plataforma es más mencionada: Twitter/X o YouTube. Muestre el conteo de menciones para cada una.

#### Ollama 3.2 1b

Después de analizar la información del archivo, puedo presentar las siguientes conclusiones:

- La plataforma más mencionada por Generación Z es TikTok (ID: 123), con un total de 5 menciones.
- El video en YouTube no cuenta.

En resumen, TikTok es la plataforma más mencionada por Generación Z.

#### Chat GPT

Plataforma Más Mencionada
La plataforma **más mencionada** en los registros de "Generacion Z" es **Twitter/X**, con un total de **48** menciones.


## 14 - Filtre los registros de "Frankenstein" que mencionan el término "Venecia". De este subconjunto, muestre el Tono Promedio para evaluar si el reconocimiento en festivales se asocia a un tono más positivo.

#### Ollama 3.2 1b


Después de analizar la información del archivo, puedo presentar las siguientes conclusiones:

- Los registros que mencionan el término “Venecia” son:

- Frankenstein (ID: 51) - Tono Sentimiento: 1,0
- Del Toro: “La ciudad de los sueños” (relatado a Del Toro elogia la actuación de Actor 4 como Monstruo).

- Los registros que mencionan el término “Venecia” no se encuentran.

En este subconjunto, el Tono Promedio es positivo. No hay registros que sugieran un tono negativo asociado con la presencia en festivales de Venecia.

#### Chat GPT

Con base en la simulación:

- El **Tono Promedio** de los registros de "Frankenstein" que mencionan **"Venecia"** es **$-0.0631$**, lo que indica un tono ligeramente negativo.
    
- El **Tono Promedio General** de todos los registros de "Frankenstein" es **$0.0411$**, lo que indica un tono ligeramente positivo.

## 15 - Calcule cuántos registros de "Generacion Z" cumplen simultáneamentelas siguientes condiciones: el Medio es El País Y el Resumen menciona la palabra "gobierno".

#### Ollama 3.2 1b

Los registros que cumplen con todas las condiciones son:
- Generación Z (ID: 55) - Tono Sentimiento: 0.9
- La palabra “gobierno” se menciona en el comentario de El País (ID: 123), donde se dice: “Señalan cuentas vinculadas a grupos de oposición.”

Por lo tanto, hay un total de 1 registro que cumple simultáneamente las condiciones

#### Chat GPT

Calcule cuántos registros de "Generación Z" cumplen simultáneamente las siguientes condiciones: el Medio es El País Y el Resumen menciona la palabra "gobierno".


## 16 - Utilizando la columna Tono_Sentimiento y los resultados del conteo de palabras clave, sintetice y argumente por qué la cobertura simulada de "Frankenstein" es, en promedio, más positiva que la de "Generacion Z".


#### Ollama 3.2 1B

Después de analizar la información proporcionada por el archivo, puedo presentar las siguientes conclusiones:

La cobertura simulada de “Frankenstein” (ID: 51) tiene un Tono Sentimiento promedio de 1.0, lo que indica una cobertura muy positiva.

En comparación con la cobertura simulada de “Generación Z” (ID: 55), que tiene un Tono Sentimiento promedio de 0.9, podemos inferir que la cobertura simulada de “Frankenstein” es en promedio más positiva.

Además, se menciona explícitamente a Del Toro en el comentario de Frankenstein (ID: 51) como uno de los principales argumentos para justificar su decisión de realizar una adaptación cinematográfica sobre la historia. Esto sugiere que la cobertura simulada de “Frankenstein” también tiene un componente emocional, y puede ser más positivo debido a la influencia del director y el argumento.

####  Chat GPT


Lamento no poder utilizar la columna **'Tono_Sentimiento'** directamente, ya que esta columna **no existe** en el archivo `datasetTexto.csv`.

Sin embargo, puedo sintetizar y argumentar la diferencia en el tono de la cobertura utilizando el **conteo de palabras clave** de las columnas de texto (`Titulo`, `Resumen`, y `Comentario\_Reaccion`)

El tono es más positivo en "Frankenstein" porque la mayoría de las noticias se centran en la **evaluación artística y el éxito comercial** de una obra de ficción. Los términos clave son de **elogio explícito** (`mejor`, `éxito`) o de **valoración de la producción** (`director`, `actor`, `maquillaje`), lo que inherentemente genera una cobertura optimista.

Por el contrario, el tono de "Generacion Z" es más negativo o serio porque se enfoca en un **conflicto social real**. Los términos predominantes giran en torno a la **insatisfacción** (`protesta`, `demandas`), la **confrontación** (`gobierno`, `critican`) y la **acción colectiva disruptiva** (`marcha`, `movimiento`),


## 17 - Con base en el día de mayor actividad, filtre todos los registros de ese día. Usando el Título y Resumen, sintetice el evento clave o confrontación que impulsó esa cobertura.


#### Ollama 3.2 1B

El día de mayor actividad es el 26 de noviembre de 2025, con un total de 4 registros que mencionan específicamente esa fecha.

Los registros que se encuentran entre los días 24 y 27 de noviembre son:

- Frankenstein (ID: 51) - Tono Sentimiento: 1.0
- Del Toro: “El dolor como motor de la monstruosidad” (relatado a Del Toro elogia la actuación de Actor 4 como Monstruo).
- Generación Z (ID: 55) - Tono Sentimiento: 0,9

En este caso, la cobertura simulada de “Frankenstein” es más positiva en promedio que la de “Generación Z”, lo que sugiere que el evento clave o confrontación que impulsó esa cobertura fue la oportunidad de presentar una adaptación cinematográfica original y exitosa.

####  Chat GPT

El día de mayor actividad en el archivo es el **16 de noviembre de 2025**, con 28 registros.

El evento clave que impulsó esta cobertura masiva fue el **punto álgido de la protesta de la Generación Z**, caracterizado por una **confrontación directa y la expansión nacional** del movimiento:

- **Evento:** Gran **marcha juvenil** contra la corrupción, la impunidad y la inseguridad.
    
- **Confrontación Principal:** Se reportaron **enfrentamientos con la policía**, resultando en **20 detenidos** y la denuncia de **detenciones arbitrarias** y desalojos.
    
- **Expansión:** La cobertura registró que la movilización se replicó en **Guadalajara y Monterrey**, confirmando el alcance nacional del evento.
    
- **Narrativa Digital:** Además de la acción en la calle, el evento se volvió viral, con la **cobertura en vivo más vista en Facebook** y la creación de una **narrativa propia** mediante YouTube y drones.

## 18 - Filtre y analice las citas o resúmenes que se atribuyen a Guillermo del Toro. Sintetice en una sola frase su enfoque principal sobre el mensaje de la historia de Frankenstein.


#### Ollama 3.2 1B

Después de analizar la información del archivo, puedo presentar las siguientes conclusiones:

En el comentario de Frankenstein (ID: 51), se menciona explícitamente a Guillermo del Toro como "un genio con la madurez de un niño" y quien "examina la inmadurez moral del científico".

####  Chat GPT

El enfoque principal de **Guillermo del Toro** sobre el mensaje de la historia de Frankenstein, según las citas y resúmenes atribuidos en el archivo, se sintetiza en la siguiente frase:

La historia es fundamentalmente una **tragedia sobre la paternidad fallida** y la **responsabilidad del creador**, donde el **dolor** es la emoción dominante de la criatura.


## 19 - Filtre los registros que mencionan "desinformación", "bots" o"infiltrar". Identifique y enumere las entidades o grupos que son acusados directamente de estos actos en el contexto de las protestas de la Generación Z.

#### Ollama 3.2 1B

Se mencionan varios registros que indican que los grupos o individuos están reportando desinformación y ataques coordinados contra las cuentas grandes de la Generación Z. Algunos ejemplos son:

- Influencers (ID: 123) - “Cuentas grandes reportan ataques coordinados y amenazas.”
- Frankenstein (ID: 123) - “Se señalan cuentas vinculadas a grupos de oposición.”

En este contexto, se acusa específicamente a los siguientes grupos o individuos:

- Los grupos de oposición o activistas.
- Los influencers o personalidades en redes sociales que están reportando desinformación y ataques coordinados.

Estos grupos o individuos son acusados directamente de infiltrar o manipular las redes sociales para propagar información falsa o perjudicial.

####  Chat GPT

Basado en el análisis de los registros de la categoría "Generacion Z" que mencionan las palabras clave de desinformación e infiltración:

Las entidades o grupos que son **acusados directamente** de desinformación, uso de bots, o infiltración en el contexto de las protestas son:

1. **Bots (Campaña digital):** Acusados de financiar y ejecutar una **campaña digital** de desinformación.
    
2. **Influencers:** Acusados de ser parte de la **campaña digital** de desinformación (junto con los bots).
    
3. **Opositores adultos:** Acusados por el Gobierno de tener **presencia** en la marcha y buscar desestabilizar (filtrados/opositores).
    
4. **Partidos de derecha:** Acusados por el Gobierno de **infiltrar** la marcha con el fin de **desestabilizar la administración**.
    
5. **Rumores oficiales:** Identificados como la **fuente de "Fake News"** que la Generación Z, a través de sus redes, intenta **desmentir**.

## 20 - Escriba y ejecute el código Python/Pandas necesario para encontrar el número de registros de "Frankenstein" donde el Comentario_Reaccion incluye la frase "obra maestra" o "clásico".


#### Ollama 3.2 1B


####  Chat GPT

`import pandas as pd`
`import re`

`data = []`
`columns = ['ID', 'Categoria', 'Titulo', 'Medio', 'Fecha', 'Resumen', 'Comentario_Reaccion']`

`pattern = re.compile(r'^(\d+),([^,]+),(.*),([^,]+),(\d{4}-\d{2}-\d{2}),"(.*)","(.*)"$')`

`try:`
    `with open('datasetTexto.csv', 'r', encoding='utf-8') as f:`
        `lines = f.readlines()`
`except UnicodeDecodeError:`
    `with open('datasetTexto.csv', 'r', encoding='latin-1') as f:`
        `lines = f.readlines()`

`for i, line in enumerate(lines):`
    `line = line.strip()`
    `if i == 0:`
        `continue # Skip header`
    `match = pattern.match(line)`
    `if match:`
        `data.append(match.groups())`

`df = pd.DataFrame(data, columns=columns)`

`df_frank = df[df['Categoria'] == 'Frankenstein']`

`keywords_pattern = 'obra maestra|clásico'`
`count = df_frank['Comentario_Reaccion'].str.contains(keywords_pattern, case=False, regex=True).sum()`

`print(f"El número de registros de 'Frankenstein' que contienen la frase 'obra maestra' o 'clásico' en 'Comentario_Reaccion' es: {count}")`


El número de registros de "Frankenstein" que contienen las frases **"obra maestra"** o **"clásico"** en la columna `Comentario_Reaccion` es: **6**.

# Conclusión

Al revisar los resultados, me queda claro que la diferencia en el procesamiento fue abismal. El modelo local de Ollama simplemente pudieron manejar el _dataset_; sus respuestas daban numeros que se sentían ierróneas. Por ejemplo, contaban solo unos pocos registros para preguntas clave o daban proporciones que no cuadraban.

En cambio, Chat GPT fue notablemente preciso. Los números que arrojó sugieren que fue capaz de leer, limpiar y procesar el archivo completo, incluso corrigiendo los registros malformados. Esto se reflejó en respuestas más confiables.