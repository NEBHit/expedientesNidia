#Relacion N a N entre Expedeinte y Tipo pago. 
#Esta relacion Guarda los distintos tipos de obra por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.expediente_model import ExpedienteModel
    from models.tipoPago_model import TipoPagoModel

class Expediente_TipoPagoModel(SQLModel, table=True):
    __tablename__ = "Expediente_TipoPago"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idTipoPago: int = Field(foreign_key="TipoPago.idTipoPago", primary_key=True)

    fechaPago: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    cantCuotas: int
    pagoPrimeraCuota: int 
    pagoUltimaCuota: int

    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
    #expediente: Optional["ExpedienteModel"] = Relationship(back_populates="tipospagos")
    #tipospagos: Optional["TipoPagoModel"] = Relationship(back_populates="expedientes")

    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="tipospagos")
    tipopago: Optional["TipoPagoModel"] = Relationship(back_populates="expedientes")
    
    
   