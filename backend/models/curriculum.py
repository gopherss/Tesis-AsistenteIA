# ==========================================
# models/curriculum.py
# SQLAlchemy Profesional
# ==========================================

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.db import Base


# ==========================================
# NIVEL
# ==========================================
class Nivel(Base):
    __tablename__ = "niveles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    grados = relationship("Grado", back_populates="nivel")


# ==========================================
# GRADO
# ==========================================
class Grado(Base):
    __tablename__ = "grados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    orden = Column(Integer, nullable=False)

    nivel_id = Column(Integer, ForeignKey("niveles.id"))

    nivel = relationship("Nivel", back_populates="grados")
    temas = relationship("Tema", back_populates="grado")


# ==========================================
# AREA
# ==========================================
class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    activo = Column(Boolean, default=True)

    competencias = relationship("Competencia", back_populates="area")
    temas = relationship("Tema", back_populates="area")


# ==========================================
# COMPETENCIA
# ==========================================
class Competencia(Base):
    __tablename__ = "competencias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)

    area_id = Column(Integer, ForeignKey("areas.id"))

    area = relationship("Area", back_populates="competencias")
    capacidades = relationship("Capacidad", back_populates="competencia")


# ==========================================
# CAPACIDAD
# ==========================================
class Capacidad(Base):
    __tablename__ = "capacidades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)

    competencia_id = Column(Integer, ForeignKey("competencias.id"))

    competencia = relationship("Competencia", back_populates="capacidades")


# ==========================================
# TEMA
# ==========================================
class Tema(Base):
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    activo = Column(Boolean, default=True)

    grado_id = Column(Integer, ForeignKey("grados.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))

    grado = relationship("Grado", back_populates="temas")
    area = relationship("Area", back_populates="temas")
    desempenos = relationship("Desempeno", back_populates="tema")


# ==========================================
# DESEMPEÑO
# ==========================================
class Desempeno(Base):
    __tablename__ = "desempenos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)

    tema_id = Column(Integer, ForeignKey("temas.id"))

    tema = relationship("Tema", back_populates="desempenos")
    