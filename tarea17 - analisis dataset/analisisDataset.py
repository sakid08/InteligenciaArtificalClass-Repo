import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

archivo = 'D:\\saids\\Desktop\\InteligenciaArtificalClass-Repo\\tarea17 - analisis dataset\\datasetTexto.csv'

if not os.path.exists(archivo):
    print(f"No se encuentra el archivo")
else:
    try:
        df = pd.read_csv(archivo, engine='python', on_bad_lines='skip')
        print("✅ Archivo cargado correctamente.")
    except Exception as e:
        print(f"Error al leer el CSV")
        exit()


    positive_keywords = [
        'excelente', 'bueno', 'buena', 'increíble', 'mejor', 'gran', 'bien', 'amor',
        'gracias', 'felicidades', 'buen', 'apoyo', 'justicia', 'verdad', 'paz',
        'seguridad', 'emotiva', 'maestría', 'ídolo', 'imperdible', 'brillante', 'genial',
        'favorito', 'orgullo', 'valiente', 'esperanza', 'solución'
    ]

    negative_keywords = [
        'malo', 'mala', 'pésimo', 'horrible', 'peor', 'odio', 'triste', 'violencia',
        'represión', 'mentira', 'falso', 'bots', 'culpa', 'miedo', 'vergüenza',
        'desinformación', 'detener', 'muerte', 'asesinato', 'enfrentamientos', 'crisis',
        'corrupción', 'injusticia', 'problema', 'error', 'falsos', 'manipulación', 'ataque'
    ]

    def analyze_sentiment(text):
        if not isinstance(text, str):
            return 'Neutral'
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_keywords if word in text_lower)
        neg_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if pos_count > neg_count:
            return 'Positiva'
        elif neg_count > pos_count:
            return 'Negativa'
        else:
            return 'Neutral'

    # análisis
    if 'Comentario_Reaccion' in df.columns:
        df['Sentimiento'] = df['Comentario_Reaccion'].apply(analyze_sentiment)

        # Visualizar
        sentiment_counts = df['Sentimiento'].value_counts()
        print("\nResultados:")
        print(sentiment_counts)

        plt.figure(figsize=(8, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
        plt.title('Distribución de Sentimientos')
        plt.xlabel('Sentimiento')
        plt.ylabel('Cantidad')
        plt.show()
        
        # Guardar
        df.to_csv('dataset_con_sentimiento.csv', index=False)
        print("\nArchivo 'dataset_con_sentimiento.csv' guardado.")
    else:
        print("Comentario_Reaccion' no existe en el CSV.")