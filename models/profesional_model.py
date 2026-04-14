from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, func

from models.tipoProfesion_model import TipoProfesionModel
from models.expediente_profesional_model import Expediente_ProfesionalModel

if TYPE_CHECKING:
    from models.expediente_profesional_model import Expediente_ProfesionalModel
 

class ProfesionalModel(SQLModel, table=True):
    __tablename__ = "Profesional"
    
    idProfesional: int | None = Field(default=None, primary_key=True)
    cuil_cuit: str 
    nombre: str 
    apellido: str 
    razonSocial: str | None = Field(default=None, nullable=True) 
    calle: str | None = Field(default=None, nullable=True)
    nroCalle: int | None = Field(default=None, nullable=True) 
    nroDpto: str | None = Field(default=None, nullable=True)
    piso: str | None = Field(default=None, nullable=True)
    areaCelular: int | None = Field(default=None, nullable=True) 
    nroCelular: int | None = Field(default=None, nullable=True)
    matricula: str | None = Field(default=None, nullable=True)
    email: str | None = Field(default=None, nullable=True)
    
    idTipoProfesion: int | None = Field(default=None, foreign_key="TipoProfesion.idTipoProfesion")

    idUsuarioCrear: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    fechaIngresoSistema: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))

    # Relación con TipoProfesion
    tipoProfesion: Optional[TipoProfesionModel] = Relationship()
    #relacion N a N
    expedientes: List["Expediente_ProfesionalModel"] = Relationship(back_populates="profesional")

    class Config:
        from_attributes = True   