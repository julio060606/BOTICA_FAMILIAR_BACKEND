from pydantic import BaseModel, Field, model_validator
from typing import List, Literal, Optional

class DetalleVentaSchema(BaseModel):
    id_producto: int
    cantidad: int = Field(gt=0, description="La cantidad debe ser mayor a cero")
    precio_unitario: float = Field(gt=0, description="El precio debe ser mayor a cero")

class VentaSchema(BaseModel):
    igv: float = Field(ge=0)
    total: float = Field(gt=0)
    medio_pago: Literal['EFECTIVO', 'TARJETA', 'YAPE', 'PLIN']
    monto_entregado: Optional[float] = 0.0
    vuelto: Optional[float] = 0.0
    detalles: List[DetalleVentaSchema] = Field(min_length=1)

    # El superpoder: Validar la matemática antes de molestar a la base de datos
    @model_validator(mode='after')
    def validar_efectivo(self):
        if self.medio_pago == 'EFECTIVO':
            if self.monto_entregado < self.total:
                raise ValueError(f"El monto entregado (S/ {self.monto_entregado}) es menor al total a pagar (S/ {self.total})")
            # Auto-calculamos el vuelto en el backend por seguridad extrema
            self.vuelto = round(self.monto_entregado - self.total, 2)
        else:
            # Si pagan con Yape/Tarjeta, forzamos estos valores a 0
            self.monto_entregado = 0.0
            self.vuelto = 0.0
            
        return self