from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db import Base
import enum

class RolEnum(str, enum.Enum):
    DIRECTOR = "DIRECTOR"
    DOCENTE = "DOCENTE"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password = Column(String)
    nombre: Mapped[str] = mapped_column(String)
    apellido: Mapped[str] = mapped_column(String)
    rol = Column(Enum(RolEnum), default=RolEnum.DOCENTE)
    sesiones = relationship("Sesion", back_populates="usuario")
    
