import cv2
import mediapipe as mp
import numpy as np
import csv
import os
from datetime import datetime

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --- Mapeo de emociones a clases numéricas ---
CLASES = {
    'Neutro': 0,
    'Feliz': 1,
    'Triste': 2,
    'Enojado': 3,
    'Sorprendido': 4
}

# --- Teclas para etiquetado manual ---
TECLAS_EMOCION = {
    ord('1'): 'Neutro',
    ord('2'): 'Feliz',
    ord('3'): 'Triste',
    ord('4'): 'Enojado',
    ord('5'): 'Sorprendido',
    ord(' '): 'Ninguna'  # Espacio para ignorar/omitir
}

# --- Archivo CSV ---
csv_filename = "emociones.csv"
header = [
    'timestamp', 'ratio_boca', 'ratio_sonrisa', 'ratio_curvatura', 'ratio_cejas', 
    'ratio_ojos', 'ratio_aspecto_ojos', 'ratio_tension_parpados', 
    'ratio_grosor_labios', 'ratio_compresion_boca', 
    'ratio_nariz_boca', 'ratio_dist_cejas', 'clase_manual'
]

# Puntos clave para detección de emociones (se mantiene igual)
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
    'nariz_punta': 1,
    'nariz_puente': 168,
    'barbilla': 152,
    'nariz_lado_izq': 48,
    'nariz_lado_der': 278,
}

# Crear CSV con encabezado si no existe
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

# Variable para almacenar la emoción manual
emocion_manual = None
ultima_tecla_presionada = None

def calcular_distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def extraer_coordenadas(landmarks, w, h, indices):
    """Extrae coordenadas de puntos específicos"""
    coords = {}
    for nombre, idx in indices.items():
        landmark = landmarks.landmark[idx]
        coords[nombre] = (int(landmark.x * w), int(landmark.y * h))
    return coords

