from sqlmodel import Session
from typing import List, Optional
from models.tipoObra_model import TipoObraModel
from repositories import tipoObra_repo

class TipoObraService:
    def __init__(self, session: Session):
        self.session = session

    def listar_tipoObras(self) -> List[TipoObraModel]:
        return tipoObra_repo.get_all(self.session)  

    def obtener_tipoExpediente_por_id(self, id: int) -> Optional[TipoObraModel]:
        return tipoObra_repo.get_by_id(self.session, id)

    def crear_tipoExpediente(self, nuevoTipoObra: TipoObraModel) -> TipoObraModel:
        return tipoObra_repo.create(self.session, nuevoTipoObra)

    def actualizar_tipoObra(self, updateTipoObra: TipoObraModel) -> Optional[TipoObraModel]:
        tipoObra = tipoObra_repo.get_by_id(self.session, updateTipoObra.idTipoObra)
        if not tipoObra:
            return None
        tipoObra.nombre = updateTipoObra.nombre
        tipoObra.descripcion = updateTipoObra.descripcion
        return tipoObra_repo.update(self.session, tipoObra)

    def eliminar_tipoObra(self, id: int) -> bool:
        tipoObra = tipoObra_repo.get_by_id(self.session, id)
        if not tipoObra:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idTipoExpediente == idTipoExpediente)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        tipoObra_repo.delete(self.session, tipoObra)
        return True