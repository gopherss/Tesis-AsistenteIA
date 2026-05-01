from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import Usuario, RolEnum
from schemas.auth import LoginRequest, UsuarioCreate, UsuarioResponse, TokenResponse
from security.security import (
    hash_password,
    verify_password,
    create_token,
    get_current_user,
    get_director_user
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(credenciales: LoginRequest, db: Session = Depends(get_db)):
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

@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_user)):
    return {"mensaje": "Logout exitoso"}

@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user

