from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.db import get_db
from models.sesion import Sesion
from models.user import Usuario
from models.metricas import MetricaCreacion
from schemas.sesion import SesionCreate, SesionUpdate, SesionResponse
from security.security import get_current_user
from services.ia_service import generar_sesion_ia
from services.validator_service import validar_sesion
from services.pdf_service import generar_pdf_sesion
from utils.logger import log
import time

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
    try:
        resultado = validar_sesion(
            area=datos.area,
            tema=datos.tema
        )

        if not resultado["ok"]:
            log(400, "POST /sesiones", f"{current_user.email} — validación falló")
            raise HTTPException(
                status_code=400,
                detail=resultado
            )

        datos.tema = resultado["tema_corregido"]

        inicio_api = time.time()
        try:
            contenido_generado = generar_sesion_ia(datos, usuario=f"{current_user.nombre} {current_user.apellido}")
        except Exception:
            contenido_generado = (
                "No se pudo generar contenido con IA "
                "en este momento."
            )
        tiempo_api = round(time.time() - inicio_api, 2)

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

        if datos.tiempo_total_segundos:
            metrica = MetricaCreacion(
                usuario_id=current_user.id,
                sesion_id=nueva_sesion.id,
                tipo="con_plataforma",
                tiempo_total_segundos=datos.tiempo_total_segundos,
                tiempo_api_segundos=tiempo_api,
            )
            db.add(metrica)
            db.commit()

        log(201, "POST /sesiones", f"{current_user.email} — \"{nueva_sesion.titulo}\"")
        return nueva_sesion
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /sesiones", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get(
    "/",
    response_model=list[SesionResponse]
)
def listar_sesiones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesiones = (
            db.query(Sesion)
            .filter(Sesion.usuario_id == current_user.id)
            .order_by(Sesion.id.desc())
            .all()
        )
        log(200, "GET /sesiones", f"{current_user.email} — {len(sesiones)} sesiones")
        return sesiones
    except Exception as e:
        log(500, "GET /sesiones", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get(
    "/{sesion_id}",
    response_model=SesionResponse
)
def obtener_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesion = (
            db.query(Sesion)
            .filter(
                Sesion.id == sesion_id,
                Sesion.usuario_id == current_user.id
            )
            .first()
        )

        if not sesion:
            log(404, f"GET /sesiones/{sesion_id}", f"{current_user.email}")
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        return sesion
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"GET /sesiones/{sesion_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put(
    "/{sesion_id}",
    response_model=SesionResponse
)
def actualizar_sesion(
    sesion_id: int,
    datos: SesionUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesion = (
            db.query(Sesion)
            .filter(
                Sesion.id == sesion_id,
                Sesion.usuario_id == current_user.id
            )
            .first()
        )

        if not sesion:
            log(404, f"PUT /sesiones/{sesion_id}", f"{current_user.email}")
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        sesion.titulo = datos.titulo
        sesion.proposito = datos.proposito
        sesion.grado = datos.grado
        sesion.area = datos.area
        sesion.tema = datos.tema
        sesion.competencias = ",".join(datos.competencias)
        sesion.capacidades = ",".join(datos.capacidades)
        sesion.desempeno = ",".join(datos.desempeno)
        sesion.numero_ejercicios = datos.numero_ejercicios
        sesion.tiempo_sesion = datos.tiempo_sesion

        db.commit()
        db.refresh(sesion)

        log(200, f"PUT /sesiones/{sesion_id}", f"{current_user.email}")
        return sesion
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /sesiones/{sesion_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete(
    "/{sesion_id}",
    status_code=status.HTTP_200_OK
)
def eliminar_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesion = (
            db.query(Sesion)
            .filter(
                Sesion.id == sesion_id,
                Sesion.usuario_id == current_user.id
            )
            .first()
        )

        if not sesion:
            log(404, f"DELETE /sesiones/{sesion_id}", f"{current_user.email}")
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        titulo = sesion.titulo
        db.delete(sesion)
        db.commit()

        log(200, f"DELETE /sesiones/{sesion_id}", f"{current_user.email} — \"{titulo}\"")
        return {
            "message": "Sesión eliminada correctamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /sesiones/{sesion_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put(
    "/{sesion_id}/regenerar-ia",
    response_model=SesionResponse
)
def regenerar_contenido_ia(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesion = (
            db.query(Sesion)
            .filter(
                Sesion.id == sesion_id,
                Sesion.usuario_id == current_user.id
            )
            .first()
        )

        if not sesion:
            log(404, f"PUT /sesiones/{sesion_id}/regenerar-ia", f"{current_user.email}")
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        try:
            class Data:
                titulo = sesion.titulo
                proposito = sesion.proposito
                grado = sesion.grado
                area = sesion.area
                tema = sesion.tema
                tiempo_sesion = sesion.tiempo_sesion
                numero_ejercicios = sesion.numero_ejercicios

            sesion.contenido_ia = generar_sesion_ia(Data(), usuario=f"{current_user.nombre} {current_user.apellido}") or ""

        except Exception as e:
            error_msg = str(e)

            if "Insufficient Balance" in error_msg:
                log(402, f"PUT /sesiones/{sesion_id}/regenerar-ia", f"{current_user.email} — saldo insuficiente")
                raise HTTPException(
                    status_code=402,
                    detail="Saldo insuficiente en la API de IA"
                )

            log(500, f"PUT /sesiones/{sesion_id}/regenerar-ia", str(e))
            raise HTTPException(
                status_code=500,
                detail=f"Error IA: {error_msg}"
            )

        db.commit()
        db.refresh(sesion)

        log(200, f"PUT /sesiones/{sesion_id}/regenerar-ia", f"{current_user.email}")
        return sesion
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /sesiones/{sesion_id}/regenerar-ia", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/{sesion_id}/descargar-pdf")
def descargar_pdf_sesion(
    sesion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        sesion = (
            db.query(Sesion)
            .filter(
                Sesion.id == sesion_id,
                Sesion.usuario_id == current_user.id
            )
            .first()
        )

        if not sesion:
            log(404, f"GET /sesiones/{sesion_id}/descargar-pdf", f"{current_user.email}")
            raise HTTPException(
                status_code=404,
                detail="Sesión no encontrada"
            )

        try:
            pdf_buffer = generar_pdf_sesion(sesion)

            log(200, f"GET /sesiones/{sesion_id}/descargar-pdf", f"{current_user.email}")
            return StreamingResponse(
                iter([pdf_buffer.getvalue()]),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=sesion_{sesion.id}_{sesion.titulo.replace(' ', '_')}.pdf"
                }
            )
        except Exception as e:
            log(500, f"GET /sesiones/{sesion_id}/descargar-pdf", f"Error al generar PDF: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar el PDF: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"GET /sesiones/{sesion_id}/descargar-pdf", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
