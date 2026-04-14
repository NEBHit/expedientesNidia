from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Column, DateTime, func

if TYPE_CHECKING:
    from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
    from models.usuario_model import UsuarioModel

class EstadoExpedienteModel(SQLModel, table=True):
    __tablename__ = "EstadoExpediente"
    
    idEstadoExpediente: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    descripcion: str | None = Field(default=None, nullable=True)

    idUsuarioCrear: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    fechaIngresoSistema: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    
    #relacion N a N
    expedientes: List["Expediente_EstadoExpedienteModel"] = Relationship(back_populates="estado")

  