from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Contacto(BaseModel):
    nombre: str = Field(..., description="Nombre del contacto")
    email: EmailStr = Field(..., description="Email del contacto")
    mensaje: str = Field(..., description="Mensaje del contacto")
    telefono: Optional[str] = Field(default=None, description="Teléfono del contacto")