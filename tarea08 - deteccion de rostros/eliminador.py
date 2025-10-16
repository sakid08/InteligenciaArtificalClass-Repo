import cv2 as cv
import os

# Ruta principal del dataset
dataSet = 'D:/saids/Desktop/gato/rostros/rostroPersonas'

# Recorre todas las carpetas (una por persona)
for persona in os.listdir(dataSet):
    personPath = os.path.join(dataSet, persona)
    if not os.path.isdir(personPath):
        continue

    print(f"\n📂 Revisando carpeta: {persona}")
    total = 0
    eliminadas = 0

    for file in os.listdir(personPath):
        filePath = os.path.join(personPath, file)

        # Solo procesar imágenes comunes
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        total += 1
        img = cv.imread(filePath, 0)

        # Verificar si la imagen está vacía o corrupta
        if img is None or img.size == 0:
            os.remove(filePath)
            eliminadas += 1
            print(f"🗑️ Eliminada (vacía/corrupta): {filePath}")
            continue

        # Verificar tamaño (debe ser exactamente 100x100)
        h, w = img.shape[:2]
        if (w, h) != (100, 100):
            os.remove(filePath)
            eliminadas += 1
            print(f"🗑️ Eliminada (tamaño {w}x{h}): {filePath}")

    print(f"✅ Carpeta {persona}: {total - eliminadas}/{total} imágenes válidas ({eliminadas} eliminadas)")

print("\n✨ Limpieza completada. Todas las imágenes ahora deberían ser válidas y de 100x100 píxeles.")
