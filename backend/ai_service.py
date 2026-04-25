import ollama
from typing import Dict, Any, Optional

class AIAssistant:
    def __init__(self, model: str = "phi3"):
        self.model = model
        self.system_prompt = """
            Eres un asistente IA para docentes de una institución educativa.

            Ayudas con:
            - planificación de clases
            - sesiones de aprendizaje
            - estrategias pedagógicas
            - análisis de estudiantes
            - ideas creativas

            Habla SIEMPRE en español.
            Usa tono natural, claro, moderno y profesional.
            Respuestas útiles y directas.
            No hables como robot."""
    
    async def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Genera una respuesta usando Ollama"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if context:
            messages.append({
                "role": "user", 
                "content": f"CONTEXTO: {context}\n\nSOLICITUD: {prompt}"
            })
        else:
            messages.append({"role": "user", "content": prompt})
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    async def get_panel_resumen(self, docente_info: Dict[str, Any]) -> Dict[str, Any]:
        """Genera el resumen del panel del docente"""
        prompt = f"""
        Genera un resumen del panel para el docente {docente_info['nombre']} {docente_info['apellido']}.
        Basado en un docente típico, proporciona:
        1. 3 sugerencias personalizadas para mejorar su práctica docente
        2. 2 recomendaciones de recursos educativos
        3. 1 consejo para manejo de estudiantes
        
        Responde en formato de lista numerada.
        """
        
        response = await self.generate_response(prompt, docente_info)
        
        return {
            "resumen": {
                "cursos_asignados": 4,
                "estudiantes_totales": 120,
                "sesiones_hoy": 2,
                "proxima_sesion": "Matemáticas - 10:00 AM",
                "tareas_pendientes": 8
            },
            "estadisticas_personales": {
                "asistencia_promedio": "95%",
                "calificacion_promedio": 4.2,
                "cursos_completados": 12,
                "horas_impartidas": 245,
                "recomendacion_ia": response
            },
            "anuncios": [
                "Reunión de departamento el viernes a las 3 PM",
                "Entrega de calificaciones antes del lunes",
                "Nuevo material disponible en la plataforma"
            ]
        }
    
    async def planificar_sesion(self, datos_sesion: Dict[str, Any]) -> str:
        """Planifica una sesión de clase usando IA"""
        prompt = f"""
        Diseña una sesión de clase completa con:
        - Nivel: {datos_sesion.get('nivel', 'No especificado')}
        - Grado: {datos_sesion.get('grado', 'No especificado')}
        - Área: {datos_sesion.get('area', 'No especificado')}
        - Tema: {datos_sesion.get('tema', 'No especificado')}
        
        Incluye:
        - Título de la sesión
        - Propósito de aprendizaje
        - Competencias a desarrollar
        - Inicio (15 min): Actividad motivadora
        - Desarrollo (45 min): Actividades principales
        - Cierre (15 min): Evaluación y reflexión
        - Materiales necesarios
        """
        return await self.generate_response(prompt, datos_sesion)
    
    async def analizar_estudiantes(self, datos_curso: Dict[str, Any]) -> str:
        """Analiza el rendimiento de estudiantes"""
        prompt = f"""
        Analiza el rendimiento del curso {datos_curso.get('curso')}:
        - Total estudiantes: {datos_curso.get('total_estudiantes')}
        - Promedio general: {datos_curso.get('promedio_general')}
        - Asistencia: {datos_curso.get('asistencia')}
        
        Proporciona:
        1. Análisis de la situación actual
        2. Recomendaciones para mejorar el rendimiento
        3. Estrategias pedagógicas sugeridas
        4. Actividades de refuerzo recomendadas
        """
        return await self.generate_response(prompt, datos_curso)

# Instancia global
ai_assistant = AIAssistant()