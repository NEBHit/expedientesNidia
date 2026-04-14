from sqlmodel import Session, select
from models.profesional_model import ProfesionalModel
from typing import List, Optional
from sqlalchemy.orm import selectinload


def get_all(session: Session) -> List[ProfesionalModel]:
    return session.exec(select(ProfesionalModel)
                                .options(selectinload(ProfesionalModel.tipoProfesion))  # ✅ esta es la relación
                                .order_by(ProfesionalModel.apellido)).all()

def get_by_all_id(session: Session, ids_profesionales: List[int]) -> List[ProfesionalModel]:
    return session.exec(
             select(ProfesionalModel).where(ProfesionalModel.idProfesional.in_(ids_profesionales))
           ).all()

def get_by_id(session: Session, id: int) -> Optional[ProfesionalModel]:
    return session.get(ProfesionalModel, id)

def create(session: Session, profesional: ProfesionalModel) -> ProfesionalModel:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def update(session: Session, profesional: ProfesionalModel) -> ProfesionalModel:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def delete(session: Session, profesional: ProfesionalModel):
    session.delete(profesional)
    session.commit()

def get_by_idTipoProfesion(session: Session, id: int) ->  ProfesionalModel:
    return session.exec(select(ProfesionalModel).where(ProfesionalModel.idTipoProfesion == id)).first()

def get_by_cuit(session: Session, id:int, cuil: str) -> List[ProfesionalModel]:
    return session.exec(select(ProfesionalModel).where(ProfesionalModel.idProfesional != id, ProfesionalModel.cuil_cuit == cuil)).all()

                               