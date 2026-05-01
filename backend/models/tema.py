from sqlalchemy import Column, Integer, String
from database.db import Base

class Tema(Base):
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True)
    grado = Column(String)
    area = Column(String)
    nombre = Column(String)
    