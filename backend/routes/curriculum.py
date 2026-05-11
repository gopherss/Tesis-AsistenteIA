from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.curriculum import Area, Grado, Tema, Competencia, Capacidad, Desempeno
from models.user import Usuario
from security.security import get_director_user

from schemas.curriculum import (
    GradoResponse, GradoCreate, GradoUpdate,
    AreaResponse, AreaCreate, AreaUpdate,
    CompetenciaResponse, CompetenciaCreate, CompetenciaUpdate,
    CapacidadResponse, CapacidadCreate, CapacidadUpdate,
    TemaResponse, TemaCreate, TemaUpdate,
    DesempenoResponse, DesempenoCreate, DesempenoUpdate,
)

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


# ============================================================
# ENDPOINTS PÚBLICOS (usados por docentes)
# ============================================================

@router.get("/areas", response_model=list[AreaResponse])
def listar_areas(db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.activo == True).all()


@router.get("/grados", response_model=list[GradoResponse])
def listar_grados(db: Session = Depends(get_db)):
    return db.query(Grado).order_by(Grado.orden).all()


@router.get("/temas", response_model=list[TemaResponse])
def listar_temas(
    area_id: int,
    grado_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Tema).filter(
        Tema.area_id == area_id,
        Tema.grado_id == grado_id
    ).all()


@router.get("/competencias", response_model=list[CompetenciaResponse])
def listar_competencias(
    area_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Competencia).filter(
        Competencia.area_id == area_id
    ).all()


@router.get("/capacidades", response_model=list[CapacidadResponse])
def listar_capacidades(
    competencia_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Capacidad).filter(
        Capacidad.competencia_id == competencia_id
    ).all()


@router.get("/desempenos", response_model=list[DesempenoResponse])
def listar_desempenos(
    tema_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Desempeno).filter(
        Desempeno.tema_id == tema_id
    ).all()


# ============================================================
# CRUD ADMIN (solo DIRECTOR)
# ============================================================

# ---------- GRADOS ----------

