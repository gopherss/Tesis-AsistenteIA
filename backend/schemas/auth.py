from pydantic import BaseModel, EmailStr
from models.user import RolEnum

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    apellido: str
    rol: RolEnum

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
