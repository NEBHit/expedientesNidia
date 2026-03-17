from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List,Optional
from sqlmodel import Session
from fastapi.responses import JSONResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from datetime import datetime, date
from fastapi import HTTPException, status

import json

from models.expediente_model import ExpedienteModel
from models.profesional_model import ProfesionalModel
from models.expediente_profesional_model import Expediente_ProfesionalModel
from models.propietario_model import PropietarioModel

from services.expediente_service import ExpedienteService
from services.profesional_service import ProfesionalService
from services.tipoObra_service import TipoObraService
from services.tipoPago_service import TipoPagoService
from services.estadoExpediente_service import EstadoExpedienteService
from services.tipoExpediente_service import TipoExpedienteService 

from utils.mail import enviar_mail 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# -------------------------------
# LISTAR EXPEDIENTES
# -------------------------------
@router.get("/expedientes", response_model=List[ExpedienteModel])
async def get_expedientes(request: Request, session: Session = Depends(get_session)):

    service = ExpedienteService(session)  # instanciás la clase
    expedientes = service.listar_expedientes()  #  usás el método de instancia

    service = TipoExpedienteService(session)  #  instanciás la clase
    tiposExpedientes = service.listar_tipoExpedientes()  #  usás el método de instancia

    service = TipoObraService(session)  #  instanciás la clase
    tipoObras = service.listar_tipoObras()  #  usás el método de instancia

    service = TipoPagoService(session)  #  instanciás la clase
    tipoPagos = service.listar_TipoPagos()  #  usás el método de instancia

    service = ProfesionalService(session)  #  instanciás la clase
    profesionales = service.listar_profesionales()  #  usás el método de instancia

    service = EstadoExpedienteService(session)  #  instanciás la clase
    estadosExpedientes = service.listar_estados()  # usás el método de instancia

    return templates.TemplateResponse("listar_expedientes.html", { 
        "request": request,
        "expedientes": expedientes,
        "tiposExpedientes": tiposExpedientes,
        "tiposObras": tipoObras,
        "tiposPagos": tipoPagos,
        "profesionales": profesionales,
        "estadosExpedientes": estadosExpedientes
    })

# -------------------------------
# AGREGAR EXPEDIENTE (GET)
# -------------------------------
@router.get("/agregar_expediente", response_model=ExpedienteModel)
async def agregar_expediente_get(request: Request, session: Session = Depends(get_session)):
     return templates.TemplateResponse("agregar_expediente.html",{"request":request})

# -------------------------------
# AGREGAR EXPEDIENTE (POST)
# -------------------------------     