def detectar_emocion(coords):
    """
    Detecta la emoción basándose en ratios de distancias faciales
    ENFOQUE PRINCIPAL EN OJOS ENTRECERRADOS Y BOCA FRUNCIDA PARA ENOJO
    """
    # Distancia de referencia
    dist_referencia = calcular_distancia(coords['nariz_puente'], coords['barbilla'])
    
    if dist_referencia == 0:
        return 'Neutro', 0, {}
    
    # ============ MEDIDAS BÁSICAS ============
    
    # Apertura de boca (vertical)
    apertura_boca = calcular_distancia(coords['boca_superior'], coords['boca_inferior'])
    ratio_boca = apertura_boca / dist_referencia
    
    # Ancho de la boca
    ancho_boca_actual = calcular_distancia(coords['comisura_izq'], coords['comisura_der'])
    ancho_boca_neutral = calcular_distancia(coords['boca_izq'], coords['boca_der'])
    ratio_sonrisa = ancho_boca_actual / ancho_boca_neutral if ancho_boca_neutral > 0 else 1.0
    
    # Curvatura de boca
    centro_boca_y = (coords['boca_superior'][1] + coords['boca_inferior'][1]) / 2
    comisura_izq_y = coords['comisura_izq'][1]
    comisura_der_y = coords['comisura_der'][1]
    desviacion_comisuras = ((comisura_izq_y - centro_boca_y) + (comisura_der_y - centro_boca_y)) / 2
    ratio_curvatura = desviacion_comisuras / dist_referencia
    
    # Altura de cejas
    altura_ceja_izq = calcular_distancia(coords['ceja_izq_centro'], coords['ojo_izq_superior'])
    altura_ceja_der = calcular_distancia(coords['ceja_der_centro'], coords['ojo_der_superior'])
    altura_cejas_promedio = (altura_ceja_izq + altura_ceja_der) / 2
    ratio_cejas = altura_cejas_promedio / dist_referencia
    
    # ============ MEDIDAS CRÍTICAS PARA ENOJO ============
    
    # 1. OJOS ENTRECERRADOS (CRÍTICO) - Apertura vertical reducida
    apertura_ojo_izq = calcular_distancia(coords['ojo_izq_superior'], coords['ojo_izq_inferior'])
    apertura_ojo_der = calcular_distancia(coords['ojo_der_superior'], coords['ojo_der_inferior'])
    apertura_ojos_promedio = (apertura_ojo_izq + apertura_ojo_der) / 2
    ratio_ojos = apertura_ojos_promedio / dist_referencia
    
    # 2. RATIO DE ASPECTO DEL OJO (ancho vs alto) - Ojos más "estrechos"
    ancho_ojo_izq = calcular_distancia(coords['ojo_izq_interior'], coords['ojo_izq_exterior'])
    ancho_ojo_der = calcular_distancia(coords['ojo_der_interior'], coords['ojo_der_exterior'])
    ancho_ojos_promedio = (ancho_ojo_izq + ancho_ojo_der) / 2
    
    # Ratio aspecto ojo (ancho/alto) - Aumenta cuando se entrecierran
    ratio_aspecto_ojo_izq = ancho_ojo_izq / (apertura_ojo_izq + 0.001)
    ratio_aspecto_ojo_der = ancho_ojo_der / (apertura_ojo_der + 0.001)
    ratio_aspecto_ojos = (ratio_aspecto_ojo_izq + ratio_aspecto_ojo_der) / 2
    
    # 3. TENSIÓN PÁRPADOS - Párpado inferior sube cuando entrecierras
    # Medimos la distancia del párpado inferior a la línea media del ojo
    centro_ojo_izq_y = (coords['ojo_izq_superior'][1] + coords['ojo_izq_inferior'][1]) / 2
    centro_ojo_der_y = (coords['ojo_der_superior'][1] + coords['ojo_der_inferior'][1]) / 2
    
    # Qué tan arriba está el párpado inferior del centro
    tension_parpado_izq = centro_ojo_izq_y - coords['ojo_izq_inferior'][1]
    tension_parpado_der = centro_ojo_der_y - coords['ojo_der_inferior'][1]
    ratio_tension_parpados = ((tension_parpado_izq + tension_parpado_der) / 2) / dist_referencia
    
    # 4. BOCA FRUNCIDA (CRÍTICO) - Labios hacia adentro, boca pequeña
    # Distancia entre los labios superior e inferior (grosor visible)
    grosor_labio_sup = calcular_distancia(coords['labio_sup_centro'], coords['labio_sup_interno'])
    grosor_labio_inf = calcular_distancia(coords['labio_inf_centro'], coords['labio_inf_interno'])
    ratio_grosor_labios = (grosor_labio_sup + grosor_labio_inf) / dist_referencia
    
    # 5. COMPRESIÓN HORIZONTAL DE LA BOCA - Boca más estrecha al fruncir
    ancho_boca_externa = calcular_distancia(coords['labio_sup_izq_ext'], coords['labio_sup_der_ext'])
    ratio_compresion_boca = ancho_boca_externa / dist_referencia
    
    # 6. RELACIÓN ANCHO/APERTURA DE BOCA - Boca cerrada pero no necesariamente ancha
    if apertura_boca > 0:
        ratio_forma_boca = ancho_boca_actual / (apertura_boca + 0.001)
    else:
        ratio_forma_boca = 10.0  # Valor alto si está cerrada
    
    # 7. NARIZ ARRUGADA (secundario) - Lados de nariz suben ligeramente
    dist_nariz_boca_izq = calcular_distancia(coords['nariz_lado_izq'], coords['comisura_izq'])
    dist_nariz_boca_der = calcular_distancia(coords['nariz_lado_der'], coords['comisura_der'])
    ratio_nariz_boca = ((dist_nariz_boca_izq + dist_nariz_boca_der) / 2) / dist_referencia
    
    # Distancia entre cejas (secundario ahora)
    dist_cejas = calcular_distancia(coords['ceja_izq_interior'], coords['ceja_der_interior'])
    ratio_dist_cejas = dist_cejas / dist_referencia

    # Ratios info
    ratios_info = {
        'ratio_boca': ratio_boca,
        'ratio_sonrisa': ratio_sonrisa,
        'ratio_curvatura': ratio_curvatura,
        'ratio_cejas': ratio_cejas,
        'ratio_ojos': ratio_ojos,
        'ratio_aspecto_ojos': ratio_aspecto_ojos,
        'ratio_tension_parpados': ratio_tension_parpados,
        'ratio_grosor_labios': ratio_grosor_labios,
        'ratio_compresion_boca': ratio_compresion_boca,
        'ratio_nariz_boca': ratio_nariz_boca,
        'ratio_dist_cejas': ratio_dist_cejas,
    }
    
    scores = {
        'Feliz': 0,
        'Triste': 0,
        'Enojado': 0,
        'Sorprendido': 0,
        'Neutro': 5  
    }
    
    # ===== FELICIDAD =====
    if ratio_sonrisa > 1.20:
        scores['Feliz'] += 4
        scores['Neutro'] -= 3
    elif ratio_sonrisa > 1.12:
        scores['Feliz'] += 2
        scores['Neutro'] -= 1
    
    if ratio_curvatura < -0.015:
        scores['Feliz'] += 4
        scores['Neutro'] -= 3
    elif ratio_curvatura < -0.008:
        scores['Feliz'] += 2
        scores['Neutro'] -= 1
    
    if 0.03 < ratio_boca < 0.10 and ratio_sonrisa > 1.15:
        scores['Feliz'] += 2
    
    # ===== TRISTEZA =====
    if ratio_curvatura > 0.012:
        scores['Triste'] += 5
        scores['Neutro'] -= 3
    elif ratio_curvatura > 0.006:
        scores['Triste'] += 3
        scores['Neutro'] -= 2
    
    if ratio_sonrisa < 1.05:
        scores['Triste'] += 2
    
    if ratio_boca < 0.025:
        scores['Triste'] += 1
    
    # ===== ENOJO (REDISEÑADO - ENFOQUE EN OJOS Y BOCA) =====
    puntos_enojo = 0
    
    # CRITERIO 1: OJOS ENTRECERRADOS (MUY IMPORTANTE)
    if ratio_ojos < 0.055:  # Ojos MUY entrecerrados
        scores['Enojado'] += 8
        puntos_enojo += 3
        scores['Neutro'] -= 4
    elif ratio_ojos < 0.068:  # Ojos moderadamente entrecerrados
        scores['Enojado'] += 5
        puntos_enojo += 2
        scores['Neutro'] -= 2
    elif ratio_ojos < 0.078:  # Ojos ligeramente entrecerrados
        scores['Enojado'] += 3
        puntos_enojo += 1
    
    # CRITERIO 2: RATIO DE ASPECTO (ojos más alargados/estrechos)
    if ratio_aspecto_ojos > 5.5:  # Ojos muy alargados
        scores['Enojado'] += 6
        puntos_enojo += 2
    elif ratio_aspecto_ojos > 4.8:  # Ojos alargados
        scores['Enojado'] += 4
        puntos_enojo += 1
    
    # CRITERIO 3: TENSIÓN EN PÁRPADOS (párpado inferior sube)
    if ratio_tension_parpados < -0.008:  # Párpados muy tensos
        scores['Enojado'] += 5
        puntos_enojo += 1.5
    elif ratio_tension_parpados < -0.004:
        scores['Enojado'] += 3
        puntos_enojo += 0.5
    
    # CRITERIO 4: BOCA FRUNCIDA - Labios delgados (hacia adentro)
    if ratio_grosor_labios < 0.012:  # Labios MUY hacia adentro
        scores['Enojado'] += 7
        puntos_enojo += 2.5
        scores['Neutro'] -= 3
    elif ratio_grosor_labios < 0.018:  # Labios moderadamente hacia adentro
        scores['Enojado'] += 5
        puntos_enojo += 1.5
        scores['Neutro'] -= 2
    elif ratio_grosor_labios < 0.025:  # Labios ligeramente hacia adentro
        scores['Enojado'] += 3
        puntos_enojo += 0.5
    
    # CRITERIO 5: BOCA COMPRIMIDA HORIZONTALMENTE
    if ratio_compresion_boca < 0.30:  # Boca muy estrecha
        scores['Enojado'] += 5
        puntos_enojo += 1.5
    elif ratio_compresion_boca < 0.35:  # Boca estrecha
        scores['Enojado'] += 3
        puntos_enojo += 1
    
    # CRITERIO 6: BOCA CERRADA con tensión
    if ratio_boca < 0.025 and ratio_sonrisa < 1.08:  # Boca cerrada y tensa
        scores['Enojado'] += 4
        puntos_enojo += 1
    elif ratio_boca < 0.035 and ratio_sonrisa < 1.10:
        scores['Enojado'] += 2
        puntos_enojo += 0.5
    
    # CRITERIO 7: Cejas juntas (SECUNDARIO ahora)
    if ratio_dist_cejas < 0.28:
        scores['Enojado'] += 3
        puntos_enojo += 0.5
    
    # CRITERIO 8: Nariz arrugada
    if ratio_nariz_boca < 0.22:
        scores['Enojado'] += 2
        puntos_enojo += 0.5

    
    # PENALIZACIONES
    if ratio_sonrisa > 1.15:  # Está sonriendo
        scores['Enojado'] = 0
        puntos_enojo = 0
    
    if ratio_curvatura < -0.010:  # Comisuras hacia arriba
        scores['Enojado'] = max(0, scores['Enojado'] - 6)
        puntos_enojo = max(0, puntos_enojo - 2)
    
    if ratio_ojos > 0.095:  # Ojos muy abiertos (incompatible)
        scores['Enojado'] = max(0, scores['Enojado'] - 5)
    
    # Requiere al menos 2.5 puntos para ser enojado
    if puntos_enojo < 2.5:
        scores['Enojado'] = 0
    
    # ===== SORPRESA =====
    condiciones_sorpresa = 0
    
    if ratio_cejas > 0.18:
        scores['Sorprendido'] += 4
        condiciones_sorpresa += 1
    
    if ratio_ojos > 0.09:
        scores['Sorprendido'] += 4
        condiciones_sorpresa += 1
    
    if ratio_boca > 0.15:
        scores['Sorprendido'] += 4
        condiciones_sorpresa += 1
    
    if condiciones_sorpresa < 2:
        scores['Sorprendido'] = 0
    else:
        scores['Neutro'] -= 5
    
    # Asegurar que los scores no sean negativos
    for emocion in scores:
        scores[emocion] = max(0, scores[emocion])
    
    # Seleccionar emoción con mayor score
    emocion = max(scores, key=scores.get)
    confianza = scores[emocion]
    
    if confianza < 3:
        emocion = 'Neutro'
        confianza = 5
    
    return emocion, confianza, ratios_info


