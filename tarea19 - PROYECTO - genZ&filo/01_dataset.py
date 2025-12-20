import pandas as pd
import numpy as np
from faker import Faker
import random

# Cargar dataset original
df = pd.read_csv('dataset_sintetico_5000_ampliado.csv')

fake = Faker()

# Temas y sentimientos posibles
temas = df['tema'].unique()
sentimientos = ['positivo', 'negativo', 'neutral']

# Frases base para generar texto (extraídas del dataset o creadas)
# Lista expandida para análisis de datos (Corpus de entrenamiento/prueba para RAG)
frases_base = [
    # --- EJE 1: GENERACIÓN Z Y CRISIS DE SENTIDO (Lyotard y Camus) ---
    "La presión por ser productivo todo el tiempo está quemando a una generación entera.",
    "Muchos jóvenes tienen una sensación de vacío difícil de explicar.",
    "Vivimos en un mundo hiperconectado, pero paradójicamente, cada día nos sentimos más solos.",
    "La Generación Z enfrenta un dilema existencial: querer cambiar el mundo, pero estar atrapada en dinámicas de inmediatez.",
    "Buscar sentido en medio del ruido digital es un acto filosófico profundo.",
    "La identidad ya no es algo fijo, sino un proyecto en constante reconstrucción.",
    "El exceso de opciones paraliza más que libera.",
    "La ansiedad existencial se ha convertido en un malestar generacional.",
    "Crecemos entre likes y seguidores, pero buscamos validación auténtica.",
    "Siento que mi vida es un loop infinito de contenido que no me llena.",
    "El fin de los grandes sueños nos dejó atrapados en el consumo de momentos.",
    "¿Para qué planear a 10 años si el mundo parece que se va a acabar mañana?",
    "A veces siento que solo existo si publico lo que estoy haciendo.",
    "La depresión post-scroll es real: te sientes menos que los demás sin razón.",
    "Nadie nos enseñó a lidiar con este vacío cuando se apaga la pantalla.",
    "El 'bed rotting' es nuestra respuesta física a un mundo que pide demasiado de nosotros.",
    "Estamos en nuestra 'depressing era' porque los metarrelatos de éxito ya no tienen sentido.",

    # --- EJE 2: MODERNIDAD LÍQUIDA Y EFÍMERO (Bauman) ---
    "Antes los proyectos de vida eran a largo plazo; hoy cambian tan rápido como las tendencias en TikTok.",
    "Todo se mueve tan rápido que incluso los recuerdos parecen caducar.",
    "La cultura de lo efímero borra cualquier intento de construir algo que perdure.",
    "La identidad en línea se construye y se desmonta como si fuera un proyecto temporal.",
    "Nada parece sólido, ni siquiera la idea de quién somos.",
    "Los vínculos afectivos hoy son más frágiles que nunca.",
    "Estamos tan acostumbrados a la recompensa instantánea que la paciencia nos parece imposible.",
    "Dejando poco espacio para la reflexión o el compromiso duradero.",
    "Tengo 500 amigos en Instagram pero nadie a quien llamar si me siento mal.",
    "Las relaciones hoy son como productos: si tienen un fallo, los descartas y buscas otro.",
    "La identidad líquida es agotadora; nunca terminas de saber quién eres.",
    "Ghosting es la respuesta moderna a la incapacidad de enfrentar un vínculo real.",
    "Mi perfil es una curaduría de estéticas (eras), no un reflejo de mi esencia.",

    # --- EJE 3: SOCIEDAD DEL RENDIMIENTO Y BURNOUT (Byung-Chul Han) ---
    "No todo en la vida debe ser rendimiento.",
    "La productividad constante se ha convertido en una nueva forma de ansiedad.",
    "Me siento culpable si paso un domingo sin hacer nada 'provechoso'.",
    "El cansancio de la Gen Z no es físico, es un cansancio del alma por tanto competir.",
    "Nos autoexplotamos pensando que somos libres porque no tenemos un jefe encima.",
    "Instagram es el escaparate de una felicidad que nadie siente de verdad.",
    "La sociedad del cansancio nos ha quitado la capacidad de contemplar el silencio.",
    "Estamos matando el eros y el deseo por culpa de la pornografía de la transparencia.",
    "Ser 'tú mismo' es hoy la orden más difícil de cumplir.",
    "El multitasking es solo una forma elegante de decir que nuestra atención está rota.",
    "El 'burnout' digital es el precio que pagamos por el auto-perfeccionamiento constante.",
    "La transparencia total en redes elimina el misterio necesario para el deseo real.",

    # --- EJE 4: IA Y PÉRDIDA DE AUTONOMÍA (Foucault y Heidegger) ---
    "¿Seguimos siendo sujetos libres si los algoritmos determinan qué contenido vemos?",
    "Cada vez que una app me recomienda algo, siento que renuncio un poco más a mi libertad.",
    "Los algoritmos parecen conocer mis gustos mejor que yo mismo.",
    "Es inquietante pensar si realmente sigo mis propias decisiones.",
    "La IA puede predecir nuestras emociones con una precisión inquietante.",
    "¿Qué queda entonces de nuestra espontaneidad?",
    "La relación entre la inteligencia artificial y nuestra autonomía se está volviendo difusa.",
    "Las plataformas moldean mi comportamiento sin que yo lo note.",
    "El algoritmo de TikTok sabe que estoy triste antes de que yo me dé cuenta.",
    "Siento que vivo en una burbuja donde solo veo lo que el sistema quiere que crea.",
    "La vigilancia digital ya no es un guardia en una torre, es un código en mi bolsillo.",
    "¿Es mi deseo o es una sugerencia de la IA que acepté por cansancio?",
    "Delegamos nuestra voluntad en máquinas porque pensar por uno mismo toma tiempo.",
    "La tecnología nos 'desoculta' como meros recursos de datos para el mercado.",
    "El algoritmo es el nuevo Panóptico: no necesito que me vean para portarme como el sistema espera.",

    # --- EJE 5: TECNOLOGÍA Y EROSIÓN DEL ESPACIO PÚBLICO (Habermas) ---
    "Con tanta información, el desafío ya no es aprender, sino filtrar.",
    "El ruido constante de las redes sociales hace difícil encontrar silencio interior.",
    "Las redes sociales ofrecen conexión, pero a menudo nos dejan más aislados.",
    "El espacio público digital está lleno de gritos, pero nadie se escucha realmente.",
    "Las burbujas de filtro nos están volviendo incapaces de entender a quien piensa distinto.",
    "La verdad ha sido reemplazada por lo que genera más interacción (engagement).",
    "Vivimos en una posverdad donde el dato importa menos que la emoción del algoritmo.",
    "La acción comunicativa ha muerto; ahora solo queda el performance para la audiencia.",
    "El debate ha sido reemplazado por el 'cancel culture', un juicio sin diálogo.",

    # --- EJE 6: METÁFORAS Y REFLEXIONES FINALES ---
    "Navegamos en un océano de información pero morimos de sed de significado.",
    "Las redes sociales son espejos distorsionados que reflejan solo lo que queremos ver.",
    "Los algoritmos son los nuevos arquitectos de nuestra realidad.",
    "La atención se ha fragmentado en mil pedazos como un cristal roto.",
    "Vivimos en un presente perpetuo, sin pasado que recordar ni futuro que imaginar.",
    "El scroll infinito es la nueva versión del mito de Sísifo.",
    "Somos ciborgs que aún sienten angustia humana.",
    "La tecnología es un teclado increíble, pero nos hemos olvidado de cómo escribir la partitura.",
    "Nuestra mayor rebeldía hoy es el silencio y la desconexión.",
    "La identidad digital es una máscara que terminó por comerse al rostro.",
    "El futuro nos da miedo, pero el presente nos tiene anestesiados."
]

