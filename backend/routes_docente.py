from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from security import get_docente_user
from ai_service import ai_assistant
from pydantic import BaseModel
from word_service import generar_word_sesion

router = APIRouter(prefix="/docente", tags=["docente"])

class PlanificacionRequest(BaseModel):
    nivel: str
    grado: str
    area: str
    tema: str

class AnalisisRequest(BaseModel):
    curso: str
    total_estudiantes: int
    promedio_general: float
    asistencia: str

@router.get("/panel")
async def get_panel_docente(docente: Usuario = Depends(get_docente_user)):
    """Panel principal del docente con IA"""
    # Datos del docente para contextualizar
    docente_info = {
        "nombre": docente.nombre,
        "apellido": docente.apellido,
        "email": docente.email
    }
    
    # Obtener resumen mejorado con IA
    panel_data = await ai_assistant.get_panel_resumen(docente_info)
    
    return {
        "mensaje": f"Panel de {docente.nombre} {docente.apellido}",
        "rol": docente.rol.value,
        **panel_data
    }

@router.get("/planificacion")
async def get_planificacion(docente: Usuario = Depends(get_docente_user)):
    """Planificación del docente"""
    return {
        "mensaje": f"Planificación de {docente.nombre} {docente.apellido}",
        "semana_actual": {
            "lunes": [
                {"hora": "08:00", "curso": "Matemáticas", "tema": "Álgebra lineal", "aula": "101"},
                {"hora": "10:00", "curso": "Física", "tema": "Mecánica clásica", "aula": "205"}
            ],
            # ... resto de días
        },
        "ia_sugerencias": "Puedes usar /docente/planificar-sesion para crear sesiones con IA"
    }

@router.post("/planificar-sesion")
async def planificar_sesion_con_ia(
    datos: PlanificacionRequest,
    docente: Usuario = Depends(get_docente_user)
):
    """Planifica una sesión de clase usando IA"""
    try:
        sesion_planificada = await ai_assistant.planificar_sesion(datos.dict())
        return {
            "mensaje": "Sesión planificada exitosamente",
            "docente": f"{docente.nombre} {docente.apellido}",
            "planificacion": sesion_planificada,
            "datos_sesion": datos.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al planificar: {str(e)}")


@router.post("/analizar-estudiantes")
async def analizar_estudiantes_con_ia(
    datos: AnalisisRequest,
    docente: Usuario = Depends(get_docente_user)
):
    """Analiza el rendimiento de estudiantes usando IA"""
    try:
        analisis = await ai_assistant.analizar_estudiantes(datos.dict())
        return {
            "mensaje": "Análisis completado",
            "docente": f"{docente.nombre} {docente.apellido}",
            "analisis_ia": analisis,
            "datos_analizados": datos.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")

@router.get("/sesiones")
async def get_sesiones(docente: Usuario = Depends(get_docente_user)):
    """Sesiones del docente con sugerencias IA"""
    return {
        "mensaje": f"Sesiones de {docente.nombre} {docente.apellido}",
        "sesiones_activas": [
            {
                "id": 1,
                "curso": "Matemáticas",
                "tema": "Álgebra lineal",
                "fecha": "2024-03-15",
                "hora_inicio": "08:00",
                "hora_fin": "09:30",
                "aula": "101",
                "estado": "completada",
                "asistencia": 28
            },
        ],
        "sugerencia_ia": "¿Quieres optimizar alguna sesión? Usa /docente/planificar-sesion"
    }

@router.get("/chat-iniciar")
async def iniciar_chat_docente(docente: Usuario = Depends(get_docente_user)):
    """Inicia una conversación con el asistente IA"""

    mensaje_inicial = await ai_assistant.generate_response(
        f"""
        Saluda al docente {docente.nombre} de forma breve, amigable y moderna.
        Máximo 2 líneas.
        Preséntate como asistente IA educativo.
        Invítalo a pedir ayuda sobre clases, sesiones, estudiantes o ideas pedagógicas.
        No seas demasiado formal.
        """,
        {"rol": docente.rol.value}
    )

    return {
        "mensaje": "Chat iniciado",
        "asistente": mensaje_inicial,
        "docente": f"{docente.nombre} {docente.apellido}"
    }

@router.post("/chat-mensaje")
async def enviar_mensaje_chat(
    mensaje: str,
    docente: Usuario = Depends(get_docente_user)
):
    """Envía un mensaje al asistente IA"""
    contexto = {
        "docente": f"{docente.nombre} {docente.apellido}",
        "rol": docente.rol.value
    }
    
    respuesta = await ai_assistant.generate_response(mensaje, contexto)
    return {
        "mensaje_usuario": mensaje,
        "respuesta_ia": respuesta
    }
