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

from utils.logger import log

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
def listar_temas(area_id: int, grado_id: int, db: Session = Depends(get_db)):
    return db.query(Tema).filter(Tema.area_id == area_id, Tema.grado_id == grado_id).all()


@router.get("/competencias", response_model=list[CompetenciaResponse])
def listar_competencias(area_id: int, db: Session = Depends(get_db)):
    return db.query(Competencia).filter(Competencia.area_id == area_id).all()


@router.get("/capacidades", response_model=list[CapacidadResponse])
def listar_capacidades(competencia_id: int, db: Session = Depends(get_db)):
    return db.query(Capacidad).filter(Capacidad.competencia_id == competencia_id).all()


@router.get("/desempenos", response_model=list[DesempenoResponse])
def listar_desempenos(tema_id: int, db: Session = Depends(get_db)):
    return db.query(Desempeno).filter(Desempeno.tema_id == tema_id).all()


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
    try:
        grado = Grado(nombre=data.nombre, orden=data.orden)
        db.add(grado)
        db.commit()
        db.refresh(grado)
        log(201, "POST /curriculum/admin/grados", f"\"{grado.nombre}\"")
        return grado
    except Exception as e:
        log(500, "POST /curriculum/admin/grados", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/grados/{grado_id}", response_model=GradoResponse)
def admin_actualizar_grado(
    grado_id: int,
    data: GradoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        grado = db.query(Grado).filter(Grado.id == grado_id).first()
        if not grado:
            log(404, f"PUT /curriculum/admin/grados/{grado_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Grado no encontrado")
        grado.nombre = data.nombre
        grado.orden = data.orden
        db.commit()
        db.refresh(grado)
        log(200, f"PUT /curriculum/admin/grados/{grado_id}", f"\"{grado.nombre}\"")
        return grado
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/grados/{grado_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/grados/{grado_id}")
def admin_eliminar_grado(
    grado_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        grado = db.query(Grado).filter(Grado.id == grado_id).first()
        if not grado:
            log(404, f"DELETE /curriculum/admin/grados/{grado_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Grado no encontrado")
        nombre = grado.nombre
        db.delete(grado)
        db.commit()
        log(200, f"DELETE /curriculum/admin/grados/{grado_id}", f"\"{nombre}\"")
        return {"message": "Grado eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/grados/{grado_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    try:
        existe = db.query(Area).filter(Area.nombre == data.nombre).first()
        if existe:
            log(400, "POST /curriculum/admin/areas", f"Duplicado: \"{data.nombre}\"")
            raise HTTPException(status_code=400, detail="El área ya existe")
        area = Area(nombre=data.nombre)
        db.add(area)
        db.commit()
        db.refresh(area)
        log(201, "POST /curriculum/admin/areas", f"\"{area.nombre}\"")
        return area
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /curriculum/admin/areas", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/areas/{area_id}", response_model=AreaResponse)
def admin_actualizar_area(
    area_id: int,
    data: AreaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        area = db.query(Area).filter(Area.id == area_id).first()
        if not area:
            log(404, f"PUT /curriculum/admin/areas/{area_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        existe = db.query(Area).filter(Area.nombre == data.nombre, Area.id != area_id).first()
        if existe:
            log(400, f"PUT /curriculum/admin/areas/{area_id}", f"Duplicado: \"{data.nombre}\"")
            raise HTTPException(status_code=400, detail="El área ya existe")
        area.nombre = data.nombre
        db.commit()
        db.refresh(area)
        log(200, f"PUT /curriculum/admin/areas/{area_id}", f"\"{area.nombre}\"")
        return area
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/areas/{area_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/areas/{area_id}")
def admin_eliminar_area(
    area_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        area = db.query(Area).filter(Area.id == area_id).first()
        if not area:
            log(404, f"DELETE /curriculum/admin/areas/{area_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        nombre = area.nombre
        db.delete(area)
        db.commit()
        log(200, f"DELETE /curriculum/admin/areas/{area_id}", f"\"{nombre}\"")
        return {"message": "Área eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/areas/{area_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    try:
        area = db.query(Area).filter(Area.id == data.area_id).first()
        if not area:
            log(404, "POST /curriculum/admin/competencias", "Área no encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        competencia = Competencia(nombre=data.nombre, area_id=data.area_id)
        db.add(competencia)
        db.commit()
        db.refresh(competencia)
        log(201, "POST /curriculum/admin/competencias", f"\"{competencia.nombre}\"")
        return competencia
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /curriculum/admin/competencias", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/competencias/{competencia_id}", response_model=CompetenciaResponse)
def admin_actualizar_competencia(
    competencia_id: int,
    data: CompetenciaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
        if not competencia:
            log(404, f"PUT /curriculum/admin/competencias/{competencia_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Competencia no encontrada")
        area = db.query(Area).filter(Area.id == data.area_id).first()
        if not area:
            log(404, f"PUT /curriculum/admin/competencias/{competencia_id}", "Área padre no encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        competencia.nombre = data.nombre
        competencia.area_id = data.area_id
        db.commit()
        db.refresh(competencia)
        log(200, f"PUT /curriculum/admin/competencias/{competencia_id}", f"\"{competencia.nombre}\"")
        return competencia
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/competencias/{competencia_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/competencias/{competencia_id}")
def admin_eliminar_competencia(
    competencia_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        competencia = db.query(Competencia).filter(Competencia.id == competencia_id).first()
        if not competencia:
            log(404, f"DELETE /curriculum/admin/competencias/{competencia_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Competencia no encontrada")
        nombre = competencia.nombre
        db.delete(competencia)
        db.commit()
        log(200, f"DELETE /curriculum/admin/competencias/{competencia_id}", f"\"{nombre}\"")
        return {"message": "Competencia eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/competencias/{competencia_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    try:
        competencia = db.query(Competencia).filter(Competencia.id == data.competencia_id).first()
        if not competencia:
            log(404, "POST /curriculum/admin/capacidades", "Competencia no encontrada")
            raise HTTPException(status_code=404, detail="Competencia no encontrada")
        capacidad = Capacidad(nombre=data.nombre, competencia_id=data.competencia_id)
        db.add(capacidad)
        db.commit()
        db.refresh(capacidad)
        log(201, "POST /curriculum/admin/capacidades", f"\"{capacidad.nombre}\"")
        return capacidad
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /curriculum/admin/capacidades", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/capacidades/{capacidad_id}", response_model=CapacidadResponse)
def admin_actualizar_capacidad(
    capacidad_id: int,
    data: CapacidadUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        capacidad = db.query(Capacidad).filter(Capacidad.id == capacidad_id).first()
        if not capacidad:
            log(404, f"PUT /curriculum/admin/capacidades/{capacidad_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Capacidad no encontrada")
        competencia = db.query(Competencia).filter(Competencia.id == data.competencia_id).first()
        if not competencia:
            log(404, f"PUT /curriculum/admin/capacidades/{capacidad_id}", "Competencia padre no encontrada")
            raise HTTPException(status_code=404, detail="Competencia no encontrada")
        capacidad.nombre = data.nombre
        capacidad.competencia_id = data.competencia_id
        db.commit()
        db.refresh(capacidad)
        log(200, f"PUT /curriculum/admin/capacidades/{capacidad_id}", f"\"{capacidad.nombre}\"")
        return capacidad
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/capacidades/{capacidad_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/capacidades/{capacidad_id}")
def admin_eliminar_capacidad(
    capacidad_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        capacidad = db.query(Capacidad).filter(Capacidad.id == capacidad_id).first()
        if not capacidad:
            log(404, f"DELETE /curriculum/admin/capacidades/{capacidad_id}", "No encontrada")
            raise HTTPException(status_code=404, detail="Capacidad no encontrada")
        nombre = capacidad.nombre
        db.delete(capacidad)
        db.commit()
        log(200, f"DELETE /curriculum/admin/capacidades/{capacidad_id}", f"\"{nombre}\"")
        return {"message": "Capacidad eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/capacidades/{capacidad_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    try:
        area = db.query(Area).filter(Area.id == data.area_id).first()
        if not area:
            log(404, "POST /curriculum/admin/temas", "Área no encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        grado = db.query(Grado).filter(Grado.id == data.grado_id).first()
        if not grado:
            log(404, "POST /curriculum/admin/temas", "Grado no encontrado")
            raise HTTPException(status_code=404, detail="Grado no encontrado")
        tema = Tema(nombre=data.nombre, area_id=data.area_id, grado_id=data.grado_id)
        db.add(tema)
        db.commit()
        db.refresh(tema)
        log(201, "POST /curriculum/admin/temas", f"\"{tema.nombre}\"")
        return tema
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /curriculum/admin/temas", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/temas/{tema_id}", response_model=TemaResponse)
def admin_actualizar_tema(
    tema_id: int,
    data: TemaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        tema = db.query(Tema).filter(Tema.id == tema_id).first()
        if not tema:
            log(404, f"PUT /curriculum/admin/temas/{tema_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        area = db.query(Area).filter(Area.id == data.area_id).first()
        if not area:
            log(404, f"PUT /curriculum/admin/temas/{tema_id}", "Área no encontrada")
            raise HTTPException(status_code=404, detail="Área no encontrada")
        grado = db.query(Grado).filter(Grado.id == data.grado_id).first()
        if not grado:
            log(404, f"PUT /curriculum/admin/temas/{tema_id}", "Grado no encontrado")
            raise HTTPException(status_code=404, detail="Grado no encontrado")
        tema.nombre = data.nombre
        tema.area_id = data.area_id
        tema.grado_id = data.grado_id
        db.commit()
        db.refresh(tema)
        log(200, f"PUT /curriculum/admin/temas/{tema_id}", f"\"{tema.nombre}\"")
        return tema
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/temas/{tema_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/temas/{tema_id}")
def admin_eliminar_tema(
    tema_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        tema = db.query(Tema).filter(Tema.id == tema_id).first()
        if not tema:
            log(404, f"DELETE /curriculum/admin/temas/{tema_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        nombre = tema.nombre
        db.delete(tema)
        db.commit()
        log(200, f"DELETE /curriculum/admin/temas/{tema_id}", f"\"{nombre}\"")
        return {"message": "Tema eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/temas/{tema_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


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
    try:
        tema = db.query(Tema).filter(Tema.id == data.tema_id).first()
        if not tema:
            log(404, "POST /curriculum/admin/desempenos", "Tema no encontrado")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        desempeno = Desempeno(descripcion=data.descripcion, tema_id=data.tema_id)
        db.add(desempeno)
        db.commit()
        db.refresh(desempeno)
        log(201, "POST /curriculum/admin/desempenos", f"\"{desempeno.descripcion[:50]}...\"")
        return desempeno
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /curriculum/admin/desempenos", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/admin/desempenos/{desempeno_id}", response_model=DesempenoResponse)
def admin_actualizar_desempeno(
    desempeno_id: int,
    data: DesempenoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        desempeno = db.query(Desempeno).filter(Desempeno.id == desempeno_id).first()
        if not desempeno:
            log(404, f"PUT /curriculum/admin/desempenos/{desempeno_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Desempeño no encontrado")
        tema = db.query(Tema).filter(Tema.id == data.tema_id).first()
        if not tema:
            log(404, f"PUT /curriculum/admin/desempenos/{desempeno_id}", "Tema padre no encontrado")
            raise HTTPException(status_code=404, detail="Tema no encontrado")
        desempeno.descripcion = data.descripcion
        desempeno.tema_id = data.tema_id
        db.commit()
        db.refresh(desempeno)
        log(200, f"PUT /curriculum/admin/desempenos/{desempeno_id}", f"\"{desempeno.descripcion[:50]}...\"")
        return desempeno
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /curriculum/admin/desempenos/{desempeno_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/admin/desempenos/{desempeno_id}")
def admin_eliminar_desempeno(
    desempeno_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user)
):
    try:
        desempeno = db.query(Desempeno).filter(Desempeno.id == desempeno_id).first()
        if not desempeno:
            log(404, f"DELETE /curriculum/admin/desempenos/{desempeno_id}", "No encontrado")
            raise HTTPException(status_code=404, detail="Desempeño no encontrado")
        desc = desempeno.descripcion[:50]
        db.delete(desempeno)
        db.commit()
        log(200, f"DELETE /curriculum/admin/desempenos/{desempeno_id}", f"\"{desc}...\"")
        return {"message": "Desempeño eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /curriculum/admin/desempenos/{desempeno_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
