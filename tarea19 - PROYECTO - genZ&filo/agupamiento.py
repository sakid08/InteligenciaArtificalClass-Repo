import pandas as pd

df = pd.read_csv("./dataset_genz.csv")

# Normalizar Medio para evitar caos silencioso
df["Medio"] = df["Medio"].str.strip().str.lower()

# Ordenar por Medio
df_ordenado = df.sort_values(by="Medio")

# Guardar en un solo CSV
df_ordenado.to_csv("datos_ordenados_por_medio.csv", index=False)
