# ==========================================
# schemas/curriculum.py
# Pydantic v2
# ==========================================
from pydantic import BaseModel, ConfigDict


# ==========================================
# NIVEL
# ==========================================
class NivelResponse(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# GRADO
# ==========================================
class GradoResponse(BaseModel):
    id: int
    nombre: str
    orden: int
    nivel_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# AREA
# ==========================================
class AreaResponse(BaseModel):
    id: int
    nombre: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# COMPETENCIA
# ==========================================
class CompetenciaResponse(BaseModel):
    id: int
    nombre: str
    area_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# CAPACIDAD
# ==========================================
class CapacidadResponse(BaseModel):
    id: int
    nombre: str
    competencia_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# TEMA
# ==========================================
class TemaResponse(BaseModel):
    id: int
    nombre: str
    grado_id: int
    area_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# DESEMPEÑO
# ==========================================
class DesempenoResponse(BaseModel):
    id: int
    descripcion: str
    tema_id: int

    model_config = ConfigDict(from_attributes=True)


