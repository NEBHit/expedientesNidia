#Relacion N a N entre Expedeinte y Tipo Obra. 
#Esta relacion Guarda los distintos tipos de obra por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.expediente_model import ExpedienteModel
    from models.tipoObra_model import TipoObraModel

class Expediente_TipoObraModel(SQLModel, table=True):
    __tablename__ = "Expediente_TipoObra"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idTipoObra: int = Field(foreign_key="TipoObra.idTipoObra", primary_key=True)

    fechaAsignacion: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="tipos")
    tipos: Optional["TipoObraModel"] = Relationship(back_populates="expedientes")
    
    class Config:
        from_attributes = True   