import pandas as pd
import os

def procesar_dataset():
    # 1. Cargar el archivo (ajustado al nombre detectado)
    archivo_entrada = './dataset_genz.csv'
    try:
        df = pd.read_csv(archivo_entrada)
    except FileNotFoundError:
        print(f"Error: No se encuentra {archivo_entrada}")
        return

    # 2. Identificar columnas (mapeo flexible para evitar campos vacíos)
    def buscar_columna(nombres_posibles):
        for col in df.columns:
            if col.lower() in nombres_posibles:
                return col
        return None

    col_tema = buscar_columna(['tema'])
    col_fecha = buscar_columna(['fecha', 'date'])
    col_texto = buscar_columna(['texto', 'comentarioreaccion', 'comentario', 'content'])
    col_usuario = buscar_columna(['usuario', 'medio', 'user', 'plataforma'])

    if not col_tema:
        print("No se encontró la columna 'tema'.")
        return

    # 3. Filtrar por Generación Z (Regex para Gen Z, Generación Z, etc.)
    mask = df[col_tema].astype(str).str.contains(r'gen(eraci[oó]n)?\s*z', case=False, na=False, regex=True)
    df_genz = df[mask].copy()

    if df_genz.empty:
        print("No se encontraron coincidencias para Generación Z.")
        return

    # 4. Crear carpeta de salida
    os.makedirs("archivos", exist_ok=True)

    # 5. Generar contenido plano para RAG
    lineas_txt = []
    for _, row in df_genz.iterrows():
        # Extraer valores usando el mapeo detectado
        fuente = str(row.get(col_usuario, '')).strip() if col_usuario else ""
        fecha = str(row.get(col_fecha, '')).strip() if col_fecha else ""
        tema = str(row.get(col_tema, '')).strip()
        contenido = str(row.get(col_texto, '')).strip() if col_texto else ""

        # Formato exacto solicitado sin decoraciones
        bloque = (
            f"Fuente: {fuente}\n"
            f"Fecha: {fecha}\n"
            f"Tema: {tema}\n"
            f"Contenido: {contenido}\n\n"
        )
        lineas_txt.append(bloque)

    # 6. Guardar archivo final
    ruta_salida = "archivos/genz_redes.txt"
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.writelines(lineas_txt)

    print(f"Hecho. Se procesaron {len(df_genz)} entradas en '{ruta_salida}'.")

if __name__ == "__main__":
    procesar_dataset()