from pydantic import BaseModel, ConfigDict


class GradoResponse(BaseModel):
    id: int
    nombre: str
    orden: int

    model_config = ConfigDict(from_attributes=True)


class GradoCreate(BaseModel):
    nombre: str
    orden: int


class GradoUpdate(BaseModel):
    nombre: str
    orden: int


class AreaResponse(BaseModel):
    id: int
    nombre: str
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class AreaCreate(BaseModel):
    nombre: str


class AreaUpdate(BaseModel):
    nombre: str


class CompetenciaResponse(BaseModel):
    id: int
    nombre: str
    area_id: int

    model_config = ConfigDict(from_attributes=True)


class CompetenciaCreate(BaseModel):
    nombre: str
    area_id: int


class CompetenciaUpdate(BaseModel):
    nombre: str
    area_id: int


class CapacidadResponse(BaseModel):
    id: int
    nombre: str
    competencia_id: int

    model_config = ConfigDict(from_attributes=True)


class CapacidadCreate(BaseModel):
    nombre: str
    competencia_id: int


class CapacidadUpdate(BaseModel):
    nombre: str
    competencia_id: int


class TemaResponse(BaseModel):
    id: int
    nombre: str
    grado_id: int
    area_id: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class TemaCreate(BaseModel):
    nombre: str
    area_id: int
    grado_id: int


class TemaUpdate(BaseModel):
    nombre: str
    area_id: int
    grado_id: int


class DesempenoResponse(BaseModel):
    id: int
    descripcion: str
    tema_id: int

    model_config = ConfigDict(from_attributes=True)


class DesempenoCreate(BaseModel):
    descripcion: str
    tema_id: int


class DesempenoUpdate(BaseModel):
    descripcion: str
    tema_id: int
