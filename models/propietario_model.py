from sqlmodel import SQLModel, Field #, Relationship
from datetime import datetime
from sqlalchemy import Column, DateTime, func

class PropietarioModel(SQLModel, table=True):
    __tablename__ = "Propietario"
    
    idPropietario: int | None = Field(default=None, primary_key=True)
    cuil_cuit: str 
    nombre: str 
    apellido: str 
    calle: str | None = Field(default=None, nullable=True)
    nroCalle: int | None = Field(default=None, nullable=True) 
    nroDpto: str | None = Field(default=None, nullable=True)
    piso: str | None = Field(default=None, nullable=True)
    areaCelular: int | None = Field(default=None, nullable=True) 
    nroCelular: int | None = Field(default=None, nullable=True)
    email: str | None = Field(default=None, nullable=True)
    idUsuarioCrear: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    fechaIngresoSistema: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
         
    class Config:
      from_attributes = True