from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.sesion import Sesion
from models.user import Usuario
from schemas.sesion import SesionCreate, SesionResponse
from security.security import get_current_user
from services.ia_service import generar_sesion_ia
from services.validator_service import validar_sesion

router = APIRouter(
    prefix="/sesiones",
    tags=["sesiones"]
)

@router.post(
    "/",
    response_model=SesionResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_sesion(
    datos: SesionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear nueva sesión pedagógica con validación inteligente + IA
    """

    # -----------------------------------------
    # 1. Validación inteligente
    # -----------------------------------------
    resultado = validar_sesion(
        area=datos.area,
        tema=datos.tema
    )

    if not resultado["ok"]:
        raise HTTPException(
            status_code=400,
            detail=resultado
        )

    # Tema corregido automáticamente
    datos.tema = resultado["tema_corregido"]

    # -----------------------------------------
    # 2. Generación IA
    # -----------------------------------------
    try:
        contenido_generado = generar_sesion_ia(datos)
    except Exception:
        contenido_generado = (
            "No se pudo generar contenido con IA "
            "en este momento."
        )

    # -----------------------------------------
    # 3. Guardado BD
    # -----------------------------------------
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
        contenido_ia=contenido_generado,
        usuario_id=current_user.id
    )

    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)

    return nueva_sesion


@router.get(
    "/",
    response_model=list[SesionResponse]
)
def listar_sesiones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista solo las sesiones del docente autenticado
    """

    sesiones = (
        db.query(Sesion)
        .filter(Sesion.usuario_id == current_user.id)
        .order_by(Sesion.id.desc())
        .all()
    )

    return sesiones

@router.get(
    "/{sesion_id}",
    response_model=SesionResponse
)
def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener una sesión específica del usuario
    """

    sesion = (
        db.query(Sesion)
        .filter(
            Sesion.id == sesion_id,
            Sesion.usuario_id == current_user.id
        )
        .first()
    )

    if not sesion:
        raise HTTPException(
            status_code=404,
            detail="Sesión no encontrada"
        )

    return sesion

@router.delete(
    "/{sesion_id}",
    status_code=status.HTTP_200_OK
)
def eliminar_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina una sesión del docente
    """

    sesion = (
        db.query(Sesion)
        .filter(
            Sesion.id == sesion_id,
            Sesion.usuario_id == current_user.id
        )
        .first()
    )

    if not sesion:
        raise HTTPException(
            status_code=404,
            detail="Sesión no encontrada"
        )

    db.delete(sesion)
    db.commit()

    return {
        "message": "Sesión eliminada correctamente"
    }

@router.put(
    "/{sesion_id}/regenerar-ia",
    response_model=SesionResponse
)
def regenerar_contenido_ia(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Regenera contenido IA de una sesión existente
    """

    sesion = (
        db.query(Sesion)
        .filter(
            Sesion.id == sesion_id,
            Sesion.usuario_id == current_user.id
        )
        .first()
    )

    if not sesion:
        raise HTTPException(
            status_code=404,
            detail="Sesión no encontrada"
        )

    try:
        class FakeData:
            titulo = sesion.titulo
            proposito = sesion.proposito
            grado = sesion.grado
            area = sesion.area
            tema = sesion.tema
            tiempo_sesion = sesion.tiempo_sesion
            numero_ejercicios = sesion.numero_ejercicios

        sesion.contenido_ia = generar_sesion_ia(FakeData())

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo regenerar IA"
        )

    db.commit()
    db.refresh(sesion)

    return sesion   