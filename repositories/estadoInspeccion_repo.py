from sqlmodel import Session, select
from models.estadoInspeccion_model import EstadoInspeccionModel
from typing import List, Optional

def get_all(session: Session) -> List[EstadoInspeccionModel]:
    return session.exec(select(EstadoInspeccionModel).order_by(EstadoInspeccionModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[EstadoInspeccionModel]:
    return session.get(EstadoInspeccionModel, id)

def create(session: Session, estado: EstadoInspeccionModel) -> EstadoInspeccionModel:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def update(session: Session, estado: EstadoInspeccionModel) -> EstadoInspeccionModel:
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado

def delete(session: Session, estado: EstadoInspeccionModel):
    session.delete(estado)
    session.commit()