from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import Usuario, RolEnum

from schemas.auth import (
    LoginRequest,
    UsuarioCreate,
    UsuarioResponse,
    TokenResponse,
    UsuarioUpdate,
    PaginatedDocentesResponse
)

from security.security import (
    hash_password,
    verify_password,
    create_token,
    get_current_user,
    get_director_user
)

router = APIRouter(prefix="/auth", tags=["auth"])


# =========================
# LOGIN
# =========================

@router.post("/login", response_model=TokenResponse)
def login(
    credenciales: LoginRequest,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == credenciales.email
    ).first()

    if not usuario or not verify_password(
        credenciales.password,
        str(usuario.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    token = create_token(str(usuario.email))

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================
# REGISTER DOCENTE
# =========================

@router.post(
    "/register-docente",
    response_model=UsuarioResponse
)
def register_docente(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):

    existe = db.query(Usuario).filter(
        Usuario.email == usuario_data.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
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


# =========================
# GET DOCENTES
# =========================

@router.get(
    "/docentes",
    response_model=PaginatedDocentesResponse
)
def get_docentes(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):

    query = db.query(Usuario).filter(
        Usuario.rol == RolEnum.DOCENTE
    )

    total = query.count()

    docentes = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": docentes
    }


# =========================
# UPDATE DOCENTE
# =========================

@router.put(
    "/docentes/{docente_id}",
    response_model=UsuarioResponse
)
def update_docente(
    docente_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):

    docente = db.query(Usuario).filter(
        Usuario.id == docente_id,
        Usuario.rol == RolEnum.DOCENTE
    ).first()

    if not docente:
        raise HTTPException(
            status_code=404,
            detail="Docente no encontrado"
        )

    docente.nombre = datos.nombre
    docente.apellido = datos.apellido
    docente.email = datos.email

    db.commit()
    db.refresh(docente)

    return docente


# =========================
# DELETE DOCENTE
# =========================

@router.delete("/docentes/{docente_id}")
def delete_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):

    docente = db.query(Usuario).filter(
        Usuario.id == docente_id,
        Usuario.rol == RolEnum.DOCENTE
    ).first()

    if not docente:
        raise HTTPException(
            status_code=404,
            detail="Docente no encontrado"
        )

    db.delete(docente)
    db.commit()

    return {
        "message": "Docente eliminado"
    }


# =========================
# LOGOUT
# =========================

@router.post("/logout")
def logout(
    current_user: Usuario = Depends(get_current_user)
):
    return {"mensaje": "Logout exitoso"}


# =========================
# ME
# =========================

@router.get(
    "/me",
    response_model=UsuarioResponse
)
def get_me(
    current_user: Usuario = Depends(get_current_user)
):
    return current_user
