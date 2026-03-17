from sqlmodel import Session, select
from models.estadoExpediente_model import EstadoExpedienteModel
from typing import List, Optional

def get_all(session: Session) -> List[EstadoExpedienteModel]:
    return session.exec(select(EstadoExpedienteModel).order_by(EstadoExpedienteModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[EstadoExpedienteModel]:
    return session.get(EstadoExpedienteModel, id)

def create(session: Session, estado: EstadoExpedienteModel) -> EstadoExpedienteModel:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: EstadoExpedienteModel) -> EstadoExpedienteModel:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: EstadoExpedienteModel):
    session.delete(estado)
    session.commit()