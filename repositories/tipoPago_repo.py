from sqlmodel import Session, select
from models.tipoPago_model import  TipoPagoModel
from typing import List, Optional

def get_all(session: Session) -> List[TipoPagoModel]:
    return session.exec(select(TipoPagoModel).order_by(TipoPagoModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoPagoModel]:
    return session.get(TipoPagoModel, id)

def create(session: Session, tipo: TipoPagoModel) -> TipoPagoModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoPagoModel) -> TipoPagoModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoPagoModel):
    session.delete(tipo)
    session.commit()