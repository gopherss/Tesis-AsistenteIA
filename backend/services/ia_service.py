import ollama
    
def generar_sesion_ia(datos):
        minutos_desarrollo = max(datos.tiempo_sesion - 20, 20)

        prompt = f"""
    Actúa como un DOCENTE EXPERTO del Currículo Nacional del Perú (EBR PRIMARIA).

    IMPORTANTE:
    - NO generes contenido genérico.
    - El tema debe ser ESPECÍFICO y enseñable en una sesión.
    - Incluye ejercicios COMPLETOS con solución paso a paso.
    - Usa lenguaje claro para el docente.

    DATOS:
    Grado: {datos.grado}
    Área: {datos.area}
    Tema: {datos.tema}
    Propósito: {datos.proposito}
    Tiempo: {datos.tiempo_sesion} minutos
    Ejercicios: {datos.numero_ejercicios}

    ---

    TÍTULO DE LA SESIÓN:

    PROPÓSITO DE APRENDIZAJE:

    COMPETENCIA:
    (usar del currículo: “Resuelve problemas de cantidad”)

    CAPACIDADES:
    - Traduce cantidades a expresiones numéricas
    - Comunica su comprensión sobre números
    - Usa estrategias de cálculo

    ESTÁNDAR DE APRENDIZAJE:
    (Según ciclo IV si es 3ro o 4to)

    DESEMPEÑO:
    (Específico del grado)

    CRITERIO DE EVALUACIÓN:
    (Observables y medibles)

    EVIDENCIA:
    (Producto concreto del estudiante)

    ---

    INICIO (10 min):
    - Situación contextualizada (Perú)
    - Preguntas guía (mínimo 3 preguntas)

    ---

    DESARROLLO ({minutos_desarrollo} min):

    1. EXPLICACIÓN DIDÁCTICA:
    (Explica al docente cómo enseñar el tema paso a paso con ejemplo)

    2. EJEMPLO RESUELTO:
    (1 problema explicado paso a paso)

    3. EJERCICIOS ({datos.numero_ejercicios}):

    Ejercicio 1:
    Enunciado:
    Solución paso a paso:

    Ejercicio 2:
    Enunciado:
    Solución paso a paso:

    (continuar…)

    ---

    CIERRE (10 min):
    - 2 preguntas de reflexión
    - 1 actividad metacognitiva

    ---

    MATERIALES:
    (Lista concreta)

    ADAPTACIÓN:
    (Estrategias para estudiantes con dificultad y avanzados)

    ---

    EVALUACIÓN RÁPIDA:

    Pregunta 1:
    Respuesta:

    Pregunta 2:
    Respuesta:
    """

        respuesta = ollama.chat(
            model="phi3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return respuesta["message"]["content"]
