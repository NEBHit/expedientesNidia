from sqlmodel import Session, select
from models.tipoProfesion_model import TipoProfesionModel
from typing import List, Optional

def get_all(session: Session) -> List[TipoProfesionModel]:
    return session.exec(select(TipoProfesionModel).order_by(TipoProfesionModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoProfesionModel]:
    return session.get(TipoProfesionModel, id)

def create(session: Session, tipo: TipoProfesionModel) -> TipoProfesionModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoProfesionModel) -> TipoProfesionModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoProfesionModel):
    session.delete(tipo)
    session.commit()