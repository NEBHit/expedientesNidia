from sqlmodel import Session, select
from sqlalchemy import delete as sa_delete

from models.expediente_model import ExpedienteModel
from models.expediente_estadoExpediente_model import Expediente_EstadoExpedienteModel
from models.propietario_model import PropietarioModel
from models.expediente_propietario_model import Expediente_PropietarioModel
from models.expediente_profesional_model import Expediente_ProfesionalModel
from models.expediente_tipoObra_model import Expediente_TipoObraModel
from models.profesional_model import ProfesionalModel
from models.estadoExpediente_model import EstadoExpedienteModel
from models.usuario_model import UsuarioModel

from repositories import propietario_repo, profesional_repo

from typing import List, Optional
from sqlalchemy.orm import selectinload
from datetime import datetime
from sqlalchemy import func

#Funcion para generar el nro de legajo consecutivo por año del expediente
def get_next_nro_legajo(session: Session, anioMesaEntrada: int) -> int:
 
    max_nro = session.query(
        func.coalesce(func.max(ExpedienteModel.nroLegajo), 0)
    ).filter(
        ExpedienteModel.anioMesaEntrada == anioMesaEntrada
    ).scalar()
   
    print("====================================================")
    print(max_nro)
    print("====================================================")

    return max_nro + 1

#Funcion para generar el nro de expedeinte consecutivo por año actual
def get_next_nro_expediente(session: Session, anio: int) -> int:
    max_nro = session.query(
        func.coalesce(func.max(ExpedienteModel.nroExpediente), 0)
    ).filter(
        ExpedienteModel.anioExpediente == anio
    ).scalar()
   
    print("====================================================")
    print(max_nro)
    print("====================================================")

    return max_nro + 1
      
def get_all(session: Session) -> List[ExpedienteModel]:
    return session.exec(select(ExpedienteModel)
                                .options(
                                    # Cargar TipoExpediente
                                    selectinload(ExpedienteModel.tipoExpediente),

                                    #CARGAR Estados Expedientes
                                    selectinload(ExpedienteModel.estados)
                                        .selectinload(Expediente_EstadoExpedienteModel.estado),

                                    #Cargar Tipos de Obras
                                    selectinload(ExpedienteModel.tipos)
                                        .selectinload(Expediente_TipoObraModel.tipos)                                        

                                )
                                .order_by(ExpedienteModel.fechaIngresoSistema)
                                ).all()

def get_by_id(session: Session, id: int) -> Optional[ExpedienteModel]:
    return session.get(ExpedienteModel , id)

def get_propietarios(session: Session, idExpediente: int):
        # 1) Buscar relaciones en la tabla intermedia.
        #    Las relaciones N a N no tienen definido repositorios, por lo tanto se tira la consultan directamente
        stmt = (
        select(PropietarioModel, Expediente_PropietarioModel.figuraPpal)
        .join(Expediente_PropietarioModel,
              PropietarioModel.idPropietario == Expediente_PropietarioModel.idPropietario)
        .where(Expediente_PropietarioModel.idExpediente == idExpediente)
    )

        resultados = session.exec(stmt).all()

        lista = []
        print("RESULTADOS =============================================================")
        print(resultados)
        print("=============================================================")


        #Armo la lista con los valores concatenados del Profesional mas lo de la relacion
        for prop, figuraPpal in resultados:
            lista.append({
                "idPropietario": prop.idPropietario,
                "cuil_cuit": prop.cuil_cuit,
                "nombre": prop.nombre,
                "apellido": prop.apellido,
                "calle": prop.calle,
                "nroCalle": prop.nroCalle,
                "nroDpto": prop.nroDpto,
                "areaCelular": prop.areaCelular,
                "nroCelular": prop.nroCelular,
                "email": prop.email,
                "ppal": figuraPpal
            })
            print("=============================================================")
            print(figuraPpal)
            print(type(figuraPpal))
            print("=============================================================")
        
        print(lista)
        
        return lista


