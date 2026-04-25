from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Usuario, RolEnum
from schemas import LoginRequest, UsuarioCreate, UsuarioResponse, TokenResponse
from security import (
    hash_password,
    verify_password,
    create_token,
    get_current_user,
    get_director_user
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(credenciales: LoginRequest, db: Session = Depends(get_db)):
    """Login de usuario"""
    usuario = db.query(Usuario).filter(Usuario.email == credenciales.email).first()
    
    if not usuario or not verify_password(credenciales.password, str(usuario.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    token = create_token(str(usuario.email))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register-docente", response_model=UsuarioResponse)
def register_docente(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):
    """Registra un docente (solo directores)"""
    
    if usuario_data.rol != RolEnum.DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se pueden registrar docentes en esta ruta"
        )
    
    existe = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    nuevo_usuario = Usuario(
        email=usuario_data.email,
        password=hash_password(usuario_data.password),
        nombre=usuario_data.nombre,
        apellido=usuario_data.apellido,
        rol=RolEnum.DOCENTE
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/dashboard")
def get_dashboard(director: Usuario = Depends(get_director_user)):
    """Dashboard exclusivo para directores"""
    return {
        "mensaje": f"Bienvenido al dashboard, {director.nombre} {director.apellido}",
        "rol": director.rol.value,
        "estadisticas": {
            "total_docentes": 15,
            "total_cursos": 45,
            "docentes_activos": 12,
            "cursos_activos": 38,
            "asistencia_promedio": "92%",
            "calificacion_promedio": 4.5
        },
        "proximos_eventos": [
            {"fecha": "2024-03-15", "evento": "Reunión de profesores", "hora": "14:00"},
            {"fecha": "2024-03-20", "evento": "Entrega de notas", "hora": "Todo el día"},
            {"fecha": "2024-03-25", "evento": "Consejo académico", "hora": "10:00"}
        ],
        "notificaciones": [
            "5 docentes pendientes de evaluación",
            "3 cursos nuevos por aprobar",
            "Actualización de planes de estudio necesaria"
        ]
    }

@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_user)):
    """Logout (cliente descarta el token)"""
    return {"mensaje": "Logout exitoso"}

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Obtiene datos del usuario autenticado"""
    return current_user