@router.post("/agregar_expediente", response_model=ExpedienteModel)
async def agregar_expediente_post(
     
    request: Request,
    idTipoExpediente : int =  Form(...),
    anioMesaEntrada : int = Form(...),
    nroExpedienteMesaEntrada: str = Form(...),
    nroPartida : str = Form(...),
    sucesion : int = Form(...),
    idEstadoExpediente : int =  Form(...),
    idTipoPago : Optional[int] = Form(None),
    fechaPagoContado : Optional[date] = Form(None),
    cantCuotas: Optional[int] = Form(None),
    fechaPagoPrimerCta: Optional[date] = Form(None),
    fechaPagoUltimaCta: Optional[date] = Form(None),
    observaciones: Optional[str] = Form(None),
    idFila : int = Form(...),  # cantPropietarios

    # JSON con los tipos de obra seleccionados
    idTipoObra: str = Form(...),

    session: Session = Depends(get_session)
    ):
    
        service = ExpedienteService(session)  # ✅ instanciás la clase
        anioMesaEntrada = int(anioMesaEntrada) if anioMesaEntrada else None
        #armar nro de entrada....debe ser consecutivos por año. 
        nroEntrada = service.obtener_proximo_nro_entrada(anioMesaEntrada)

        fechaUltimaMod = datetime.now()

        # Procesar Tipos de Obra (VIENEN COMO JSON STRING)
        try:
            lista_tiposObras = json.loads(idTipoObra)  # Ej: ["1","3","5"]
        except:
            raise HTTPException(status_code=400, detail="Error procesando idTipoObra")

        # Procesar propietarios
        valoresPropietarios = []
        for i in range(1, idFila + 1):  # recorre prop1...propN
            valor = (await request.form()).get(f"prop{i}", "").strip()
            # valor esperado: "cuil/apellido/nombre/figuraPpal/calle/nroCalle/piso/dpto/areaCel/nroCel/email"

            if valor:
                partes = valor.split("/")
                
                if len(partes) >= 11:

                    '''nro_calle_int = int(partes[5]) if partes[5] else None
                    area_celular_int = int(partes[8]) if  partes[8] else None
                    nro_celular_int = int(partes[9]) if partes[9] else None
                    figuraPpal_int = int(partes[3]) if partes[3] else 0
'''
                    nro_calle_int = int(partes[5]) if partes[5] not in (None, "", "null") else None
                    area_celular_int = int(partes[8]) if partes[8] not in (None, "", "null") else None
                    nro_celular_int = int(partes[9]) if partes[9] not in (None, "", "null") else None
                    figuraPpal_int = int(partes[3]) if partes[3] not in (None, "", "null") else 0

                    propietario = PropietarioModel(
                        cuil_cuit = partes[0],
                        apellido = partes[1],
                        nombre = partes[2],
                        figuraPpal = partes[3],
                        calle = partes[4],
                        nroCalle = nro_calle_int,# partes[5],
                        piso = partes[6],
                        nroDpto = partes[7],
                        areaCelular = area_celular_int, #partes[8],
                        nroCelular = nro_celular_int,#partes[9],
                        email = partes[10],
                        idUsuarioCrear=request.session["user_id"]
                    )
                    valoresPropietarios.append({
                        "propietario": propietario,
                        "figuraPpal": figuraPpal_int
                    })
             
        # Procesar profesionales
        valoresExpedientesProfesionales = []
        for i in range(1, idFila + 1):  # recorre prof1...profN
            valor = (await request.form()).get(f"prof{i}", "").strip()
            # valor esperado: "idProfesional/contactoPpal"

            if valor:
                partes = valor.split("/")
                if len(partes) >= 2:

                    expProfesional = Expediente_ProfesionalModel(
                        idProfesional = int(partes[0]) if partes[0] else None,
                        contactoPpal = partes[1],
                       # fechaIngresoSistema=datetime.now() 
                    )
                    valoresExpedientesProfesionales.append(expProfesional)

        nuevo_expediente = ExpedienteModel(
            idTipoExpediente=idTipoExpediente,
            nroEntrada=nroEntrada,
            anioMesaEntrada=anioMesaEntrada,
            nroExpedienteMesaEntrada=nroExpedienteMesaEntrada,
            nroPartida=nroPartida,
            sucesion=sucesion,
            idTipoPago=idTipoPago,
            fechaPagoContado=fechaPagoContado,
            cantCuotas=cantCuotas,
            fechaPagoPrimerCta=fechaPagoPrimerCta,
            fechaPagoUltimaCta=fechaPagoUltimaCta,
            observaciones=observaciones,
            idUsuarioCrear=request.session["user_id"],
            idUsuarioModificar=request.session["user_id"],
            fechaUltimaMod=fechaUltimaMod  
        )
        
        exito = service.crear_expediente(nuevo_expediente, idEstadoExpediente, lista_tiposObras, valoresPropietarios, valoresExpedientesProfesionales)  
    
        if "/" not in exito:
            # No contiene "/"
            parte1=""
        else:
            # Contiene "/"
            parte1, parte2 = exito.split("/")

        if parte1 == "duplicado":
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": "El Cuil/Cuit " + parte2 + " ingresado ya fue asignado a un Propietario. Verifique la información."}
            )
        
        else:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Expediente agregado exitosamente"}
            )

# ---------------------------------------
# OBTENER PROPIETARIOS DE UN EXPEDIENTE
# ---------------------------------------
#Retorna solo los propietarios de un expediente determinado. Relacion N a N
@router.get("/expediente/{idExpediente}/propietarios")
def get_propietarios_expediente(idExpediente: int, session: Session = Depends(get_session)):
    service = ExpedienteService(session)
    return service.get_propietarios(idExpediente)

# ---------------------------------------
# OBTENER PROFESIONALES DE UN EXPEDIENTE
# ---------------------------------------
#Retorna solo los propietarios de un expediente determinado. Relacion N a N
@router.get("/expediente/{idExpediente}/profesionales")
def get_profesionales_expediente(idExpediente: int, session: Session = Depends(get_session)):
    service = ExpedienteService(session)
    return service.get_profesionales(idExpediente)

# ---------------------------------------
# OBTENER ESTADOS DE UN EXPEDIENTE
# ---------------------------------------
#Retorna solo los estados de un expediente determinado. Relacion N a N
@router.get("/expediente/{idExpediente}/estados")
def get_estados_expediente(idExpediente: int, session: Session = Depends(get_session)):
    service = ExpedienteService(session)
    return service.get_estados(idExpediente)