@router.get("/admin/grados", response_model=list[GradoResponse])
def admin_listar_grados(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    return db.query(Grado).order_by(Grado.orden).all()


@router.post("/admin/grados", response_model=GradoResponse, status_code=201)
def admin_crear_grado(
    data: GradoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    grado = Grado(nombre=data.nombre, orden=data.orden)
    db.add(grado)
    db.commit()
    db.refresh(grado)
    return grado


@router.put("/admin/grados/{grado_id}", response_model=GradoResponse)
def admin_actualizar_grado(
    grado_id: int,
    data: GradoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    grado = db.query(Grado).filter(Grado.id == grado_id).first()
    if not grado:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    grado.nombre = data.nombre
    grado.orden = data.orden
    db.commit()
    db.refresh(grado)
    return grado


@router.delete("/admin/grados/{grado_id}")
def admin_eliminar_grado(
    grado_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    grado = db.query(Grado).filter(Grado.id == grado_id).first()
    if not grado:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    db.delete(grado)
    db.commit()
    return {"message": "Grado eliminado"}


# ---------- ÁREAS ----------

@router.get("/admin/areas", response_model=list[AreaResponse])
def admin_listar_areas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    return db.query(Area).order_by(Area.nombre).all()


@router.post("/admin/areas", response_model=AreaResponse, status_code=201)
def admin_crear_area(
    data: AreaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    existe = db.query(Area).filter(Area.nombre == data.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El área ya existe")
    area = Area(nombre=data.nombre)
    db.add(area)
    db.commit()
    db.refresh(area)
    return area


@router.put("/admin/areas/{area_id}", response_model=AreaResponse)
def admin_actualizar_area(
    area_id: int,
    data: AreaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    existe = db.query(Area).filter(Area.nombre == data.nombre, Area.id != area_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="El área ya existe")
    area.nombre = data.nombre
    db.commit()
    db.refresh(area)
    return area


@router.delete("/admin/areas/{area_id}")
def admin_eliminar_area(
    area_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    db.delete(area)
    db.commit()
    return {"message": "Área eliminada"}


# ---------- COMPETENCIAS ----------

@router.get("/admin/competencias", response_model=list[CompetenciaResponse])
def admin_listar_competencias(
    area_id: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    query = db.query(Competencia)
    if area_id:
        query = query.filter(Competencia.area_id == area_id)
    return query.all()


@router.post("/admin/competencias", response_model=CompetenciaResponse, status_code=201)
def admin_crear_competencia(
    data: CompetenciaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    area = db.query(Area).filter(Area.id == data.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    competencia = Competencia(nombre=data.nombre, area_id=data.area_id)
    db.add(competencia)
    db.commit()
    db.refresh(competencia)
    return competencia


@router.put("/admin/competencias/{competencia_id}", response_model=CompetenciaResponse)
def admin_actualizar_competencia(
    competencia_id: int,
    data: CompetenciaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    area = db.query(Area).filter(Area.id == data.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    competencia.nombre = data.nombre
    competencia.area_id = data.area_id
    db.commit()
    db.refresh(competencia)
    return competencia


@router.delete("/admin/competencias/{competencia_id}")
def admin_eliminar_competencia(
    competencia_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    db.delete(competencia)
    db.commit()
    return {"message": "Competencia eliminada"}


# ---------- CAPACIDADES ----------

@router.get("/admin/capacidades", response_model=list[CapacidadResponse])
def admin_listar_capacidades(
    competencia_id: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    query = db.query(Capacidad)
    if competencia_id:
        query = query.filter(Capacidad.competencia_id == competencia_id)
    return query.all()


@router.post("/admin/capacidades", response_model=CapacidadResponse, status_code=201)
def admin_crear_capacidad(
    data: CapacidadCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    competencia = db.query(Competencia).filter(Competencia.id == data.competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    capacidad = Capacidad(nombre=data.nombre, competencia_id=data.competencia_id)
    db.add(capacidad)
    db.commit()
    db.refresh(capacidad)
    return capacidad


@router.put("/admin/capacidades/{capacidad_id}", response_model=CapacidadResponse)
def admin_actualizar_capacidad(
    capacidad_id: int,
    data: CapacidadUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    capacidad = db.query(Capacidad).filter(Capacidad.id == capacidad_id).first()
    if not capacidad:
        raise HTTPException(status_code=404, detail="Capacidad no encontrada")
    competencia = db.query(Competencia).filter(Competencia.id == data.competencia_id).first()
    if not competencia:
        raise HTTPException(status_code=404, detail="Competencia no encontrada")
    capacidad.nombre = data.nombre
    capacidad.competencia_id = data.competencia_id
    db.commit()
    db.refresh(capacidad)
    return capacidad


@router.delete("/admin/capacidades/{capacidad_id}")
def admin_eliminar_capacidad(
    capacidad_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    capacidad = db.query(Capacidad).filter(Capacidad.id == capacidad_id).first()
    if not capacidad:
        raise HTTPException(status_code=404, detail="Capacidad no encontrada")
    db.delete(capacidad)
    db.commit()
    return {"message": "Capacidad eliminada"}


# ---------- TEMAS ----------

@router.get("/admin/temas", response_model=list[TemaResponse])
def admin_listar_temas(
    area_id: int | None = None,
    grado_id: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    query = db.query(Tema)
    if area_id:
        query = query.filter(Tema.area_id == area_id)
    if grado_id:
        query = query.filter(Tema.grado_id == grado_id)
    return query.all()


@router.post("/admin/temas", response_model=TemaResponse, status_code=201)
def admin_crear_tema(
    data: TemaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    area = db.query(Area).filter(Area.id == data.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    grado = db.query(Grado).filter(Grado.id == data.grado_id).first()
    if not grado:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    tema = Tema(nombre=data.nombre, area_id=data.area_id, grado_id=data.grado_id)
    db.add(tema)
    db.commit()
    db.refresh(tema)
    return tema


@router.put("/admin/temas/{tema_id}", response_model=TemaResponse)
def admin_actualizar_tema(
    tema_id: int,
    data: TemaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    tema = db.query(Tema).filter(Tema.id == tema_id).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    area = db.query(Area).filter(Area.id == data.area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    grado = db.query(Grado).filter(Grado.id == data.grado_id).first()
    if not grado:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    tema.nombre = data.nombre
    tema.area_id = data.area_id
    tema.grado_id = data.grado_id
    db.commit()
    db.refresh(tema)
    return tema


@router.delete("/admin/temas/{tema_id}")
def admin_eliminar_tema(
    tema_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    tema = db.query(Tema).filter(Tema.id == tema_id).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    db.delete(tema)
    db.commit()
    return {"message": "Tema eliminado"}


# ---------- DESEMPEÑOS ----------

@router.get("/admin/desempenos", response_model=list[DesempenoResponse])
def admin_listar_desempenos(
    tema_id: int | None = None,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    query = db.query(Desempeno)
    if tema_id:
        query = query.filter(Desempeno.tema_id == tema_id)
    return query.all()


@router.post("/admin/desempenos", response_model=DesempenoResponse, status_code=201)
def admin_crear_desempeno(
    data: DesempenoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    tema = db.query(Tema).filter(Tema.id == data.tema_id).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    desempeno = Desempeno(descripcion=data.descripcion, tema_id=data.tema_id)
    db.add(desempeno)
    db.commit()
    db.refresh(desempeno)
    return desempeno


@router.put("/admin/desempenos/{desempeno_id}", response_model=DesempenoResponse)
def admin_actualizar_desempeno(
    desempeno_id: int,
    data: DesempenoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    desempeno = db.query(Desempeno).filter(Desempeno.id == desempeno_id).first()
    if not desempeno:
        raise HTTPException(status_code=404, detail="Desempeño no encontrado")
    tema = db.query(Tema).filter(Tema.id == data.tema_id).first()
    if not tema:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    desempeno.descripcion = data.descripcion
    desempeno.tema_id = data.tema_id
    db.commit()
    db.refresh(desempeno)
    return desempeno


@router.delete("/admin/desempenos/{desempeno_id}")
def admin_eliminar_desempeno(
    desempeno_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    desempeno = db.query(Desempeno).filter(Desempeno.id == desempeno_id).first()
    if not desempeno:
        raise HTTPException(status_code=404, detail="Desempeño no encontrado")
    db.delete(desempeno)
    db.commit()
    return {"message": "Desempeño eliminado"}
