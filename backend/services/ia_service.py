from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generar_sesion_ia(datos):
    minutos_desarrollo = max(datos.tiempo_sesion - 20, 20)

    prompt = f"""
Actúa como un DOCENTE EXPERTO del Currículo Nacional del Perú (EBR PRIMARIA).

IMPORTANTE:
- NO generes contenido genérico.
- Tema específico.
- Incluye ejercicios con solución paso a paso.

DATOS:
Grado: {datos.grado}
Área: {datos.area}
Tema: {datos.tema}
Propósito: {datos.proposito}
Tiempo: {datos.tiempo_sesion}
Ejercicios: {datos.numero_ejercicios}

TÍTULO DE LA SESIÓN:
PROPÓSITO DE APRENDIZAJE:
COMPETENCIA:
CAPACIDADES:
DESEMPEÑO:
CRITERIO DE EVALUACIÓN:
EVIDENCIA:

INICIO:
DESARROLLO:
EJERCICIOS:
CIERRE:
EVALUACIÓN:
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un docente experto del Perú"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content