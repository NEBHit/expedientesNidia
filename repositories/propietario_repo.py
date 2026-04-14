from sqlmodel import Session, select
from models.propietario_model import PropietarioModel
from typing import List, Optional
from sqlalchemy.orm import selectinload

def get_all(session: Session) -> List[PropietarioModel]:
    return session.exec(select(PropietarioModel)
                                .options(selectinload(PropietarioModel.tipoProfesion))  # ✅ esta es la relación
                                .order_by(PropietarioModel.apellido)).all()

def get_by_id(session: Session, id: int) -> Optional[PropietarioModel]:
    return session.get(PropietarioModel, id)

def get_by_all_id(session: Session, ids_propietarios: List[int]) -> List[PropietarioModel]:
    return session.exec(
             select(PropietarioModel).where(PropietarioModel.idPropietario.in_(ids_propietarios))
           ).all()

def create(session: Session, profesional: PropietarioModel) -> PropietarioModel:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def update(session: Session, profesional: PropietarioModel) -> PropietarioModel:
    session.add(profesional)
    session.commit()
    session.refresh(profesional)
    return profesional

def delete(session: Session, profesional: PropietarioModel):
    session.delete(profesional)
    session.commit()

def get_by_cuit_distintApellido(session: Session, apellido : str, cuil: str) -> List[PropietarioModel]:
    return session.exec(select(PropietarioModel).where(PropietarioModel.apellido != apellido, PropietarioModel.cuil_cuit == cuil)).all()

def get_by_cuit(session: Session, cuil: str) -> PropietarioModel:
    return session.exec(select(PropietarioModel).where(PropietarioModel.cuil_cuit == cuil)).first()
                               