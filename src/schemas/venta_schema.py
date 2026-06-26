from pydantic import BaseModel, Field
from typing import List, Literal

class DetalleVentaSchema(BaseModel):
    id_producto: int
    cantidad: int = Field(gt=0, description="La cantidad debe ser mayor a cero")
    precio_unitario: float = Field(gt=0, description="El precio debe ser mayor a cero")

class VentaSchema(BaseModel):
    igv: float = Field(ge=0)
    total: float = Field(gt=0)
    medio_pago: Literal['EFECTIVO', 'TARJETA', 'YAPE', 'PLIN']
    # Obligamos a que la lista de detalles tenga al menos 1 producto
    detalles: List[DetalleVentaSchema] = Field(min_length=1)