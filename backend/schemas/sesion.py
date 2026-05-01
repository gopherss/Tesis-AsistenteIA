from pydantic import BaseModel, field_validator
from typing import List

class SesionCreate(BaseModel):
    titulo: str
    proposito: str
    grado: str
    area: str
    tema: str
    competencias: List[str]
    capacidades: List[str]
    desempeno: List[str]
    numero_ejercicios: int
    tiempo_sesion: int

class SesionResponse(BaseModel):
    id: int
    titulo: str
    proposito: str
    grado: str
    area: str
    tema: str
    competencias: List[str]
    capacidades: List[str]
    desempeno: List[str]
    numero_ejercicios: int
    tiempo_sesion: int
    usuario_id: int

    @field_validator('competencias', 'capacidades', 'desempeno', mode='before')
    @classmethod
    def parse_string_to_list(cls, v):
        if isinstance(v, str):
            return [item.strip() for item in v.split(',') if item.strip()]
        return v

    class Config:
        from_attributes = True
