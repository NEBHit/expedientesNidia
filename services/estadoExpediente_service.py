from sqlmodel import Session
from typing import List, Optional
from models.estadoExpediente_model import EstadoExpedienteModel
from repositories import estadoExpediente_repo

class EstadoExpedienteService:
    def __init__(self, session: Session):
        self.session = session

    def listar_estados(self) -> List[EstadoExpedienteModel]:
        return estadoExpediente_repo.get_all(self.session)  

    def obtener__estado_por_id(self, id: int) -> Optional[EstadoExpedienteModel]:
        return estadoExpediente_repo.get_by_id(self.session, id)

    def crear_estado(self, nuevoEstado: EstadoExpedienteModel) -> EstadoExpedienteModel:
        return estadoExpediente_repo.create(self.session, nuevoEstado)

    def actualizar_estado(self, updateEstado: EstadoExpedienteModel) -> Optional[EstadoExpedienteModel]:
        estado = estadoExpediente_repo.get_by_id(self.session, updateEstado.idEstadoExpediente)
        if not estado:
            return None
        estado.nombre = updateEstado.nombre
        estado.descripcion = updateEstado.descripcion
        return estadoExpediente_repo.update(self.session, estado)

    def eliminar_estado(self, id: int) -> bool:
        estado = estadoExpediente_repo.get_by_id(self.session, id)
        if not estado:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idEstadoExpediente == idEstadoExpediente)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        estadoExpediente_repo.delete(self.session, estado)
        return True