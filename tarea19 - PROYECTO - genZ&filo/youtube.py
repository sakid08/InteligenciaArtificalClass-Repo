import requests
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader
from itertools import islice
import time
import json
import random
import os

# ===========================
# CONFIGURACIÓN GENERAL
# ===========================

ARCHIVO_SALIDA = "datos/redes_sociales/corpus_genz_es.txt"
os.makedirs(os.path.dirname(ARCHIVO_SALIDA), exist_ok=True)

TOTAL_OBJETIVO = 5000

# ======== YOUTUBE (Contexto Hispano) ========
LIMITE_POR_VIDEO = 300
URLS_VIDEOS = [
    "https://www.youtube.com/watch?v=-1uomPlqtTc", # La Generación Ansiosa (Análisis)
    "https://www.youtube.com/watch?v=zPNbDDxysk0", # La sociedad del cansancio (Byung-Chul Han)
    "https://www.youtube.com/watch?v=_dGN3Z1qVY4", # Dejar las redes sociales - Experiencia real
    "https://www.youtube.com/watch?v=b-Jdy1Huj6g", # Dopamina digital y adicción
    "https://www.youtube.com/watch?v=Nh9dWEHj9do", # Crisis de salud mental en la Gen Z
]

# ======== REDDIT (Comunidades Hispanas) ========
# Subreddits activos donde se habla de salud mental y sociedad en español
SUBREDDITS_OBJETIVO = [
    "Desahogo",          # Equivalente a offmychest
    "es",                # Comunidad general de España
    "Mexico",            # Comunidad general de México
    "Argentina",         # Comunidad general de Argentina
    "Ansiedad",          # Específico de salud mental
    "Soledad",           # Específico de soledad
    "Conversaciones",    # Charlas generales
    "Psicologia",        # Temas de psicología
]

# Términos temáticos para filtrar (Traducidos y adaptados)
TERMINOS_BUSQUEDA = [
    "burnout",           # Se usa mucho en español también
    "quemado del trabajo",
    "soledad",
    "dejar redes sociales",
    "ansiedad social",
    "futuro incierto",
    "crisis existencial",
    "fatiga digital",
    "no tengo amigos",
    "harto de todo",
    "dopamina",
]

# ===========================
# FUNCIONES AUXILIARES
# ===========================

def normalizar_texto(texto):
    if not texto:
        return ""
    # Reemplaza saltos de línea y elimina espacios redundantes
    texto_limpio = texto.replace("\n", " ").strip()
    texto_limpio = " ".join(texto_limpio.split())
    return texto_limpio


# ===========================
# EXTRACTOR YOUTUBE
# ===========================

def extraer_comentarios_youtube():
    print("\n=== Descargando datos de YouTube (Español) ===")
    descargador = YoutubeCommentDownloader()
    lista_comentarios = []

    for url in URLS_VIDEOS:
        print(f"> Procesando video: {url}")
        try:
            # sort_by=1 suele ser 'Más recientes', 0 es 'Más populares'
            generador = descargador.get_comments_from_url(url, sort_by=1)
            
            for comentario in islice(generador, LIMITE_POR_VIDEO):
                texto = normalizar_texto(comentario.get("text", ""))
                
                # Filtramos comentarios muy cortos (tipo "jaja", "saludos")
                if len(texto) > 30:
                    entrada = f"FUENTE:YOUTUBE | URL:{url} | COMENTARIO:{texto}"
                    lista_comentarios.append(entrada)
                    
        except Exception as e:
            print(f"Error extrayendo de {url}: {e}")

    print(f"Total recolectado YouTube: {len(lista_comentarios)}\n")
    return lista_comentarios


# ===========================
# EXTRACTOR REDDIT (API Pushshift)
# ===========================
# Nota: La API pública de Pushshift tiene limitaciones estrictas actualmente.
# Si falla, considera usar PRAW (la librería oficial) con credenciales de desarrollador.

def peticion_reddit(endpoint, parametros):
    """Wrapper para manejar la petición HTTP con reintentos."""
    base_url = f"https://api.pushshift.io/reddit/{endpoint}"
    # Headers a veces ayudan a evitar bloqueos simples
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Script/Investigacion'}
    
    for _ in range(3):
        try:
            r = requests.get(base_url, params=parametros, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429: # Too many requests
                time.sleep(2)
        except Exception:
            time.sleep(1)
            
    return {"data": []}


def extraer_datos_reddit(limite_total=3000):
    print("\n=== Descargando datos de Reddit (Español) ===")
    resultados = []

    for sub in SUBREDDITS_OBJETIVO:
        print(f"> Explorando r/{sub}")

        for termino in TERMINOS_BUSQUEDA:
            params = {
                "subreddit": sub,
                "q": termino,
                "size": 50,  # Reducido por precaución con la API
                "sort": "desc",
                # "after": "30d" # Opcional: filtrar por tiempo si se desea
            }

            datos = peticion_reddit("search/comment", params).get("data", [])
            
            for c in datos:
                cuerpo = normalizar_texto(c.get("body", ""))
                
                # Filtros de calidad: longitud mínima y evitar enlaces
                if len(cuerpo) > 25 and "http" not in cuerpo:
                    entrada = (
                        f"FUENTE:REDDIT | SUB:{sub} | "
                        f"BUSQUEDA:{termino} | COMENTARIO:{cuerpo}"
                    )
                    resultados.append(entrada)

            # Pausa para ser amable con la API
            time.sleep(0.5)

            if len(resultados) >= limite_total:
                break
        
        if len(resultados) >= limite_total:
            break

    print(f"Total recolectado Reddit: {len(resultados)}\n")
    return resultados


# ===========================
# EJECUCIÓN PRINCIPAL
# ===========================

def generar_dataset():
    datos_youtube = extraer_comentarios_youtube()
    
    # Ajustamos el límite de Reddit para intentar balancear si YouTube trae pocos
    limite_reddit = TOTAL_OBJETIVO - len(datos_youtube) + 500
    datos_reddit = extraer_datos_reddit(limite_total=limite_reddit)

    corpus_completo = datos_youtube + datos_reddit

    # Mezclar para evitar sesgos por orden de fuente
    random.shuffle(corpus_completo)

    # Recortar al objetivo exacto
    corpus_final = corpus_completo[:TOTAL_OBJETIVO]

    # Guardar en archivo de texto
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        for linea in corpus_final:
            f.write(linea + "\n")

    print("=== PROCESO FINALIZADO ===")
    print(f"Total de entradas guardadas: {len(corpus_final)}")
    print(f"Ubicación: {os.path.abspath(ARCHIVO_SALIDA)}")


if __name__ == "__main__":
    generar_dataset()