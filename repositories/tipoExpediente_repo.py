from sqlmodel import Session, select
from models.tipoExpediente_model import TipoExpedienteModel
from typing import List, Optional

def get_all(session: Session) -> List[TipoExpedienteModel]:
    return session.exec(select(TipoExpedienteModel).order_by(TipoExpedienteModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoExpedienteModel]:
    return session.get(TipoExpedienteModel, id)

def create(session: Session, tipo: TipoExpedienteModel) -> TipoExpedienteModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoExpedienteModel) -> TipoExpedienteModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoExpedienteModel):
    session.delete(tipo)
    session.commit()