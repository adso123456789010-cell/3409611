from pydantic import BaseModel, Field
from typing import  Optional


class Product(BaseModel):
    codigo: str = Field(..., description="Codigo único del producto")
    nombre: str = Field(..., description="Nombre del producto")
    categoria: str
    precio: float = Field(..., gt= 0, description="Precio del producto debe ser mayor a 0 ")
    stock: int = Field(default=0, ge= 0, description="el Stock no puede ser negativo, por defecto es 0")
    compatible_con_: Optional[str] = None
    
from pydantic import BaseModel, Field


class OrdenCreate(BaseModel):
    placa: str = Field(..., max_length=6)
    modelo: str
    falla_reportada: str


class OrdenUpdate(BaseModel):
    nuevo_estado: str
    costo_reparacion: float