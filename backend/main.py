from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from routes.auth import router as auth_router
from routes.sesiones import router as sesiones_router
from routes.curriculum import router as curriculum_router

# Importar modelos para que SQLAlchemy registre las tablas
import models.user
import models.sesion
import models.curriculum

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Educativo IA",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sesiones_router)
app.include_router(curriculum_router)
