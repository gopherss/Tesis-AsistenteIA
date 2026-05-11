from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IniciarSesionUsuarioRequest(BaseModel):
    usuario_id: int


class SesionUsuarioResponse(BaseModel):
    id: int
    usuario_id: int
    inicio: datetime
    fin: Optional[datetime] = None
    clicks: int
    duracion_segundos: int

    class Config:
        from_attributes = True


class ActualizarClicksRequest(BaseModel):
    clicks: int


class FinalizarSesionRequest(BaseModel):
    duracion_segundos: int


class IniciarCreacionRequest(BaseModel):
    sesion_id: Optional[int] = None
    tipo: str


class SinPlataformaRequest(BaseModel):
    tiempo_total_segundos: float
    tema: str = ""
    area: str = ""
    grado: str = ""


class FinalizarCreacionRequest(BaseModel):
    tiempo_total_segundos: float
    tiempo_api_segundos: float


class EncuestaRequest(BaseModel):
    sesion_id: Optional[int] = None
    puntuacion: int
    comentario: str = ""


class EncuestaResponse(BaseModel):
    id: int
    usuario_id: int
    sesion_id: Optional[int]
    puntuacion: int
    comentario: str
    created_at: datetime

    class Config:
        from_attributes = True


class EstadisticasResponse(BaseModel):
    total_docentes: int
    total_sesiones_con_plataforma: int
    total_sesiones_sin_plataforma: int
    tiempo_promedio_con_plataforma: float
    tiempo_promedio_sin_plataforma: float
    tiempo_promedio_api: float
    clicks_promedio_por_sesion: float
    satisfaccion_promedio: float
    total_encuestas: int
    sesiones_por_docente: list[dict]
    satisfaccion_reciente: list[dict]
