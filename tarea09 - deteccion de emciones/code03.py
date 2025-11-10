import cv2 as cv
import os

# Cargar el reconocedor y las etiquetas
faceRecognizer = cv.face.EigenFaceRecognizer_create()
faceRecognizer.read('Eigenface.xml')
faces = ['angry', 'happy', 'sad']

# Cargar video y el clasificador de rostros
cap = cv.VideoCapture(0)
rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 3)

    for (x, y, w, h) in rostros:
        frame2 = gray[y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (48, 48), interpolation=cv.INTER_CUBIC)

        result = faceRecognizer.predict(frame2)
        label = result[0]
        confidence = result[1]

        # Mostrar emoción o "Desconocido" según la confianza
        if confidence < 2800:
            emotion = faces[label]
            color = (0, 255, 0)  # verde
        else:
            emotion = 'Desconocido'
            color = (0, 0, 255)  # rojo

        # Dibujar rectángulo y texto con la emoción
        cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv.putText(frame, f'{emotion}', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv.LINE_AA)

    cv.imshow('Detección de emociones', frame)
    k = cv.waitKey(1)
    if k == 27:  # tecla ESC
        break

cap.release()
cv.destroyAllWindows()
