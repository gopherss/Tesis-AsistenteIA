from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database.db import Base


class SesionUsuario(Base):
    __tablename__ = "sesiones_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    inicio = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)
    duracion_segundos = Column(Integer, default=0)

    usuario = relationship("Usuario")


class MetricaCreacion(Base):
    __tablename__ = "metricas_creacion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"), nullable=True)
    tipo = Column(String(20), nullable=False)
    tiempo_total_segundos = Column(Float, default=0)
    tiempo_api_segundos = Column(Float, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario")
    sesion = relationship("Sesion")


class EncuestaSatisfaccion(Base):
    __tablename__ = "encuestas_satisfaccion"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    sesion_id = Column(Integer, ForeignKey("sesiones.id"), nullable=True)
    puntuacion = Column(Integer, nullable=False)
    comentario = Column(Text, default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario")
    sesion = relationship("Sesion")
