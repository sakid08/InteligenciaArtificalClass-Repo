import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

# ===================== 1. CARGAR LOS DATOS =====================
print("="*60)
print("ENTRENAMIENTO DE MODELO DE ÁRBOL DE DECISIÓN")
print("="*60)

archivo_csv = "emociones.csv"

try:
    df = pd.read_csv(archivo_csv)
    print(f"✓ Datos cargados desde: {archivo_csv}")
    print(f"  Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    print("\nPrimeras 5 filas:")
    print(df.head())
except FileNotFoundError:
    print(f"✗ Error: No se encontró el archivo '{archivo_csv}'")
    print("  Asegúrate de que el archivo CSV existe en el directorio actual.")
    exit()

# ===================== 2. PREPROCESAMIENTO =====================
print("\n" + "-"*60)
print("PREPROCESAMIENTO DE DATOS")
print("-"*60)

# Verificar qué columnas tenemos
print("Columnas disponibles:")
print(df.columns.tolist())

# Definir qué columna usar como target (etiqueta)
# Si tienes datos manuales, usa 'clase_manual', si no, 'clase'
if 'clase_manual' in df.columns:
    target_column = 'clase_manual'
    print("\n✓ Usando etiquetas manuales (clase_manual)")
elif 'clase' in df.columns:
    target_column = 'clase'
    print("\n✓ Usando etiquetas automáticas (clase)")
else:
    print("\n✗ Error: No se encontró columna de clases")
    exit()

# Verificar valores únicos en la columna target
print(f"Valores únicos en {target_column}: {sorted(df[target_column].unique())}")

# Eliminar filas con valores nulos en el target
df_clean = df.dropna(subset=[target_column])
print(f"✓ Filas después de eliminar nulos: {df_clean.shape[0]}")

# Definir características (features) - todas las columnas que empiezan con 'ratio_'
feature_columns = [col for col in df_clean.columns if col.startswith('ratio_')]
print(f"\n✓ Características seleccionadas ({len(feature_columns)}):")
for i, feat in enumerate(feature_columns, 1):
    print(f"  {i:2d}. {feat}")

# Preparar X (features) y y (target)
X = df_clean[feature_columns]
y = df_clean[target_column]

# Verificar que tenemos datos
if len(X) == 0:
    print("\n✗ Error: No hay datos para entrenar")
    exit()

print(f"\n✓ Datos preparados:")
print(f"  X (features): {X.shape}")
print(f"  y (target): {y.shape}")
print(f"  Clases en y: {sorted(y.unique())}")

# Convertir y a enteros (por si acaso)
y = y.astype(int)

# ===================== 3. NORMALIZAR DATOS =====================
print("\n" + "-"*60)
print("NORMALIZACIÓN DE CARACTERÍSTICAS")
print("-"*60)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("✓ Características normalizadas (media=0, std=1)")

# ===================== 4. DIVIDIR EN TRAIN/TEST =====================
print("\n" + "-"*60)
print("DIVISIÓN TRAIN/TEST (80%/20%)")
print("-"*60)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✓ Conjunto de entrenamiento: {X_train.shape[0]} muestras")
print(f"✓ Conjunto de prueba: {X_test.shape[0]} muestras")

# Verificar distribución de clases
print("\nDistribución de clases en entrenamiento:")
train_counts = pd.Series(y_train).value_counts().sort_index()
for clase, count in train_counts.items():
    print(f"  Clase {clase}: {count} muestras ({count/len(y_train)*100:.1f}%)")

print("\nDistribución de clases en prueba:")
test_counts = pd.Series(y_test).value_counts().sort_index()
for clase, count in test_counts.items():
    print(f"  Clase {clase}: {count} muestras ({count/len(y_test)*100:.1f}%)")

# ===================== 5. ENTRENAR MODELO =====================
print("\n" + "-"*60)
print("ENTRENAMIENTO DEL ÁRBOL DE DECISIÓN")
print("-"*60)

# Crear y entrenar el modelo
modelo = DecisionTreeClassifier(
    max_depth=8,           # Profundidad máxima para evitar overfitting
    min_samples_split=10,  # Mínimo de muestras para dividir un nodo
    min_samples_leaf=5,    # Mínimo de muestras en una hoja
    random_state=42,
    class_weight='balanced'  # Balancear clases si están desbalanceadas
)

modelo.fit(X_train, y_train)
print("✓ Modelo entrenado exitosamente")

# ===================== 6. EVALUAR MODELO =====================
print("\n" + "-"*60)
print("EVALUACIÓN DEL MODELO")
print("-"*60)

# Predecir en train y test
y_train_pred = modelo.predict(X_train)
y_test_pred = modelo.predict(X_test)

# Calcular métricas
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"✓ Precisión en entrenamiento: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"✓ Precisión en prueba: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Reporte de clasificación detallado
print("\n" + "="*60)
print("REPORTE DE CLASIFICACIÓN (TEST)")
print("="*60)
print(classification_report(y_test, y_test_pred, 
                           target_names=['Neutro', 'Feliz', 'Triste', 'Enojado', 'Sorprendido']))

# Matriz de confusión
print("\n" + "="*60)
print("MATRIZ DE CONFUSIÓN (TEST)")
print("="*60)
conf_matrix = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Neutro', 'Feliz', 'Triste', 'Enojado', 'Sorprendido'],
            yticklabels=['Neutro', 'Feliz', 'Triste', 'Enojado', 'Sorprendido'])
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de Confusión - Árbol de Decisión')
plt.tight_layout()
plt.savefig('matriz_confusion.png', dpi=300, bbox_inches='tight')
print("✓ Matriz de confusión guardada como 'matriz_confusion.png'")

