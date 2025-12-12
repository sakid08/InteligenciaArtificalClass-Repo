import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# ===================== CARGAR MODELO ENTRENADO =====================
print("Cargando modelo entrenado...")
try:
    modelo = joblib.load('modelo_arbol_decision.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Cargar columnas de características
    with open('feature_columns.txt', 'r') as f:
        feature_columns = [line.strip() for line in f]
    
    print("✓ Modelo cargado exitosamente")
    print(f"✓ Características: {len(feature_columns)}")
    print(f"✓ Clases del modelo: {modelo.classes_}")
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("  Primero debes entrenar el modelo con 'train_model.py'")
    exit()

# ===================== CONFIGURACIÓN DETECTOR =====================

CLASES_EMOCION = {
    0: 'Neutro',
    1: 'Feliz',
    2: 'Triste',
    3: 'Enojado',
    4: 'Sorprendido'
}

COLORES_EMOCION = {
    'Neutro': (200, 200, 200),
    'Feliz': (0, 255, 0),
    'Triste': (255, 0, 0),
    'Enojado': (0, 0, 255),
    'Sorprendido': (0, 255, 255)
}

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Puntos clave (deben ser los mismos que usaste para entrenar)
PUNTOS_CLAVE = {
    'ceja_izq_interior': 70,
    'ceja_izq_exterior': 107,
    'ceja_der_interior': 300,
    'ceja_der_exterior': 336,
    'ceja_izq_centro': 105,
    'ceja_der_centro': 334,
    'ojo_izq_superior': 159,
    'ojo_izq_inferior': 145,
    'ojo_der_superior': 386,
    'ojo_der_inferior': 374,
    'ojo_izq_exterior': 33,
    'ojo_der_exterior': 263,
    'ojo_izq_interior': 133,
    'ojo_der_interior': 362,
    'parpado_izq_medio': 160,
    'parpado_der_medio': 387,
    'ojo_izq_inf_medio': 144,
    'ojo_der_inf_medio': 373,
    'boca_superior': 13,
    'boca_inferior': 14,
    'comisura_izq': 61,
    'comisura_der': 291,
    'boca_izq': 78,
    'boca_der': 308,
    'labio_sup_centro': 0,
    'labio_inf_centro': 17,
    'labio_sup_izq_ext': 185,
    'labio_sup_der_ext': 409,
    'labio_inf_izq_ext': 62,
    'labio_inf_der_ext': 292,
    'labio_sup_interno': 12,
    'labio_inf_interno': 15,
    'nariz_puente': 168,
    'barbilla': 152,
    'nariz_lado_izq': 48,
    'nariz_lado_der': 278,
}

# ===================== FUNCIONES AUXILIARES =====================
def calcular_distancia(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def extraer_coordenadas(landmarks, w, h, indices):
    coords = {}
    for nombre, idx in indices.items():
        landmark = landmarks.landmark[idx]
        coords[nombre] = (int(landmark.x * w), int(landmark.y * h))
    return coords

def calcular_caracteristicas(coords):
    dist_referencia = calcular_distancia(coords['nariz_puente'], coords['barbilla'])
    
    if dist_referencia == 0:
        return None
    
    ratios = {}
    
    # 1. Ratio boca (apertura vertical)
    apertura_boca = calcular_distancia(coords['boca_superior'], coords['boca_inferior'])
    ratios['ratio_boca'] = apertura_boca / dist_referencia
    
    # 2. Ratio sonrisa
    ancho_boca_actual = calcular_distancia(coords['comisura_izq'], coords['comisura_der'])
    ancho_boca_neutral = calcular_distancia(coords['boca_izq'], coords['boca_der'])
    ratios['ratio_sonrisa'] = ancho_boca_actual / ancho_boca_neutral if ancho_boca_neutral > 0 else 1.0
    
    # 3. Ratio curvatura
    centro_boca_y = (coords['boca_superior'][1] + coords['boca_inferior'][1]) / 2
    comisura_izq_y = coords['comisura_izq'][1]
    comisura_der_y = coords['comisura_der'][1]
    desviacion_comisuras = ((comisura_izq_y - centro_boca_y) + (comisura_der_y - centro_boca_y)) / 2
    ratios['ratio_curvatura'] = desviacion_comisuras / dist_referencia
    
    # 4. Ratio cejas
    altura_ceja_izq = calcular_distancia(coords['ceja_izq_centro'], coords['ojo_izq_superior'])
    altura_ceja_der = calcular_distancia(coords['ceja_der_centro'], coords['ojo_der_superior'])
    altura_cejas_promedio = (altura_ceja_izq + altura_ceja_der) / 2
    ratios['ratio_cejas'] = altura_cejas_promedio / dist_referencia
    
    # 5. Ratio ojos (apertura)
    apertura_ojo_izq = calcular_distancia(coords['ojo_izq_superior'], coords['ojo_izq_inferior'])
    apertura_ojo_der = calcular_distancia(coords['ojo_der_superior'], coords['ojo_der_inferior'])
    apertura_ojos_promedio = (apertura_ojo_izq + apertura_ojo_der) / 2
    ratios['ratio_ojos'] = apertura_ojos_promedio / dist_referencia
    
    # 6. Ratio aspecto ojos
    ancho_ojo_izq = calcular_distancia(coords['ojo_izq_interior'], coords['ojo_izq_exterior'])
    ancho_ojo_der = calcular_distancia(coords['ojo_der_interior'], coords['ojo_der_exterior'])
    ancho_ojos_promedio = (ancho_ojo_izq + ancho_ojo_der) / 2
    ratio_aspecto_ojo_izq = ancho_ojo_izq / (apertura_ojo_izq + 0.001)
    ratio_aspecto_ojo_der = ancho_ojo_der / (apertura_ojo_der + 0.001)
    ratios['ratio_aspecto_ojos'] = (ratio_aspecto_ojo_izq + ratio_aspecto_ojo_der) / 2
    
    # 7. Ratio tensión párpados
    centro_ojo_izq_y = (coords['ojo_izq_superior'][1] + coords['ojo_izq_inferior'][1]) / 2
    centro_ojo_der_y = (coords['ojo_der_superior'][1] + coords['ojo_der_inferior'][1]) / 2
    tension_parpado_izq = centro_ojo_izq_y - coords['ojo_izq_inferior'][1]
    tension_parpado_der = centro_ojo_der_y - coords['ojo_der_inferior'][1]
    ratios['ratio_tension_parpados'] = ((tension_parpado_izq + tension_parpado_der) / 2) / dist_referencia
    
    # 8. Ratio grosor labios
    grosor_labio_sup = calcular_distancia(coords['labio_sup_centro'], coords['labio_sup_interno'])
    grosor_labio_inf = calcular_distancia(coords['labio_inf_centro'], coords['labio_inf_interno'])
    ratios['ratio_grosor_labios'] = (grosor_labio_sup + grosor_labio_inf) / dist_referencia
    
    # 9. Ratio compresión boca
    ancho_boca_externa = calcular_distancia(coords['labio_sup_izq_ext'], coords['labio_sup_der_ext'])
    ratios['ratio_compresion_boca'] = ancho_boca_externa / dist_referencia
    
    # 10. Ratio nariz boca
    dist_nariz_boca_izq = calcular_distancia(coords['nariz_lado_izq'], coords['comisura_izq'])
    dist_nariz_boca_der = calcular_distancia(coords['nariz_lado_der'], coords['comisura_der'])
    ratios['ratio_nariz_boca'] = ((dist_nariz_boca_izq + dist_nariz_boca_der) / 2) / dist_referencia
    
    # 11. Ratio distancia cejas
    dist_cejas = calcular_distancia(coords['ceja_izq_interior'], coords['ceja_der_interior'])
    ratios['ratio_dist_cejas'] = dist_cejas / dist_referencia
    
    return ratios

# ===================== DETECCIÓN EN TIEMPO REAL =====================
# Buffer para suavizar predicciones
predicciones_buffer = deque(maxlen=5)

print("\nIniciando cámara...")
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            coords = extraer_coordenadas(face_landmarks, w, h, PUNTOS_CLAVE)
            
            # Calcular características
            ratios = calcular_caracteristicas(coords)
            
            if ratios:
                # Convertir a array en el orden correcto
                X_new = np.array([[ratios[col] for col in feature_columns]])
                
                # Normalizar
                X_new_scaled = scaler.transform(X_new)
                
                # Predecir
                clase_predicha = modelo.predict(X_new_scaled)[0]
                prediccion_prob = modelo.predict_proba(X_new_scaled)[0]
                
                # Añadir al buffer
                predicciones_buffer.append(clase_predicha)
                
                # Suavizar predicción (moda del buffer)
                if len(predicciones_buffer) > 0:
                    clase_suavizada = max(set(predicciones_buffer), key=list(predicciones_buffer).count)
                    emocion = CLASES_EMOCION.get(clase_suavizada, 'Desconocido')
                    confianza = prediccion_prob[clase_predicha]
                else:
                    emocion = 'Neutro'
                    confianza = 0.5
                
                # Mostrar resultado
                color = COLORES_EMOCION.get(emocion, (200, 200, 200))
                
                # Dibujar rectángulo y texto
                cv2.rectangle(frame, (10, 10), (400, 80), color, -1)
                cv2.putText(frame, f"Emoción: {emocion}", (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(frame, f"Confianza: {confianza:.2f}", (20, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                
                
                # Mostrar todas las probabilidades
                y_offset = 100
                for i, prob in enumerate(prediccion_prob):
                    emocion_nombre = CLASES_EMOCION.get(i, f"Clase {i}")
                    cv2.putText(frame, f"{emocion_nombre}: {prob:.3f}", 
                               (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                               COLORES_EMOCION.get(emocion_nombre, (255, 255, 255)), 1)
                    y_offset += 20
    
    # Mostrar instrucciones
    cv2.putText(frame, "Presiona 'q' para salir", (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('Detección de Emociones - Modelo Entrenado', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nPrograma finalizado")