def get_profesionales(session: Session, idExpediente: int):
    # 1) Buscar relaciones en la tabla intermedia.
    #    Las relaciones N a N no tienen definido repositorios, por lo tanto se tira la consultan directamente
    
    stmt = (
        select(ProfesionalModel, Expediente_ProfesionalModel.contactoPpal)
        .join(Expediente_ProfesionalModel,
              ProfesionalModel.idProfesional == Expediente_ProfesionalModel.idProfesional)
        .where(Expediente_ProfesionalModel.idExpediente == idExpediente)
    )

    resultados = session.exec(stmt).all()

    lista = []
    
    #Armo la lista con los valores concatenados del Profesional mas lo de la relacion
    for prof, contactoPpal in resultados:
         lista.append({
            "idProfesional": prof.idProfesional,
            "nombre": prof.nombre,
            "apellido": prof.apellido,
            "matricula": prof.matricula,
            "contactoPpal": contactoPpal
        })

    return lista

def get_estados(session: Session, idExpediente: int):
    # 1) Buscar relaciones en la tabla intermedia.
    #    Las relaciones N a N no tienen definido repositorios, por lo tanto se tira la consultan directamente
 
    stmt = (
        select(
            EstadoExpedienteModel,
            UsuarioModel,
            Expediente_EstadoExpedienteModel.fechaCambioEstado
        )
        .join(
            Expediente_EstadoExpedienteModel,
            EstadoExpedienteModel.idEstadoExpediente
            == Expediente_EstadoExpedienteModel.idEstadoExpediente
        )
        .join(
            UsuarioModel,
            UsuarioModel.idUsuario
            == Expediente_EstadoExpedienteModel.idUsuario
        )
        .where(
            Expediente_EstadoExpedienteModel.idExpediente == idExpediente
        )
        .order_by(
            Expediente_EstadoExpedienteModel.fechaCambioEstado.desc()
        )
    )

    resultados = session.exec(stmt).all()

    lista = []
    
    #Armo la lista con los valores concatenados del Profesional mas lo de la relacion
    for estado, usuario, fecha in resultados:
        lista.append({
            "nombre": estado.nombre,
            "fecha": fecha.strftime('%Y-%m-%d %H:%M:%S'), #Formateo la fecha para que no me muestre la T en el dateTime
            "usuario": usuario.usuario
        })

    return lista

def create(session: Session, expediente : ExpedienteModel, idEstadoExpediente: int, propietarios : list[dict]) -> ExpedienteModel :
    #Crea un expediente sin propietarios y son profesionales
    session.add(expediente)
    session.flush()  # OBTENER el id sin hacer commit

    # Registrar el estado inicial en la tabla expediente_estadoexpediente
    nuevo_estado = Expediente_EstadoExpedienteModel(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente=idEstadoExpediente, 
        fechaCambioEstado= datetime.now()
    )

    session.add(nuevo_estado)
    session.commit()
    session.refresh(expediente)
    return expediente 