# -------------------------------
# ACTUALIZAR EXPEDIENTE
# -------------------------------
@router.put("/expediente/{idExpediente}", response_model=ExpedienteModel)
async def update_expediente(
    request: Request, 
    idExpediente: int,
    expediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    fechaUltimaMod = datetime.now()

    expediente = ExpedienteModel(
        idExpediente = idExpediente,
        nroEntrada=expediente_data["nroEntrada"],
        anioMesaEntrada=expediente_data["anioMesaEntrada"],
        nroExpedienteMesaEntrada=expediente_data["nroExpedienteMesaEntrada"],
        nroPartida=expediente_data["nroPartida"],
        sucesion=expediente_data["sucesion"],
        observaciones=expediente_data["observaciones"],
        idUsuarioModificar=request.session["user_id"],
        fechaUltimaMod=fechaUltimaMod  
    )

    service = ExpedienteService(session)

    #Leer estado anterios
    idEstadoExpedienteAnterior=expediente_data["IDESTADOEXPEDIENTEEditHIDDEN"]
    #Leer el nuevo estado
    idEstadoExpedienteNuevo=expediente_data["idEstadoexpedienteEdit"]

    print("""==============================================================""")
    print("""PROPIETARIOS ROUTER""")
    print("""==============================================================""")
   
    # Procesar propietarios
    valoresPropietarios = []

    for valor in expediente_data.get("propietarios", []):  # recorre prop1...propN
        # valor esperado: "cuil/apellido/nombre/figuraPpal/calle/nroCalle/piso/dpto/areaCel/nroCel/email"
        partes = valor.split("/")
        
        #print("""pARTES!!!==============================================================""")
        #print(int(partes[3]) if partes[3] not in (None, "", "null") else 0)
        #print(partes[1])
        #print("""==============================================================""")

        #print(len(partes))

        if len(partes) >= 11:

                nro_calle_int = int(partes[5]) if partes[5] not in (None, "", "null") else None
                area_celular_int = int(partes[8]) if partes[8] not in (None, "", "null") else None
                nro_celular_int = int(partes[9]) if partes[9] not in (None, "", "null") else None
                figuraPpal_int = int(partes[3]) if partes[3] not in (None, "", "null") else 0

                propietario = PropietarioModel(
                    cuil_cuit = partes[0],
                    apellido = partes[1],
                    nombre = partes[2],
                   # figuraPpal = partes[3],
                    calle = partes[4],
                    nroCalle = nro_calle_int,
                    piso = partes[6],
                    nroDpto = partes[7],
                    areaCelular = area_celular_int,
                    nroCelular = nro_celular_int,
                    email = partes[10],
                    idUsuarioCrear=request.session["user_id"]
                )
                
                valoresPropietarios.append({
                        "propietario": propietario,
                        "figuraPpal": figuraPpal_int
                })

                #print("""valores!!!==============================================================""")
                #print(propietario.apellido)
                #print(propietario.nroCalle)
                #print("""==============================================================""")
 
    #print("Cantidad de propietarios router:!!!!!!!!", len(valoresPropietarios))

    print("""==============================================================""")
    print("""   PROFESIONALES ROUTER""")
    print("""==============================================================""")
    #Leer cantidad de propietarios
   # idFila: int = int(expediente_data["idFilaProfEdit"])  # cantProFESIONALES

    valoresProfesionales = []

    for valor in expediente_data.get("profesionales", []):
        partes = valor.split("/")
        if len(partes) >= 2:
            valoresProfesionales.append({
                "idProfesional": int(partes[0]) if partes[0] not in (None, "", "null") else None,
                "contactoPpal": int(partes[1]) if partes[1] not in (None, "", "null") else 0
        })

    exito = service.actualizar_expediente(expediente,idEstadoExpedienteAnterior,idEstadoExpedienteNuevo,valoresPropietarios,valoresProfesionales)
    
    if exito == "noExiste":
            return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content={"error": "Expediente no encontrado."}
                    )
    else:    
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Expediente actualizado exitosamente"}
              )
    
    #Cuando tenga que enviar el mail segun el estado a actulizar debo hacer esto y sacar el if anterior
'''    if exito == "noExiste":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Expediente no encontrado."}
        )

    # ✅ Enviar correo una vez actualizado
    try:
        destinatario = "nidia@9deJulio.gob.ar"
        asunto = f"Expediente actualizado N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"
        mensaje = f"""
        Se actualizó el expediente N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}.
        Nuevo estado: {idEstadoExpedienteNuevo}.
        Observaciones: {expediente.observaciones or 'Ninguna'}.
        """
        enviar_mail(destinatario, asunto, mensaje)
    except Exception as e:
        print(f"⚠️ Error al enviar el correo: {e}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Expediente actualizado exitosamente"}
    )
'''
    
      

# -------------------------------
# ELIMINAR EXPEDIENTE
# -------------------------------
@router.delete("/expediente/{idExpediente}")
async def delete_expediente(
    idExpediente: int,
    session: Session = Depends(get_session)
):
    service = ExpedienteService(session)  # ✅ instanciás la clase
    exito = service.eliminar_expediente(idExpediente)
    if not exito:
        return {"error": "Expediente no encontrado"}
      
    return {"message": "Expediente eliminado exitosamente"}


