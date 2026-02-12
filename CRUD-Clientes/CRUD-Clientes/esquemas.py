from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional

# --- ESQUEMAS PARA USUARIOS (Autenticación) ---
class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class Usuario(UsuarioBase):
    id: int
    is_active: bool

    # Sintaxis moderna para Pydantic v2
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# --- ESQUEMAS PARA CLIENTES (CRUD) ---
# Estos campos coinciden con la estructura de tu tabla en MySQL
class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    edad: int = Field(..., ge=0, le=150)
    fecha_nacimiento: date
    telefono: str = Field(..., min_length=9, max_length=20)
    direccion: str = Field(..., min_length=5, max_length=200)

class ClienteCreate(ClienteBase):
    """Esquema para crear un cliente (requiere todos los campos de ClienteBase)"""
    pass

class ClienteUpdate(BaseModel):
    """Esquema para actualizar (todos los campos son opcionales)"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    edad: Optional[int] = Field(None, ge=0, le=150)
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = Field(None, min_length=9, max_length=20)
    direccion: Optional[str] = Field(None, min_length=5, max_length=200)

class Cliente(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)