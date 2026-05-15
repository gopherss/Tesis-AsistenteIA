from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db
from models.user import Usuario, RolEnum
from models.metricas import SesionUsuario, MetricaCreacion, EncuestaSatisfaccion
from models.sesion import Sesion
from security.security import get_current_user, get_director_user
from schemas.metricas import (
    ActualizarClicksRequest,
    FinalizarSesionRequest,
    IniciarCreacionRequest,
    FinalizarCreacionRequest,
    EncuestaRequest,
    SinPlataformaRequest,
    EstadisticasResponse,
)
from datetime import datetime, timezone
from utils.logger import log

router = APIRouter(prefix="/metricas", tags=["metricas"])


@router.post("/iniciar-sesion")
def iniciar_sesion_usuario(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        sesion = SesionUsuario(
            usuario_id=current_user.id,
            inicio=datetime.now(timezone.utc),
        )
        db.add(sesion)
        db.commit()
        db.refresh(sesion)
        log(201, "POST /metricas/iniciar-sesion", f"{current_user.email}")
        return {"id": sesion.id, "inicio": sesion.inicio}
    except Exception as e:
        log(500, "POST /metricas/iniciar-sesion", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/sesion/{sesion_usuario_id}/clicks")
def actualizar_clicks(
    sesion_usuario_id: int,
    data: ActualizarClicksRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        sesion = db.query(SesionUsuario).filter(
            SesionUsuario.id == sesion_usuario_id,
            SesionUsuario.usuario_id == current_user.id,
        ).first()
        if not sesion:
            log(404, f"PUT /metricas/sesion/{sesion_usuario_id}/clicks", f"{current_user.email}")
            raise HTTPException(status_code=404, detail="Sesión de usuario no encontrada")
        sesion.clicks = data.clicks
        db.commit()
        log(200, f"PUT /metricas/sesion/{sesion_usuario_id}/clicks", f"{current_user.email}")
        return {"clicks": sesion.clicks}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /metricas/sesion/{sesion_usuario_id}/clicks", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/sesion/{sesion_usuario_id}/finalizar")
def finalizar_sesion_usuario(
    sesion_usuario_id: int,
    data: FinalizarSesionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        sesion = db.query(SesionUsuario).filter(
            SesionUsuario.id == sesion_usuario_id,
            SesionUsuario.usuario_id == current_user.id,
        ).first()
        if not sesion:
            log(404, f"PUT /metricas/sesion/{sesion_usuario_id}/finalizar", f"{current_user.email}")
            raise HTTPException(status_code=404, detail="Sesión de usuario no encontrada")
        sesion.fin = datetime.now(timezone.utc)
        sesion.duracion_segundos = data.duracion_segundos
        db.commit()
        log(200, f"PUT /metricas/sesion/{sesion_usuario_id}/finalizar", f"{current_user.email}")
        return {"message": "Sesión finalizada"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /metricas/sesion/{sesion_usuario_id}/finalizar", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/iniciar-creacion")
def iniciar_creacion(
    data: IniciarCreacionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        metrica = MetricaCreacion(
            usuario_id=current_user.id,
            sesion_id=data.sesion_id,
            tipo=data.tipo,
        )
        db.add(metrica)
        db.commit()
        db.refresh(metrica)
        log(201, "POST /metricas/iniciar-creacion", f"{current_user.email}")
        return {"id": metrica.id}
    except Exception as e:
        log(500, "POST /metricas/iniciar-creacion", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/creacion/{metrica_id}/finalizar")
def finalizar_creacion(
    metrica_id: int,
    data: FinalizarCreacionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        metrica = db.query(MetricaCreacion).filter(
            MetricaCreacion.id == metrica_id,
            MetricaCreacion.usuario_id == current_user.id,
        ).first()
        if not metrica:
            log(404, f"PUT /metricas/creacion/{metrica_id}/finalizar", f"{current_user.email}")
            raise HTTPException(status_code=404, detail="Métrica no encontrada")
        metrica.tiempo_total_segundos = data.tiempo_total_segundos
        metrica.tiempo_api_segundos = data.tiempo_api_segundos
        db.commit()
        log(200, f"PUT /metricas/creacion/{metrica_id}/finalizar", f"{current_user.email}")
        return {"message": "Métrica actualizada"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /metricas/creacion/{metrica_id}/finalizar", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/encuesta")
def crear_encuesta(
    data: EncuestaRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        if data.puntuacion < 1 or data.puntuacion > 5:
            log(400, "POST /metricas/encuesta", f"{current_user.email} — puntuación inválida")
            raise HTTPException(status_code=400, detail="Puntuación debe ser entre 1 y 5")
        encuesta = EncuestaSatisfaccion(
            usuario_id=current_user.id,
            sesion_id=data.sesion_id,
            puntuacion=data.puntuacion,
            comentario=data.comentario,
        )
        db.add(encuesta)
        db.commit()
        db.refresh(encuesta)
        log(201, "POST /metricas/encuesta", f"{current_user.email} — {data.puntuacion}/5")
        return {"message": "Encuesta registrada", "id": encuesta.id}
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /metricas/encuesta", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/registrar-sin-plataforma")
def registrar_sin_plataforma(
    data: SinPlataformaRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    try:
        metrica = MetricaCreacion(
            usuario_id=current_user.id,
            tipo="sin_plataforma",
            tiempo_total_segundos=data.tiempo_total_segundos,
        )
        db.add(metrica)
        db.commit()
        db.refresh(metrica)
        log(201, "POST /metricas/registrar-sin-plataforma", f"{current_user.email} — {data.tiempo_total_segundos}s")
        return {"message": "Registrado", "id": metrica.id}
    except Exception as e:
        log(500, "POST /metricas/registrar-sin-plataforma", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/estadisticas", response_model=EstadisticasResponse)
def obtener_estadisticas(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_director_user),
):
    try:
        total_docentes = db.query(Usuario).filter(Usuario.rol == RolEnum.DOCENTE).count()

        total_con = db.query(MetricaCreacion).filter(MetricaCreacion.tipo == "con_plataforma").count()
        total_sin = db.query(MetricaCreacion).filter(MetricaCreacion.tipo == "sin_plataforma").count()

        avg_con = db.query(func.avg(MetricaCreacion.tiempo_total_segundos)).filter(
            MetricaCreacion.tipo == "con_plataforma"
        ).scalar() or 0

        avg_sin = db.query(func.avg(MetricaCreacion.tiempo_total_segundos)).filter(
            MetricaCreacion.tipo == "sin_plataforma"
        ).scalar() or 0

        avg_api = db.query(func.avg(MetricaCreacion.tiempo_api_segundos)).filter(
            MetricaCreacion.tipo == "con_plataforma"
        ).scalar() or 0

        avg_clicks = db.query(func.avg(SesionUsuario.clicks)).scalar() or 0

        avg_satisfaccion = db.query(func.avg(EncuestaSatisfaccion.puntuacion)).scalar() or 0
        total_encuestas = db.query(EncuestaSatisfaccion).count()

        sesiones_por_docente = (
            db.query(
                Usuario.nombre,
                Usuario.apellido,
                func.count(MetricaCreacion.id).label("total"),
            )
            .join(MetricaCreacion, MetricaCreacion.usuario_id == Usuario.id, isouter=True)
            .filter(Usuario.rol == RolEnum.DOCENTE)
            .group_by(Usuario.id)
            .all()
        )

        satisfaccion_reciente = (
            db.query(
                EncuestaSatisfaccion.puntuacion,
                EncuestaSatisfaccion.comentario,
                EncuestaSatisfaccion.created_at,
                Usuario.nombre,
                Usuario.apellido,
            )
            .join(Usuario, EncuestaSatisfaccion.usuario_id == Usuario.id)
            .order_by(EncuestaSatisfaccion.created_at.desc())
            .limit(10)
            .all()
        )

        log(200, "GET /metricas/estadisticas", "Director consultó estadísticas")
        return {
            "total_docentes": total_docentes,
            "total_sesiones_con_plataforma": total_con,
            "total_sesiones_sin_plataforma": total_sin,
            "tiempo_promedio_con_plataforma": round(float(avg_con), 2),
            "tiempo_promedio_sin_plataforma": round(float(avg_sin), 2),
            "tiempo_promedio_api": round(float(avg_api), 2),
            "clicks_promedio_por_sesion": round(float(avg_clicks), 2),
            "satisfaccion_promedio": round(float(avg_satisfaccion), 2),
            "total_encuestas": total_encuestas,
            "sesiones_por_docente": [
                {"nombre": f"{r.nombre} {r.apellido}", "total": r.total}
                for r in sesiones_por_docente
            ],
            "satisfaccion_reciente": [
                {
                    "docente": f"{r.nombre} {r.apellido}",
                    "puntuacion": r.puntuacion,
                    "comentario": r.comentario,
                    "fecha": r.created_at.isoformat() if r.created_at else None,
                }
                for r in satisfaccion_reciente
            ],
        }
    except Exception as e:
        log(500, "GET /metricas/estadisticas", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