def create_expediente_completo(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int, lista_tiposObras: list, propietarios : list[dict], expedientesProfesionales : list[dict]) -> ExpedienteModel :
    #Crea un expedeinte completo, es decir, agrega las relaciones con estadoExpedeinte, propietariosExpedientes y ProfesionalesExpedientes
    session.add(expediente)
    session.flush()  # OBTENER el id sin hacer commit
    #session.commit()
    #session.refresh(expediente)
 
    # Registrar el estado inicial en la tabla expediente_estadoexpediente
    nuevo_estado = Expediente_EstadoExpedienteModel(
        idExpediente=expediente.idExpediente,
        idEstadoExpediente = idEstadoExpediente, 
        fechaCambioEstado= datetime.now(),
        idUsuario=expediente.idUsuarioCrear
    )
    session.add(nuevo_estado)

    # REGISTRAR TIPOS DE OBRA  (NUEVO)

    #print("====================================================================")
    #print("cantidadtipos obras: ", len(lista_tiposObras))
    for tipo in lista_tiposObras:
        nuevo_tipo = Expediente_TipoObraModel(
            idExpediente=expediente.idExpediente,
            idTipoObra=int(tipo),
            fechaAsignacion= datetime.now()
        )
        session.add(nuevo_tipo)

    #Crear propietarios y asociarlos a la tabla expediente_propietario
    for p_dict in propietarios:

        #print("__________________________________________________________")
        #print(propietarios)
        #print("__________________________________________________________")

        p = p_dict["propietario"]
        figuraPpal = p_dict["figuraPpal"]
        # Buscar si ya existe un propietario con ese CUIL. sI EXISTE SOLO SE ACTUALIZAN LOS DATOS. A ESTA ALTURA SE VERIFICO QUE EL APELLIDO COINCIDE.
        cuil = p.cuil_cuit
        existing_propietario = session.exec(select(PropietarioModel).where(PropietarioModel.cuil_cuit == cuil)).first()

        if existing_propietario is None:
            #Registrar nuevo Propietario
            nuevo_propietario = PropietarioModel(
                cuil_cuit=p.cuil_cuit,
                nombre=p.nombre,
                apellido=p.apellido,
                calle=p.calle,
                nroCalle=p.nroCalle,
                piso=p.piso,
                nroDpto=p.nroDpto,
                areaCelular=p.areaCelular,
                nroCelular=p.nroCelular,
                email=p.email,
                idUsuarioCrear=expediente.idUsuarioCrear
            )
            session.add(nuevo_propietario)
            session.flush()  # OBTENER el id sin hacer commit
        #    session.commit()
        #    session.refresh(nuevo_propietario)
            prop_id = nuevo_propietario.idPropietario
        else: 
           # Actualizar propietario existente
            existing_propietario.nombre = p.nombre
            existing_propietario.calle = p.calle
            existing_propietario.nroCalle = p.nroCalle
            existing_propietario.piso = p.piso
            existing_propietario.nroDpto = p.nroDpto
            existing_propietario.areaCelular = p.areaCelular 
            existing_propietario.nroCelular = p.nroCelular 
            existing_propietario.email = p.email
            
            #session.commit()
            #session.refresh(existing_propietario)
            prop_id = existing_propietario.idPropietario       
            
        #Registar la relacion Expediente_Propietario
        nuevo_ExpProp = Expediente_PropietarioModel(
            idExpediente=expediente.idExpediente,
            idPropietario=prop_id,
            figuraPpal=figuraPpal,
            fechaCambioPropietario= datetime.now()
        )
    
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProp)

    #Crear relacion expediente_profesional
    for p in expedientesProfesionales:
        #Registar la relacion Expediente_Profesional
        nuevo_ExpProf = Expediente_ProfesionalModel(
            idExpediente=expediente.idExpediente,
            idProfesional=p.idProfesional,
            contactoPpal=p.contactoPpal,
            fechaIngresoSistema= datetime.now()
        )
        
        # Asociar propietarios al expediente (relación N a N)
        session.add(nuevo_ExpProf)
                
    session.commit()
    
    return "exito" 

#-----------------------------------------------------------------------------------------------------
#Actualiza solamente el expediente y el estado. No se tiene en cuenta las tablas relacionadas
# ---------------------------------------------------------------------------------------------------- 
def update(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int) -> ExpedienteModel:
    session.add(expediente )
    #session.commit()

    #Actualizar la relacion Expediente_estadoExpediente si cambio el estado del expediente
    if idEstadoExpediente is not None: 
        # Registrar el estado inicial en la tabla expediente_estadoexpediente
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpediente,  
            fechaCambioEstado= datetime.now(),
            idUsuario=expediente.idUsuarioModificar
        )

        session.add(nuevo_estado)
    
    session.commit()
    session.refresh(expediente )
    return expediente 

