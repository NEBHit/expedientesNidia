from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import Column, DateTime, func

class InspectorModel(SQLModel, table=True):
    __tablename__ = "Inspector"
    
    idInspector: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, nullable=False)
    apellido: str | None = Field(default=None, nullable=True)

    idUsuarioCrear: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    fechaIngresoSistema: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))

    class Config:
        from_attributes = True    