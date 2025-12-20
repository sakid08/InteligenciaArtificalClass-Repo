import os

def crear_filosofia_profunda():
    print("--- GENERANDO BASE DE CONOCIMIENTO FILOSÓFICO DE ALTA PROFUNDIDAD ---")
    
    texto_teorico = """
    DOCUMENTO MAESTRO V3: ANALÍTICA EXISTENCIAL Y CRÍTICA DE LA RAZÓN ALGORÍTMICA
    
    ==========================================================================
    EJE 1: ONTOLOGÍA DE LA CRISIS DE SENTIDO (GEN Z)
    ==========================================================================
    
    1.1. JEAN-FRANÇOIS LYOTARD Y LA MERCANTILIZACIÓN DEL SABER
    - Tesis: El saber ha perdido su valor de uso (formación del espíritu) para adquirir un valor de cambio (datos/eficiencia).
    - La Gen Z y el Vacío: Al colapsar los metarrelatos (como el gran relato de la emancipación), el joven se enfrenta a un "presentismo" absoluto. El sentido no se proyecta al futuro, se agota en el instante del scroll.
    
    1.2. ZYGMUNT BAUMAN: ADIÓS A LOS VÍNCULOS DE DURACIÓN
    - Fragilidad del Vínculo Social: En la red, las relaciones se rigen por la lógica del "consumo". Se puede "desconectar" a alguien con un clic, eliminando la responsabilidad ética hacia el otro.
    - El Miedo al Compromiso: La identidad líquida es una defensa ante un mundo incierto; la Gen Z evita definiciones sólidas para no quedar "atrapada", lo que deriva en una angustia por falta de raíces.

    1.3. ÁNGELUS NOVUS Y EL NIHILISMO FRAGMENTADO
    - La saturación de información impide la experiencia (Erfahrung). El joven Gen Z "sabe" muchas cosas pero no "experimenta" un sentido profundo, quedando en una periferia existencial.

    ==========================================================================
    EJE 2: BYUNG-CHUL HAN: PSICOPOLÍTICA Y LA AUTO-EXPLOTACIÓN
    ==========================================================================
    
    2.1. DE LA SOCIEDAD DISCIPLINARIA A LA SOCIEDAD DEL RENDIMIENTO
    - Foucault vs. Han: Mientras Foucault hablaba de muros y hospitales (mandatos externos), Han describe un mundo de "gimnasios y oficinas de cristal". El individuo de la Gen Z no se siente oprimido, se siente "libre" para triunfar, lo cual es la forma más efectiva de dominación.
    - La Agonía del Eros: El algoritmo de citas y redes reduce al otro a un objeto de consumo. Se pierde el "misterio" del encuentro, reemplazándolo por un catálogo de perfiles.
    
    2.2. EL ENJAMBRE DIGITAL
    - A diferencia de la "masa" organizada, el "enjambre" digital (Gen Z en redes) no tiene una voz común. Son individuos aislados que reaccionan a estímulos, lo que impide una verdadera revolución o cambio de sentido social.

    ==========================================================================
    EJE 3: MICHEL FOUCAULT: GUBERNAMENTALIDAD Y BIO-ALGORITMOS
    ==========================================================================
    
    3.1. TECNOLOGÍAS DEL YO
    - Las redes sociales funcionan como dispositivos de "confesión" moderna. La Gen Z se ve obligada a narrar su vida constantemente, convirtiendo su intimidad en una técnica de control y visibilidad.
    
    3.2. EL PODER DE LA NORMALIZACIÓN
    - El algoritmo no castiga la desviación, la "corrige" mediante la invisibilidad. Si el contenido de un joven no encaja en el patrón estético/ideológico dominante, el sistema lo desplaza, forzando una autocensura inconsciente.

    ==========================================================================
    EJE 4: MARTIN HEIDEGGER: LA PREGUNTA POR LA TÉCNICA
    ==========================================================================
    
    4.1. EL OLVIDO DEL SER EN LA HIPERCONECTIVIDAD
    - El Dasein (ser-ahí) se pierde en la "cháchara" (Gerede) de las redes sociales. La comunicación constante en plataformas como X o TikTok es, para Heidegger, una forma de huir de uno mismo y de la angustia de la muerte.
    
    4.2. EL PELIGRO DE LA "CIBERNÉTICA"
    - Heidegger vaticinó que la cibernética reemplazaría a la filosofía. Cuando la IA "piensa" por nosotros y predice nuestras necesidades, el humano deja de hacerse las preguntas fundamentales sobre el sentido de su existencia.

    ==========================================================================
    EJE 5: JÜRGÉN HABERMAS: LA CRISIS DE LA VERDAD
    ==========================================================================
    
    5.1. ACCIÓN COMUNICATIVA VS. ALGORITMOS RECURSIVOS
    - La autonomía requiere que podamos dialogar y cambiar de opinión. Los algoritmos de recomendación son "monológicos": solo te dicen lo que ya piensas.
    - Esto destruye el "Espacio Público" y convierte la política en un espectáculo de emociones (posverdad), afectando la capacidad de la Gen Z para ejercer una ciudadanía autónoma.

    ==========================================================================
    EJE 6: SÍNTESIS PARA INTERPRETACIÓN RAG
    ==========================================================================
    - ENAJENACIÓN DIGITAL: El sujeto ya no se reconoce en sus propios deseos, pues estos son pre-fabricados por el sistema de recomendación.
    - DOLOR TRANSPARENTE: La obligación de mostrar felicidad en Instagram oculta una crisis de salud mental profunda.
    - AUTONOMÍA CERCADA: La ilusión de libertad dentro de una arquitectura digital diseñada para la permanencia y el consumo.
    """

    os.makedirs("archivos", exist_ok=True)
    ruta = "archivos/marco_teorico_filosofia_PROFUNDO.txt"
    
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto_teorico)
    
    print(f"💎 ARCHIVO DE ALTA DENSIDAD GENERADO: {ruta}")
    print(f"📈 Caracteres: {len(texto_teorico)}. Listo para análisis semántico avanzado.")

if __name__ == "__main__":
    crear_filosofia_profunda()