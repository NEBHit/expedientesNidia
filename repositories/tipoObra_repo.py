from sqlmodel import Session, select
from models.tipoObra_model import TipoObraModel
from typing import List, Optional

def get_all(session: Session) -> List[TipoObraModel]:
    return session.exec(select(TipoObraModel).order_by(TipoObraModel.nombre)).all()

def get_by_id(session: Session, id: int) -> Optional[TipoObraModel]:
    return session.get(TipoObraModel, id)

def create(session: Session, tipo: TipoObraModel) -> TipoObraModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def update(session: Session, tipo: TipoObraModel) -> TipoObraModel:
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    return tipo

def delete(session: Session, tipo: TipoObraModel):
    session.delete(tipo)
    session.commit()