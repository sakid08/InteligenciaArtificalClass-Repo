import cv2 as cv
import numpy as np
import os

dataSet = 'D:/saids/Desktop/gato/02 emociones/train'
faces = os.listdir(dataSet)
print(f"Carpetas encontradas: {faces}")

labels = []
facesData = []
label = 0

for face in faces:
    facePath = os.path.join(dataSet, face)
    if not os.path.isdir(facePath):
        continue

    print(f"\n📂 Leyendo carpeta: {face}")
    count = 0
    for faceName in os.listdir(facePath):
        imgPath = os.path.join(facePath, faceName)

        # Saltar si no es imagen
        if not faceName.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img = cv.imread(imgPath, 0)
        if img is None or img.size == 0:
            print(f"⚠️ Imagen inválida (se omitirá): {imgPath}")
            continue

        # Verificar tamaño
        h, w = img.shape
        if (w, h) != (48, 48):
            print(f"⚠️ Tamaño distinto a 48x48 ({w}x{h}), se omitirá: {imgPath}")
            continue

        facesData.append(img)
        labels.append(label)
        count += 1

    print(f"✅ {count} imágenes válidas de {face}")
    label += 1

print(f"\nTotal de imágenes válidas: {len(facesData)}")

if len(facesData) == 0:
    raise RuntimeError("❌ No hay imágenes válidas para entrenar el modelo.")

faceRecognizer = cv.face.EigenFaceRecognizer_create()
faceRecognizer.train(facesData, np.array(labels))
faceRecognizer.write('Eigenface.xml')

print("\n✅ Modelo EigenFace entrenado y guardado como 'Eigenface.xml'")
