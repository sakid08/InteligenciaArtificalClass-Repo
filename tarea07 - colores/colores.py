import cv2 as cv
import numpy as np
import sys

# --- FUNCIÓN PARA REDIMENSIONAR IMÁGENES MUY GRANDES ---
def redimensionar_para_mostrar(imagen, max_ancho=1000):
    """
    Redimensiona una imagen para mostrarla en pantalla si su ancho supera
    un máximo, manteniendo la proporción original.
    """
    alto, ancho = imagen.shape[:2]
    if ancho > max_ancho:
        proporcion = max_ancho / float(ancho)
        nuevo_alto = int(alto * proporcion)
        imagen_redimensionada = cv.resize(imagen, (max_ancho, nuevo_alto), interpolation=cv.INTER_AREA)
        return imagen_redimensionada
    else:
        return imagen
# ---------------------------------------------------------

# Cargar imagen
img = cv.imread('D:\\saids\\Desktop\\InteligenciaArtificalClass-Repo\\tarea07 - colores\\figura.png', 1)

# Convertir a HSV
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# --- SEGMENTACIÓN SOLO PARA VERDE ---
umbralBajo = (35, 80, 80)
umbralAlto = (85, 255, 255)
mascara = cv.inRange(img_hsv, umbralBajo, umbralAlto)

# Procesar máscara (cerrado morfológico)
kernel = np.ones((5,5), np.uint8)
mascara_procesada = cv.morphologyEx(mascara, cv.MORPH_CLOSE, kernel)

# Aplicar la máscara a la imagen original
resultado = cv.bitwise_and(img, img, mask=mascara_procesada) 
resultado_con_centros = resultado.copy()

# Encontrar contornos
contornos, _ = cv.findContours(mascara_procesada, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

for i, contorno in enumerate(contornos):
    area = cv.contourArea(contorno)
    if area > 100:  # Filtrar ruidos pequeños
        M = cv.moments(contorno)
        
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue
        # Dibujar contorno en verde
        cv.drawContours(resultado_con_centros, [contorno], -1, (0, 255, 0), 2)
        
        # Dibujar centroide en rojo
        cv.circle(resultado_con_centros, (cX, cY), 5, (0, 0, 255), -1)
        
        # Escribir coordenadas
        cv.putText(resultado_con_centros, f"({cX},{cY})", (cX + 10, cY - 10), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# --- Mostrar resultados ---
cv.namedWindow('Imagen Original', cv.WINDOW_NORMAL)
cv.namedWindow('Imagen HSV', cv.WINDOW_NORMAL)
cv.namedWindow('Mascara (sin procesar)', cv.WINDOW_NORMAL)
cv.namedWindow('Mascara Procesada', cv.WINDOW_NORMAL)
cv.namedWindow('Resultado (Verde Aislado)', cv.WINDOW_NORMAL)
cv.namedWindow('Figuras con Centros', cv.WINDOW_NORMAL)

cv.imshow('Imagen Original', redimensionar_para_mostrar(img))
cv.imshow('Imagen HSV', redimensionar_para_mostrar(img_hsv))
cv.imshow('Mascara (sin procesar)', redimensionar_para_mostrar(mascara))
cv.imshow('Mascara Procesada', redimensionar_para_mostrar(mascara_procesada))
cv.imshow('Resultado (Verde Aislado)', redimensionar_para_mostrar(resultado))
cv.imshow('Figuras con Centros', redimensionar_para_mostrar(resultado_con_centros))

cv.waitKey(0)
cv.destroyAllWindows()
