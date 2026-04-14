from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func, Date
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, date


if TYPE_CHECKING:
     from models.tipoExpediente_model import TipoExpedienteModel
     from models.expediente_tipoObra_model import Expediente_TipoObraModel
     from models.tipoPago_model import TipoPagoModel
     from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
     from models.expediente_profesional_model import Expediente_ProfesionalModel
    
     
class ExpedienteModel(SQLModel, table=True):
    __tablename__ = "Expediente"
    
    idExpediente: int | None = Field(default=None, primary_key=True)
    idTipoExpediente: int | None = Field(..., foreign_key="TipoExpediente.idTipoExpediente")
     #El nro de expediente se forma con el nroEntrada + el anioMesa de Entrada
    nroLegajo: int # 3 digitos, se reinicia con cada año 
    nroExpediente: int #Se reinicia con cada año 
    anioExpediente: int #año en el que el expedeinte se crea = anioActual
    anioMesaEntrada: int 
    nroExpedienteMesaEntrada: str | None = Field(default=None, nullable=True)
    nroPartida: str | None = Field(default=None, nullable=True)
    catastroRafam: str | None = Field(default=None, nullable=True)
    sucesion: int | None = Field(default=None, nullable=True)
    observaciones: str | None = Field(default=None, nullable=True)

    idUsuarioCrear: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    idUsuarioModificar: int = Field(default=None, foreign_key="Usuario.idUsuario", nullable=False)
    
    fechaIngresoSistema: datetime = Field(sa_column=Column(DateTime, server_default=func.now()))
    fechaUltimaMod: datetime = Field(sa_column=Column(DateTime, server_default=func.now(), onupdate=func.now()))
   
    #Relacion 1 a N con TipoPago
    idTipoPago: int | None = Field(default=None, foreign_key="TipoPago.idTipoPago")
    tipoPago: Optional["TipoPagoModel"] = Relationship(back_populates="expedientes")

    fechaPagoContado: date | None = Field(
        default=None,
        sa_column=Column(Date, nullable=True)
    )

    cantCuotas: int | None = Field(default=None)
    
    fechaPagoPrimerCta: date | None = Field(
        default=None,
        sa_column=Column(Date, nullable=True)
    )

    fechaPagoUltimaCta: date | None = Field(
        default=None,
        sa_column=Column(Date, nullable=True)
    )

    #Realcion 1 a N (Con TipoExpediente)
    tipoExpediente: Optional["TipoExpedienteModel"] = Relationship(back_populates="expedientes")
    # Relación N a N (tabla intermedia Expediente_TipoObra)
    tipos: List["Expediente_TipoObraModel"] = Relationship(back_populates="expediente")
    # Relación N a N (tabla intermedia Expediente_EstadoExpediente)
    estados: List["Expediente_EstadoExpedienteModel"] = Relationship(back_populates="expediente")
    # Relación N a N (tabla intermedia Expediente_Profesional)
    profesionales: List["Expediente_ProfesionalModel"] = Relationship(back_populates="expediente")
   
    class Config:
        from_attributes = True       
       
