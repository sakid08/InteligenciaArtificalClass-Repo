import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

DATASET_PATH = './dataset_genz.csv'
TEMA_OBJETIVO = 'Generación Z y crisis de sentido'
OUTPUT_DIR = 'graficos'

SENT_MAPPING = {'negativo': 1, 'neutral': 5, 'positivo': 10}
STOPWORDS_ES = {
    "de","la","que","el","en","y","a","los","se","del","las","un","por","con","no",
    "una","su","para","es","al","lo","como","mas","pero","sus","le","ya","o",
    "porque","muy","sin","sobre","también","me","hasta","donde","quien","desde",
    "nos","durante","uno","ni","contra","ese","eso","mí","mis","tengo","esta",
    "estamos","todo","todos","está","cada","siento","parecen","hacer","ser","son"
}

# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def generar_analisis_completo():
    print("\n--- GENERANDO ANÁLISIS COMPLETO GEN Z ---")

    if not os.path.exists(DATASET_PATH):
        print(f"❌ Error: No se encuentra el archivo '{DATASET_PATH}'")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # -------------------------------------------------
    # 1. CARGA Y PREPROCESAMIENTO
    # -------------------------------------------------

    df = pd.read_csv(DATASET_PATH)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['valor_sentimiento'] = df['sentimiento'].map(SENT_MAPPING)

    df_genz = df[df['tema'] == TEMA_OBJETIVO].copy()

    if df_genz.empty:
        print("⚠️ No hay datos para el tema especificado.")
        return

    print(f"📊 Registros analizados: {len(df_genz)}")

    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['figure.dpi'] = 100

    # -------------------------------------------------
    # 2. GRÁFICO: EMOCIONES VS MEDIOS
    # -------------------------------------------------

    plt.figure(figsize=(12, 7))
    sns.countplot(
        data=df_genz,
        x='Medio',
        hue='sentimiento',
        hue_order=['negativo','neutral','positivo'],
        palette={'negativo':'#ff6b6b','neutral':'#feca57','positivo':'#1dd1a1'}
    )
    plt.title('Comparación de Emociones por Plataforma', fontweight='bold')
    plt.xlabel('Plataforma')
    plt.ylabel('Cantidad de Opiniones')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/1_emociones_vs_medios.png')
    plt.close()

    # -------------------------------------------------
    # 3. GRÁFICO: PLATAFORMAS DIGITALES
    # -------------------------------------------------

    plt.figure(figsize=(10, 6))
    conteo = df_genz['Medio'].value_counts().reset_index()
    conteo.columns = ['Medio','Total']
    sns.barplot(data=conteo, x='Medio', y='Total', hue='Medio', palette='viridis')
    plt.title('Plataformas donde opina la Gen Z', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/2_plataformas_digitales.png')
    plt.close()

    # -------------------------------------------------
    # 4. GRÁFICO: EVOLUCIÓN TEMPORAL
    # -------------------------------------------------

    plt.figure(figsize=(12, 6))
    serie = (
        df_genz
        .groupby(df_genz['fecha'].dt.to_period('M'))['valor_sentimiento']
        .mean()
        .to_timestamp()
    )
    plt.plot(serie.index, serie.values, marker='o', linewidth=3)
    plt.fill_between(serie.index, serie.values, alpha=0.15)
    plt.ylim(1, 10)
    plt.title('Evolución Mensual del Ánimo Promedio', fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/3_evolucion_animo.png')
    plt.close()

    # -------------------------------------------------
    # 5. GRÁFICO: DETECCIÓN DE MENSAJES REPETIDOS (BOTS)
    # -------------------------------------------------

    plt.figure(figsize=(12, 8))
    top_textos = df['texto'].value_counts().head(10).reset_index()
    top_textos.columns = ['Mensaje','Frecuencia']
    top_textos['Mensaje_Corto'] = top_textos['Mensaje'].str[:70] + '...'

    sns.barplot(
        data=top_textos,
        y='Mensaje_Corto',
        x='Frecuencia',
        hue='Mensaje_Corto',
        palette='Reds_r'
    )
    plt.title('Mensajes Idénticos Detectados', fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/4_deteccion_bots.png')
    plt.close()

    # -------------------------------------------------
    # 6. NUBE DE PALABRAS
    # -------------------------------------------------

    texto_completo = " ".join(df_genz['texto'].astype(str))

    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color='black',
        stopwords=STOPWORDS_ES,
        colormap='plasma',
        max_words=200,
        contour_width=2,
        contour_color='white'
    ).generate(texto_completo)

    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'{OUTPUT_DIR}/5_nube_semantica.png', bbox_inches='tight')
    plt.show()

    print("\n✅ Análisis completo finalizado. Revisa la carpeta 'graficos'.")


if __name__ == "__main__":
    generar_analisis_completo()