# Configuración de colores por emoción
COLORES_EMOCION = {
    'Neutro': (200, 200, 200),
    'Feliz': (0, 255, 0),
    'Triste': (255, 0, 0),
    'Enojado': (0, 0, 255),
    'Sorprendido': (0, 255, 255),
    'Ninguna': (100, 100, 100)
}

# Captura de video
cap = cv2.VideoCapture(0)

# Mostrar instrucciones
print("\n" + "="*50)
print("CONTROL MANUAL DE ETIQUETADO")
print("="*50)
print("Teclas para etiquetar emoción:")
print("  1 = Neutro")
print("  2 = Feliz")
print("  3 = Triste")
print("  4 = Enojado")
print("  5 = Sorprendido")
print("  ESPACIO = Ignorar/no guardar")
print("  q = Salir")
print("="*50)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    # Variables para almacenar datos
    emocion_auto = 'Neutro'
    confianza_auto = 0
    ratios_info = {}
    
    # En lugar de llamar a detectar_emocion, simplemente inicializa las variables
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            coords = extraer_coordenadas(face_landmarks, w, h, PUNTOS_CLAVE)
            # NO llamar a detectar_emocion aquí
            emocion_auto = 'Neutro'
            confianza_auto = 0
            ratios_info = {}
            
            # Puedes mantener los puntos dibujados si quieres
            for nombre, (x, y) in coords.items():
                cv2.circle(frame, (x, y), 2, (200, 200, 200), -1)

    # Y en la sección de guardado:
    elif key == 13:  # Tecla ENTER para guardar
        if emocion_manual and results.multi_face_landmarks:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            if emocion_manual != 'Ninguna':
                # Crear fila con todos los ratios en 0
                fila = [timestamp] + [0] * (len(header) - 2)
                fila.append(CLASES.get(emocion_manual, 0))
                
                with open(csv_filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fila)
                
                print(f"✓ Guardado: {emocion_manual} | {timestamp}")
            else:
                print(f"✗ Omitido (ESPACIO)")
            
            emocion_manual = None
    
    # Mostrar información en pantalla
    y_offset = 30
    line_height = 30
    
    # 1. Emoción automática detectada
    cv2.putText(frame, f"Auto: {emocion_auto} ({confianza_auto:.1f})", 
                (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORES_EMOCION[emocion_auto], 2)
    y_offset += line_height
    
    # 2. Emoción manual seleccionada (si hay)
    if emocion_manual:
        cv2.putText(frame, f"Manual: {emocion_manual}", 
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        y_offset += line_height
    else:
        cv2.putText(frame, "Manual: (presione 1-5)", 
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 1)
        y_offset += line_height
    
    # 3. Última tecla presionada
    if ultima_tecla_presionada:
        cv2.putText(frame, f"Ultima tecla: {ultima_tecla_presionada}", 
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 1)
    y_offset += line_height
    
    # 4. Estado de guardado
    if emocion_manual:
        estado_color = (0, 255, 0) if emocion_manual != 'Ninguna' else (0, 165, 255)
        estado_texto = "GUARDAR (Enter)" if emocion_manual != 'Ninguna' else "OMITIR (Enter)"
        cv2.putText(frame, estado_texto, 
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, estado_color, 1)
    
    # Manejo de teclas
    key = cv2.waitKey(1) & 0xFF
    
    if key in TECLAS_EMOCION:
        emocion_manual = TECLAS_EMOCION[key]
        ultima_tecla_presionada = chr(key) if key != ord(' ') else 'ESPACIO'
        print(f"Emoción manual seleccionada: {emocion_manual}")
    
    elif key == 13:  # Tecla ENTER para guardar
        if emocion_manual and results.multi_face_landmarks:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            
            if emocion_manual != 'Ninguna':  # Solo guardar si no es "omitir"
                fila = [timestamp] + [0] * (len(header) - 2)  # Todos los ratios en 0
                fila.append(CLASES.get(emocion_manual, 0))
                
                with open(csv_filename, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fila)
                
                print(f"✓ Guardado: {emocion_manual} | {timestamp}")
            
            emocion_manual = None
    
    elif key == ord('q'):
        break
    
    cv2.imshow('Detector de Emociones (Manual: 1-5, ENTER=Guardar)', frame)

cap.release()
cv2.destroyAllWindows()
print("\nPrograma finalizado. Datos guardados en:", csv_filename)