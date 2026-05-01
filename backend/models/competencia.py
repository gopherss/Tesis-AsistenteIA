from sqlalchemy import Column, Integer, String
from database.db import Base

class Competencia(Base):
    __tablename__ = "competencias"

    id = Column(Integer, primary_key=True)
    area = Column(String)
    nombre = Column(String)
    