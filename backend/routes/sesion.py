from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.sesion import Sesion
from models.user import Usuario
from schemas.sesion import SesionCreate, SesionResponse
from security.security import get_current_user

router = APIRouter(prefix="/sesiones", tags=["sesiones"])

@router.post("/", response_model=SesionResponse)
def crear_sesion(
    datos: SesionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    nueva_sesion = Sesion(
        titulo=datos.titulo,
        proposito=datos.proposito,
        grado=datos.grado,
        area=datos.area,
        tema=datos.tema,
        competencias=",".join(datos.competencias),
        capacidades=",".join(datos.capacidades),
        desempeno=",".join(datos.desempeno),
        numero_ejercicios=datos.numero_ejercicios,
        tiempo_sesion=datos.tiempo_sesion,
        usuario_id=current_user.id
    )
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)
    return nueva_sesion

@router.get("/", response_model=list[SesionResponse])
def listar_sesiones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Sesion).filter(Sesion.usuario_id == current_user.id).all()
