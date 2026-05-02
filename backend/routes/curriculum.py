from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models.curriculum import Area, Grado, Tema

router = APIRouter(prefix="/curriculum", tags=["curriculum"])


@router.get("/areas")
def listar_areas(db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.activo == True).all()


@router.get("/grados")
def listar_grados(db: Session = Depends(get_db)):
    return db.query(Grado).order_by(Grado.orden).all()


@router.get("/temas")
def listar_temas(
    area_id: int,
    grado_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Tema).filter(
        Tema.area_id == area_id,
        Tema.grado_id == grado_id
    ).all()