def generar_texto_compuesto():
    num_frases = random.randint(2, 3)
    frases_seleccionadas = random.sample(frases_base, num_frases)
    conectores = [" ", ". ", " "]
    texto = ""
    for i, frase in enumerate(frases_seleccionadas):
        if i == 0:
            texto += frase
        else:
            if random.random() > 0.5:
                texto += ". " + frase
            else:
                texto += " " + frase
    return texto

# Generar nuevos registros
nuevos_datos = []
for i in range(5000):
    nuevo_id = df['id'].max() + i + 1
    nueva_fecha = fake.date_between(start_date='-4y', end_date='today')
    nuevo_usuario = f"user_{random.randint(10000, 99999)}"
    texto = generar_texto_compuesto()
    tema = random.choice(temas)
    sentimiento = random.choice(sentimientos)
    likes = random.randint(500, 20000)
    reposts = random.randint(10, 5000)
    
    nuevos_datos.append({
        'id': nuevo_id,
        'fecha': nueva_fecha,
        'usuario': nuevo_usuario,
        'texto': texto,
        'tema': tema,
        'sentimiento': sentimiento,
        'likes': likes,
        'reposts': reposts
    })

# Convertir a DataFrame y unir al original
df_nuevo = pd.DataFrame(nuevos_datos)
df_ampliado = pd.concat([df, df_nuevo], ignore_index=True)

df_ampliado.to_csv('dataset_super_sintetico.csv', index=False)