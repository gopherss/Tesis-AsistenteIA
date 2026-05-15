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

from utils.logger import log

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    credenciales: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        usuario = db.query(Usuario).filter(
            Usuario.email == credenciales.email
        ).first()

        if not usuario or not verify_password(
            credenciales.password,
            str(usuario.password)
        ):
            log(401, "POST /auth/login", credenciales.email)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        token = create_token(str(usuario.email))
        log(200, "POST /auth/login", f"{usuario.nombre} {usuario.apellido} ({usuario.email})")
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /auth/login", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/register-docente", response_model=UsuarioResponse)
def register_docente(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):
    try:
        existe = db.query(Usuario).filter(
            Usuario.email == usuario_data.email
        ).first()

        if existe:
            log(400, "POST /auth/register-docente", f"Email duplicado: {usuario_data.email}")
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

        log(201, "POST /auth/register-docente", f"{nuevo_usuario.email}")
        return nuevo_usuario
    except HTTPException:
        raise
    except Exception as e:
        log(500, "POST /auth/register-docente", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/docentes", response_model=PaginatedDocentesResponse)
def get_docentes(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):
    try:
        query = db.query(Usuario).filter(
            Usuario.rol == RolEnum.DOCENTE
        )

        total = query.count()
        docentes = query.offset(
            (page - 1) * limit
        ).limit(limit).all()

        log(200, "GET /auth/docentes", f"página {page}, {len(docentes)} docentes")
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "data": docentes
        }
    except HTTPException:
        raise
    except Exception as e:
        log(500, "GET /auth/docentes", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/docentes/{docente_id}", response_model=UsuarioResponse)
def update_docente(
    docente_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):
    try:
        docente = db.query(Usuario).filter(
            Usuario.id == docente_id,
            Usuario.rol == RolEnum.DOCENTE
        ).first()

        if not docente:
            log(404, f"PUT /auth/docentes/{docente_id}", "No encontrado")
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado"
            )

        docente.nombre = datos.nombre
        docente.apellido = datos.apellido
        docente.email = datos.email

        db.commit()
        db.refresh(docente)

        log(200, f"PUT /auth/docentes/{docente_id}", f"{docente.email}")
        return docente
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"PUT /auth/docentes/{docente_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/docentes/{docente_id}")
def delete_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    director: Usuario = Depends(get_director_user)
):
    try:
        docente = db.query(Usuario).filter(
            Usuario.id == docente_id,
            Usuario.rol == RolEnum.DOCENTE
        ).first()

        if not docente:
            log(404, f"DELETE /auth/docentes/{docente_id}", "No encontrado")
            raise HTTPException(
                status_code=404,
                detail="Docente no encontrado"
            )

        email = docente.email
        db.delete(docente)
        db.commit()

        log(200, f"DELETE /auth/docentes/{docente_id}", f"{email}")
        return {"message": "Docente eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        log(500, f"DELETE /auth/docentes/{docente_id}", str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/logout")
def logout(
    current_user: Usuario = Depends(get_current_user)
):
    log(200, "POST /auth/logout", f"{current_user.email}")
    return {"mensaje": "Logout exitoso"}


@router.get("/me", response_model=UsuarioResponse)
def get_me(
    current_user: Usuario = Depends(get_current_user)
):
    return current_user
