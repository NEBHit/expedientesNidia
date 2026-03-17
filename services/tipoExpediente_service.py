from sqlmodel import Session
from typing import List, Optional
from models.tipoExpediente_model import TipoExpedienteModel
from repositories import tipoExpediente_repo

class TipoExpedienteService:
    def __init__(self, session: Session):
        self.session = session

    def listar_tipoExpedientes(self) -> List[TipoExpedienteModel]:
        return tipoExpediente_repo.get_all(self.session)  

    def obtener_tipoExpediente_por_id(self, id: int) -> Optional[TipoExpedienteModel]:
        return tipoExpediente_repo.get_by_id(self.session, id)

    def crear_tipoExpediente(self, nuevoTipoExpediente: TipoExpedienteModel) -> TipoExpedienteModel:
        return tipoExpediente_repo.create(self.session, nuevoTipoExpediente)

    def actualizar_tipoExpediente(self, updateTipoExpediente: TipoExpedienteModel) -> Optional[TipoExpedienteModel]:
        tipoExpediente = tipoExpediente_repo.get_by_id(self.session, updateTipoExpediente.idTipoExpediente)
        if not tipoExpediente:
            return None
        tipoExpediente.nombre = updateTipoExpediente.nombre
        tipoExpediente.descripcion = updateTipoExpediente.descripcion
        return tipoExpediente_repo.update(self.session, tipoExpediente)

    def eliminar_tipoExpediente(self, id: int) -> bool:
        tipoExpediente = tipoExpediente_repo.get_by_id(self.session, id)
        if not tipoExpediente:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idTipoExpediente == idTipoExpediente)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        tipoExpediente_repo.delete(self.session, tipoExpediente)
        return True