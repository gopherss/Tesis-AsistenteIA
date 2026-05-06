from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db import Base

class Sesion(Base):
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    proposito = Column(Text, nullable=False)
    grado = Column(String, nullable=False)
    area = Column(String, nullable=False)
    tema = Column(String, nullable=False)
    competencias = Column(Text)   # puedes guardar como JSON string
    capacidades = Column(Text)
    desempeno = Column(Text)
    numero_ejercicios = Column(Integer, default=0)
    tiempo_sesion = Column(Integer, default=0)  # minutos

    contenido_ia: Mapped[str] = mapped_column(Text, default="")

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="sesiones")
