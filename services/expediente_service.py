from sqlmodel import Session
from typing import List, Optional

from models.expediente_model import ExpedienteModel

from repositories import expediente_repo, propietario_repo

class ExpedienteService:
    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    def obtener_proximo_nro_legajo(self, anioMesaEntrada: int) -> int:
        return expediente_repo.get_next_nro_legajo(self.session, anioMesaEntrada)
    
    def obtener_proximo_nro_expediente(self, anio: int) -> int:
        return expediente_repo.get_next_nro_expediente(self.session, anio)
    
    def __init__(self, session: Session):
        self.session = session

    def listar_expedientes(self) -> List[ExpedienteModel]:

        expedientes=expediente_repo.get_all(self.session)

        # Extraer el último estado asignado por expediente y generar un nuevo objeto expedientes con los datos extraidos de expediente 
        # agregados el id del ultimo estado y la fecha de la ultima modficacion del estado para mostrar en al tabla, ya que es una relacion n a n
        expedientes_con_estado = []
        for exp in expedientes:
            ultimo_estado_id = None
            ultimo_estado_nombre = "Sin estado"

            for e in exp.estados:
                
                print(e.idRelacion, e.fechaCambioEstado, e.idEstadoExpediente)
          
            if exp.estados:
                ultimo_rel = max(
                    exp.estados,
                    key=lambda e: e.fechaCambioEstado
                )

                ultimo_estado_id = ultimo_rel.idEstadoExpediente
                ultimo_estado_nombre = (
                    ultimo_rel.estado.nombre
                    if ultimo_rel.estado else "Sin estado"
                )

            tipos_obra_ids = [t.idTipoObra for t in exp.tipos] if exp.tipos else []
    
            expedientes_con_estado.append({
                "expediente": exp,
                "ultimo_estado_id": ultimo_estado_id,
                "ultimo_estado_nombre": ultimo_estado_nombre,
                "tiposObra": tipos_obra_ids
            })

        return  expedientes_con_estado

    def obtener_expediente_por_id(self, id: int) -> Optional[ExpedienteModel]:
        return expediente_repo.get_by_id(self.session, id)

    #Obtener propietarios del Expedeinte. relacion N a N
    def get_propietarios(self, idExpediente: int):
        return expediente_repo.get_propietarios(self.session,idExpediente)

    #Obtener profesionales del Expediente. relacion N a N
    def get_profesionales(self, idExpediente: int):
        return expediente_repo.get_profesionales(self.session,idExpediente)

    #Obtener estados del Expediente. relacion N a N
    def get_estados(self, idExpediente: int):
        return expediente_repo.get_estados(self.session,idExpediente)
    
    def crear_expediente(self, nuevoExpediente: ExpedienteModel, idEstadoExpediente: int, lista_tiposObras: list[dict], propietarios_data: list[dict], expedientesProfesionales_data: list[dict]) -> Optional[ExpedienteModel]:
        #Validar que no exista un propietario con el Cuil ingresado
        
        for p_dict in propietarios_data:
            p = p_dict["propietario"]
            propietario = propietario_repo.get_by_cuit_distintApellido(self.session, p.apellido, p.cuil_cuit)
            if propietario:
                return "duplicado/" +  p.cuil_cuit 
        
        return expediente_repo.create_expediente_completo(self.session,nuevoExpediente,idEstadoExpediente, lista_tiposObras, propietarios_data, expedientesProfesionales_data) 
       
    def actualizar_expediente(self, updateExpediente: ExpedienteModel, idEstadoExpediente:int, idEstadoExpNuevo:int,propietarios_data: list[dict],profesionales_data: list[dict]) -> Optional[ExpedienteModel]:
        
        expediente = expediente_repo.get_by_id(self.session, updateExpediente.idExpediente)
        
        if not expediente:
            return "noExiste"
        
        # Actualizar campos manualmente
        #expediente.idTipoObra = updateExpediente.idTipoObra
        expediente.nroExpedienteMesaEntrada = updateExpediente.nroExpedienteMesaEntrada
        expediente.anioMesaEntrada = updateExpediente.anioMesaEntrada
        expediente.nroPartida = updateExpediente.nroPartida
        expediente.sucesion = updateExpediente.sucesion
        expediente.observaciones = updateExpediente.observaciones
        expediente.idUsuarioModificar = updateExpediente.idUsuarioModificar
        expediente.fechaUltimaMod=updateExpediente.fechaUltimaMod

        return expediente_repo.update_expediente_con_relaciones(self.session, expediente, idEstadoExpediente, idEstadoExpNuevo,propietarios_data, profesionales_data)        
            
    def eliminar_expediente(self, id: int) -> bool:
        expediente = expediente_repo.get_by_id(self.session, id)
        if not expediente:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idInspector == idInspector)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        expediente_repo.delete(self.session, expediente)
        return True