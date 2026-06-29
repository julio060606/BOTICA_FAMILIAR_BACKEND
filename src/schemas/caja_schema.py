from pydantic import BaseModel, Field
from typing import Literal, Optional

class AbrirTurnoSchema(BaseModel):
    saldo_inicial: float = Field(ge=0, description="El saldo no puede ser negativo")
    observaciones: Optional[str] = ""

class CerrarTurnoSchema(BaseModel):
    saldo_fisico_real: float = Field(ge=0)
    observaciones: Optional[str] = ""

class MovimientoCajaSchema(BaseModel):
    tipo: Literal['INGRESO', 'EGRESO']
    monto: float = Field(gt=0, description="El monto debe ser mayor a 0")
    concepto: str = Field(min_length=3, description="Debe explicar el motivo")