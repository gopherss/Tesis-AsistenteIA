from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database.db import Base
import enum

class RolEnum(str, enum.Enum):
    DIRECTOR = "DIRECTOR"
    DOCENTE = "DOCENTE"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    rol = Column(Enum(RolEnum), default=RolEnum.DOCENTE)
    sesiones = relationship("Sesion", back_populates="usuario")
    
