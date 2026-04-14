from sqlmodel import Session
from typing import List, Optional
from models.tipoPago_model import TipoPagoModel
from repositories import tipoPago_repo

class TipoPagoService:
    def __init__(self, session: Session):
        self.session = session

    def listar_TipoPagos(self) -> List[TipoPagoModel]:
        return tipoPago_repo.get_all(self.session)  

    def obtener_tipoExpediente_por_id(self, id: int) -> Optional[TipoPagoModel]:
        return tipoPago_repo.get_by_id(self.session, id)

    def crear_tipoExpediente(self, nuevoTipoPago: TipoPagoModel) -> TipoPagoModel:
        return tipoPago_repo.create(self.session, nuevoTipoPago)

    def actualizar_TipoPago(self, updateTipoPago: TipoPagoModel) -> Optional[TipoPagoModel]:
        tipoPago = tipoPago_repo.get_by_id(self.session, updateTipoPago.idTipoPago)
        if not tipoPago:
            return None
        tipoPago.nombre = updateTipoPago.nombre
        tipoPago.descripcion = updateTipoPago.descripcion
        return tipoPago_repo.update(self.session, tipoPago)

    def eliminar_TipoPago(self, id: int) -> bool:
        tipoPago = tipoPago_repo.get_by_id(self.session, id)
        if not tipoPago:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idTipoExpediente == idTipoExpediente)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        tipoPago_repo.delete(self.session, tipoPago)
        return True