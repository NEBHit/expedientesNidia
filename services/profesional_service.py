from sqlmodel import Session
from typing import List, Optional
from models.profesional_model import ProfesionalModel
from repositories import profesional_repo

class ProfesionalService:
    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    def __init__(self, session: Session):
        self.session = session

    def listar_profesionales(self) -> List[ProfesionalModel]:
        return profesional_repo.get_all(self.session)  

    def obtener_profesional_por_id(self, id: int) -> Optional[ProfesionalModel]:
        return profesional_repo.get_by_id(self.session, id)

    def crear_profesional(self, nuevoProfesional: ProfesionalModel) -> ProfesionalModel:
        return profesional_repo.create(self.session, nuevoProfesional)
    
    def actualizar_profesional(self, updateProfesional: ProfesionalModel) -> Optional[ProfesionalModel]:

        profesional = profesional_repo.get_by_id(self.session, updateProfesional.idProfesional)
        if not profesional:
            print ("error:" + "noExiste" )
            return "noExiste"
        
         # Validar que el cuil_cuit no esté repetido en otro profesional
        profesionales_repetidos = profesional_repo.get_by_cuit(
            self.session,
            updateProfesional.idProfesional,
            updateProfesional.cuil_cuit
        )
        if profesionales_repetidos:
            print ("error:" + "cuilRepetido" )
            return "cuilRepetido"
      
        # Actualizar campos manualmente
        profesional.nombre = updateProfesional.nombre
        profesional.apellido = updateProfesional.apellido
        profesional.razonSocial = updateProfesional.razonSocial
        profesional.cuil_cuit = updateProfesional.cuil_cuit
        profesional.calle = updateProfesional.calle
        profesional.nroCalle = updateProfesional.nroCalle
        profesional.nroDpto = updateProfesional.nroDpto
        profesional.piso = updateProfesional.piso
        profesional.areaCelular = updateProfesional.areaCelular
        profesional.nroCelular = updateProfesional.nroCelular
        profesional.matricula = updateProfesional.matricula
        profesional.email = updateProfesional.email
        profesional.idTipoProfesion = updateProfesional.idTipoProfesion

        return profesional_repo.update(self.session, profesional)        
  
            
    def eliminar_profesional(self, id: int) -> bool:
        profesional = profesional_repo.get_by_id(self.session, id)
        if not profesional:
            return False
        
        # Verificar si hay Expedientes que usen este Estado
        #expedientes = session.exec(
        #    select(Expediente).where(Expediente.idInspector == idInspector)
        #).all()

        #if expedientes:
        #    return {
        #        "error": "No se puede eliminar el Estado de Expediente porque está asociado a uno o más expedientes."
        #    }

        profesional_repo.delete(self.session, profesional)
        return True