def update_expediente_con_relaciones(session: Session, expediente : ExpedienteModel, idEstadoExpediente:int,idEstadoExpedienteNuevo:int, propietarios : list[dict], profesionales : list[dict]) -> ExpedienteModel:
    session.add(expediente)
    #session.commit()

    # 1) Registrar el estado en la tabla expediente_estadoexpediente si es que se modifico
    if idEstadoExpediente != idEstadoExpedienteNuevo:
        nuevo_estado = Expediente_EstadoExpedienteModel(
            idExpediente=expediente.idExpediente,
            idEstadoExpediente=idEstadoExpedienteNuevo, 
            fechaCambioEstado= datetime.now(),
            idUsuario=expediente.idUsuarioModificar
        )
        session.add(nuevo_estado)
   
    '''print("CANT PROPIETARIOS==============================================================")
    print("Cantidad de propietarios router:!!!!!!!!", len(propietarios))
    print(propietarios)
    print("==============================================================")
    '''
    # 2) Crear o modificar propietarios 
    # Cada propietario leido es de la forma {PropietarioModel, figuraPpal}, por lo tanto, 
    # el primer parametro es un objeto ORM (PropietarioModel)
    # el segundo es un int
    # se deben acceder de forma distintas! 
    for p in propietarios:

        ''' print("PROPIETARIO==============================================================")
        print(p)
        print("==============================================================")
        '''

        prop = p["propietario"]

        # Buscar si ya existe un propietario con ese CUIL. 
        # SI EXISTE SOLO SE ACTUALIZAN LOS DATOS. A ESTA ALTURA SE VERIFICO QUE EL APELLIDO COINCIDE en el front.
        cuil = prop.cuil_cuit
        existing_propietario = propietario_repo.get_by_cuit(session,cuil)

        if existing_propietario is None:
            #Registrar nuevo Propietario
            nuevo_propietario = PropietarioModel(
                cuil_cuit=prop.cuil_cuit,
                nombre=prop.nombre,
                apellido=prop.apellido,
                calle=prop.calle,
                nroCalle=prop.nroCalle,
                piso=prop.piso,
                nroDpto=prop.nroDpto,
                areaCelular=prop.areaCelular,
                nroCelular=prop.nroCelular,
                email=prop.email
            )
            session.add(nuevo_propietario)
            #session.commit()
            #session.refresh(nuevo_propietario)
            session.flush()  # OBTENER el id sin hacer commit
            prop_id = nuevo_propietario.idPropietario

            # 3) Registrar la relacion Expediente_Propietario
            nuevo_ExpProp = Expediente_PropietarioModel(
                idExpediente=expediente.idExpediente,
                idPropietario=prop_id,
                figuraPpal=p["figuraPpal"],
                fechaCambioPropietario= datetime.now()
            )
            session.add(nuevo_ExpProp)
        else: 
            # Actualizar propietario existente
            existing_propietario.nombre = prop.nombre
            existing_propietario.calle = prop.calle
            existing_propietario.nroCalle = prop.nroCalle
            existing_propietario.piso = prop.piso
            existing_propietario.nroDpto = prop.nroDpto
            existing_propietario.areaCelular = prop.areaCelular 
            existing_propietario.nroCelular = prop.nroCelular 
            existing_propietario.email = prop.email
            
            #session.commit()
            #session.refresh(existing_propietario)
            
            prop_id = existing_propietario.idPropietario       

            # 3)En esta instancia puede pasar que:
            #   3.a. el propietario ya fue relacionado con el expediente, en tal caso no se hace nada
            #   3.b. el propietario no esta relacionado y debe relacionarse
            
        #Consulto si esta relacionado o no. Como es una relacion N a N no se tiene repositorio y se ejecuta la consulta directamente
        expedientesPropietarios = session.exec(
            select(Expediente_PropietarioModel).where((Expediente_PropietarioModel.idPropietario == prop_id) and (Expediente_PropietarioModel.idExpediente == expediente.idExpediente))
        ).all()

        if not expedientesPropietarios:
            # 3.b.el propietario no esta relacionado y debe relacionarse.
            # Registar la relacion Expediente_Propietario
            nuevo_ExpProp = Expediente_PropietarioModel(
                idExpediente=expediente.idExpediente,
                idPropietario=prop_id,
                figuraPpal = p["figuraPpal"],
                fechaCambioPropietario= datetime.now()
            )

            #print("PROPIETARIO figura==============================================================")
            #print(p["figuraPpal"])
            #print("==============================================================")
        
            # Asociar propietarios al expediente (relación N a N)
            session.add(nuevo_ExpProp)
    session.flush()
    # 3) Crear relacion expediente_profesional 
    # 3.1 Eliminar todas las relaciones para ese expediente y agregar sola las relaciones activas en esta instancia 
    session.execute(
        sa_delete(Expediente_ProfesionalModel).where(Expediente_ProfesionalModel.idExpediente == expediente.idExpediente)
    )

    # 3.2 Para cada profesional de la lista creo la relacion 
    for p in profesionales:
        expediente_profesional = Expediente_ProfesionalModel(
            idExpediente = expediente.idExpediente,
            idProfesional = p["idProfesional"],
            contactoPpal = p["contactoPpal"],
            fechaIngresoSistema= datetime.now()
        )
        # Asociar propietarios al expediente (relación N a N)
        session.add(expediente_profesional)
                 
    session.commit()
    session.refresh(expediente)

    return "exito" 

def delete(session: Session, expediente : ExpedienteModel):  #creeria que no se puede eliminar un expedeinte ingresado o bien ver cuando!!!!! En proceso de analisis
    #session.delete(expediente )
    #session.commit()

    return expediente
         