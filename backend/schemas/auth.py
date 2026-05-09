from pydantic import BaseModel, EmailStr
from models.user import RolEnum
from typing import List


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: str
    rol: RolEnum


class UsuarioUpdate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr


class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str
    apellido: str
    rol: RolEnum

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PaginatedDocentesResponse(BaseModel):
    total: int
    page: int
    limit: int
    data: List[UsuarioResponse]
    