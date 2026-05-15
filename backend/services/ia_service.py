from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generar_sesion_ia(datos, usuario: str = "Desconocido"):

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

    usage = response.usage
    if usage:
        print()
        print("=" * 60)
        print(f"  🤖  CONSUMO DE TOKENS — DeepSeek")
        print("=" * 60)
        print(f"  👤  Usuario        : {usuario}")
        print(f"  🆔  ID respuesta   : {response.id}")
        print(f"  📚  Modelo         : {response.model}")
        print(f"  📦  Objeto         : {response.object}")
        print(f"  ⏱️  Timestamp      : {response.created}")
        print(f"  ⬆️   Prompt        : {usage.prompt_tokens:>6} tokens")
        print(f"  ⬇️   Completion    : {usage.completion_tokens:>6} tokens")
        print(f"  🔄  Total          : {usage.total_tokens:>6} tokens")
        print(f"  🎯  Razón cierre   : {response.choices[0].finish_reason}")
        print(f"  📍  Índice choice  : {response.choices[0].index}")
        
        # Estos campos dependen del proveedor y pueden no estar siempre disponibles
        if hasattr(response, "system_fingerprint"):
            print(f"  🖇️  Fingerprint    : {response.system_fingerprint}")
        if hasattr(response, "latency"):
            print(f"  ⏳  Latencia       : {response.latency} ms")
        if hasattr(response, "estimated_cost"):
            print(f"  💲  Costo estimado : {response.estimated_cost} USD")

        print("-" * 60)
        print()

    return response.choices[0].message.content
