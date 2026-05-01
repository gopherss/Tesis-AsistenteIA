import ollama


def generar_sesion_ia(datos):
    minutos_desarrollo = max(datos.tiempo_sesion - 20, 20)

    prompt = f"""
Actúa como un DOCENTE EXPERTO DEL PERÚ especializado en EBR primaria.

Crea una sesión profesional y lista para usar.

Grado: {datos.grado}
Área: {datos.area}
Tema: {datos.tema}
Propósito: {datos.proposito}
Tiempo: {datos.tiempo_sesion} minutos
Ejercicios: {datos.numero_ejercicios}

Devuelve exactamente:

TÍTULO DE LA SESIÓN:
PROPÓSITO DE APRENDIZAJE:
COMPETENCIA:
CAPACIDADES:
CRITERIO DE EVALUACIÓN:
EVIDENCIA:

INICIO (10 min):
DESARROLLO ({minutos_desarrollo} min):
CIERRE (10 min):

MATERIALES:
ADAPTACIÓN:
EVALUACIÓN RÁPIDA:
"""

    respuesta = ollama.chat(
        model="phi3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return respuesta["message"]["content"]