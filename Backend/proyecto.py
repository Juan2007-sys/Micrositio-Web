from pydantic import BaseModel, Field, conint
from typing import Optional

class Proyecto(BaseModel):
    id: Optional[int] = Field(default=None, description="ID del proyecto")
    nombre: str = Field(..., description="Nombre del proyecto")
    descripcion: str = Field(..., description="Descripción del proyecto")
    url: str = Field(..., description="URL del proyecto")
    imagen: str = Field(..., description="Imagen del proyecto")
    video: Optional[str] = Field(default=None, description="Video del proyecto")
