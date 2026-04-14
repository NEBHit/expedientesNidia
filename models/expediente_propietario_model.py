#Relacion N a N entre Expedeinte y Esatdo Expediente. 
#Esta relacion Guarda los distintos estados por los que pasa el Expediente y registra las fecha
from sqlmodel import SQLModel, Field #, Relationship
from sqlalchemy import Column, DateTime, func
from datetime import datetime

class Expediente_PropietarioModel(SQLModel, table=True):
    __tablename__ = "Expediente_Propietario"
    
    idExpediente: int = Field(foreign_key="Expediente.idExpediente", primary_key=True)
    idPropietario: int = Field(foreign_key="Propietario.idPropietario", primary_key=True)
    figuraPpal: int | None = Field(default=1, nullable=True) 

    fechaCambioPropietario: datetime = Field(
        sa_column=Column(DateTime, server_default=func.now())
    )