# ===================== 7. IMPORTANCIA DE CARACTERÍSTICAS =====================
print("\n" + "-"*60)
print("IMPORTANCIA DE CARACTERÍSTICAS")
print("-"*60)

importancias = modelo.feature_importances_
indices = np.argsort(importancias)[::-1]

print("Características ordenadas por importancia:")
for i, idx in enumerate(indices[:10]):  # Top 10
    print(f"  {i+1:2d}. {feature_columns[idx]:25s}: {importancias[idx]:.4f}")

# Gráfico de importancia de características
plt.figure(figsize=(12, 6))
plt.bar(range(len(feature_columns)), importancias[indices])
plt.xticks(range(len(feature_columns)), 
           [feature_columns[i] for i in indices], rotation=45, ha='right')
plt.xlabel('Características')
plt.ylabel('Importancia')
plt.title('Importancia de Características en el Árbol de Decisión')
plt.tight_layout()
plt.savefig('importancia_caracteristicas.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico de importancia guardado como 'importancia_caracteristicas.png'")

# ===================== 8. VISUALIZAR EL ÁRBOL =====================
print("\n" + "-"*60)
print("VISUALIZACIÓN DEL ÁRBOL DE DECISIÓN")
print("-"*60)

plt.figure(figsize=(20, 12))
plot_tree(modelo, 
          feature_names=feature_columns,
          class_names=['Neutro', 'Feliz', 'Triste', 'Enojado', 'Sorprendido'],
          filled=True, 
          rounded=True,
          max_depth=3,  # Mostrar solo primeros 3 niveles por claridad
          fontsize=10)
plt.title('Árbol de Decisión (primeros 3 niveles)', fontsize=16)
plt.tight_layout()
plt.savefig('arbol_decision.png', dpi=300, bbox_inches='tight')
print("✓ Árbol de decisión guardado como 'arbol_decision.png'")

# ===================== 9. GUARDAR MODELO =====================
print("\n" + "-"*60)
print("GUARDANDO MODELO ENTRENADO")
print("-"*60)

# Guardar el modelo
joblib.dump(modelo, 'modelo_arbol_decision.pkl')
print("✓ Modelo guardado como 'modelo_arbol_decision.pkl'")

# Guardar el scaler
joblib.dump(scaler, 'scaler.pkl')
print("✓ Scaler guardado como 'scaler.pkl'")

# Guardar las columnas de características
with open('feature_columns.txt', 'w') as f:
    for col in feature_columns:
        f.write(col + '\n')
print("✓ Columnas de características guardadas como 'feature_columns.txt'")

# ===================== 10. RESUMEN FINAL =====================
print("\n" + "="*60)
print("RESUMEN DEL ENTRENAMIENTO")
print("="*60)
print(f"Modelo: Árbol de Decisión")
print(f"Profundidad máxima: {modelo.get_depth()}")
print(f"Número de hojas: {modelo.get_n_leaves()}")
print(f"Precisión en test: {test_accuracy*100:.2f}%")
print(f"Características usadas: {len(feature_columns)}")
print(f"Clases: {sorted(y.unique())}")

print("\nArchivos generados:")
print("  1. modelo_arbol_decision.pkl - Modelo entrenado")
print("  2. scaler.pkl - Normalizador de características")
print("  3. feature_columns.txt - Lista de características")
print("  4. matriz_confusion.png - Matriz de confusión")
print("  5. importancia_caracteristicas.png - Importancia de características")
print("  6. arbol_decision.png - Visualización del árbol")

print("\n✓ ¡Entrenamiento completado exitosamente!")
print("="*60)

# Mostrar algunos gráficos
plt.show()