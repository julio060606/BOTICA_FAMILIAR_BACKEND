from pydantic import BaseModel, Field
from typing import Optional

class TicketVentaSchema(BaseModel):
    id_turno: int = Field(..., gt=0)
    id_usuario: int = Field(..., gt=0)
    nro_ticket: str = Field(..., min_length=5, max_length=50)
    subtotal: float = Field(..., ge=0)
    igv: float = Field(..., ge=0)
    total: float = Field(..., gt=0)
    medio_pago: str = Field(..., pattern="^(EFECTIVO|TARJETA|YAPE|PLIN)$")
    
    # Campos opcionales (tienen DEFAULT en tu base de datos)
    cliente_doc: Optional[str] = "00000000"
    cliente_nombre: Optional[str] = "Público en General"
    estado: Optional[str] = "VALIDO"