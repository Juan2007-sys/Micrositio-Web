from pydantic import BaseModel, Field, conint
from typing import Optional

class Ubicacion(BaseModel):
    nombre: str
    descripcion: str = None
    latitud: float
    longitud: float
    direccion: str = None