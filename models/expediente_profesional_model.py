#Relacion N a N entre Expedeinte y Profesional. 
#Esta relacion Guarda los profesionales asignados al Expediente
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from models.expediente_model import ExpedienteModel
    from models.profesional_model import ProfesionalModel

class Expediente_ProfesionalModel(SQLModel, table=True):
    __tablename__ = "Expediente_Profesional"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idProfesional: int = Field(foreign_key="Profesional.idProfesional", primary_key=True)
    contactoPpal: int | None = Field(default=1, nullable=True) 
    
    fechaIngresoSistema: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )

    # Relaciones con back_populates. Relacion N a N
    # Forward references (clases referenciadas como string)
    expediente: Optional["ExpedienteModel"] = Relationship(back_populates="profesionales")
    profesional: Optional["ProfesionalModel"] = Relationship(back_populates="expedientes")
    
    class Config:
        from_attributes = True
    
   