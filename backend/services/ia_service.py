from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generar_sesion_ia(datos):

    prompt = f"""
Actúa como un DOCENTE EXPERTO del Currículo Nacional del Perú (EBR PRIMARIA).

IMPORTANTE:

- NO uses markdown.
- NO uses ###.
- NO uses tablas markdown.
- NO uses símbolos como | o ---.
- Usa texto limpio y profesional.
- Usa listas simples con guiones.
- No uses emojis.
- Incluye ejercicios con solución.
- Redacta contenido pedagógico real.
- Todo debe verse bien en PDF.

DATOS:

Grado: {datos.grado}
Área: {datos.area}
Tema: {datos.tema}
Propósito: {datos.proposito}
Tiempo: {datos.tiempo_sesion}
Número de ejercicios: {datos.numero_ejercicios}

ESTRUCTURA OBLIGATORIA:

TÍTULO DE LA SESIÓN
PROPÓSITO DE APRENDIZAJE
COMPETENCIA
CAPACIDADES
DESEMPEÑO
CRITERIO DE EVALUACIÓN
EVIDENCIA

INICIO
DESARROLLO
EJERCICIOS
SOLUCIÓN DE EJERCICIOS
CIERRE
EVALUACIÓN
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "Eres un docente experto del Perú"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
