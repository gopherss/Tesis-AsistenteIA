from datetime import datetime, timedelta, timezone
from typing import Optional, Final
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import Usuario,RolEnum
from os import getenv

SECRET_KEY: Final[str] = getenv("SECRET_KEY", "default_secret")
ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 90))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

async def get_current_user(
    credentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: Optional[str] = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario

async def get_director_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    if current_user.rol.value != RolEnum.DIRECTOR:
        raise HTTPException(status_code=403, detail="Solo directores pueden realizar esta acción")
    return current_user


async def get_docente_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    if current_user.rol.value != RolEnum.DOCENTE:
        raise HTTPException(status_code=403, detail="Solo docentes pueden realizar esta acción")
    return current_user

