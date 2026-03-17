from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List,Optional
from sqlmodel import Session
from fastapi.responses import JSONResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from datetime import datetime, date
from fastapi import status
from fastapi import BackgroundTasks

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

from services.email_service import enviar_expediente_creado

from utils.mail import enviar_mail 

router = APIRouter()
templates = Jinja2Templates(directory="templates")

ESTADO_DERECHO_CONSTRUCCION_PAGO = 7

#-------------------------------------------------
#Funciones de ayuda para parseqar datos
#-------------------------------------------------
CAMPOS_PROPIETARIO = [
    "cuil_cuit",
    "apellido",
    "nombre",
    "figuraPpal",
    "calle",
    "nroCalle",
    "piso",
    "nroDpto",
    "areaCelular",
    "nroCelular",
    "email"
]


def to_int(valor, default=None):
    if valor in (None, "", "null", "undefined"):
        return default
    return int(valor)


def parse_propietario_string(valor: str, user_id: int):
    """
    Convierte:
    'cuil/apellido/nombre/...'
    en:
    { propietario: PropietarioModel, figuraPpal:int }
    """

    partes = valor.split("/")

    if len(partes) < len(CAMPOS_PROPIETARIO):
        return None

    data = dict(zip(CAMPOS_PROPIETARIO, partes))

    propietario = PropietarioModel(
        cuil_cuit=data["cuil_cuit"],
        apellido=data["apellido"],
        nombre=data["nombre"],
        calle=data["calle"],
        nroCalle=to_int(data["nroCalle"]),
        piso=data["piso"],
        nroDpto=data["nroDpto"],
        areaCelular=to_int(data["areaCelular"]),
        nroCelular=to_int(data["nroCelular"]),
        email=data["email"],
        idUsuarioCrear=user_id
    )

    return {
        "propietario": propietario,
        "figuraPpal": to_int(data["figuraPpal"], 0)
    }


def parse_profesional_string(valor: str):
    partes = valor.split("/")

    if len(partes) < 2:
        return None

    return {
        "idProfesional": to_int(partes[0]),
        "contactoPpal": to_int(partes[1], 0)
    }

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
    background_tasks: BackgroundTasks,
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
    idFilaProf : int = Form(...),  # cantProfesionales

    # JSON con los tipos de obra seleccionados
    idTipoObra: str = Form(...),

    session: Session = Depends(get_session)
    ):
    
        service = ExpedienteService(session)  # ✅ instanciás la clase
        
        fechaUltimaMod = datetime.now()

        # Procesar Tipos de Obra (VIENEN COMO JSON STRING)
        lista_tiposObras = json.loads(idTipoObra)  # Ej: ["1","3","5"]

        if not lista_tiposObras:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Debe seleccionar al menos un Tipo de Obra"}
            )
       
        form = await request.form()

        # -------------------------
        # PROPIETARIOS
        # -------------------------
        valoresPropietarios = []
        for i in range(1, idFila + 1):
            valor = form.get(f"prop{i}", "").strip()
            if not valor:
                continue

            parsed = parse_propietario_string(
                valor,
                request.session["user_id"]
            )

            if parsed:
                valoresPropietarios.append(parsed)

        if not valoresPropietarios:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Debe ingresar al menos un propietario"}
            )

        # -------------------------
        # PROFESIONALES
        # -------------------------
        valoresExpedientesProfesionales = []

        if idFilaProf > 1 :
            for i in range(1, idFilaProf + 1):
                valor = form.get(f"prof{i}", "").strip()

                if not valor:
                    continue

                parsed = parse_profesional_string(valor)

                if parsed:
                    valoresExpedientesProfesionales.append(
                        Expediente_ProfesionalModel(**parsed)
                    )
        
        if not valoresExpedientesProfesionales:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Debe ingresar al menos un profesional"}
            )   
 

        #----------------------------------------------------
        # Expediente
        #----------------------------------------------------
        #Generando el nro de Legajo en forma automatica por año de mesa de entrada
        anioMesaEntrada = int(anioMesaEntrada) if anioMesaEntrada else None
        #armar nro de legajo....debe ser consecutivos por año. 
        nroLegajo = service.obtener_proximo_nro_legajo(anioMesaEntrada)
    
        print("nroLegajo ====================================================")
        print(nroLegajo)
        print("====================================================")

        #Generando el nro de Expediente en forma automatica por año actual solo cuando es estado seleccionado sea 7
        #Verificar estado Expediente

        nuevo_nroExpediente = None
        anioActual = None
        if idEstadoExpediente == ESTADO_DERECHO_CONSTRUCCION_PAGO: #DERECHO CONTRUCCION PAGO
            anioActual = datetime.now().year
            nuevo_nroExpediente = service.obtener_proximo_nro_expediente(anioActual)

            print("nuevo_nroExpediente ====================================================")
            print(nuevo_nroExpediente)
            print("====================================================")    

        nuevo_expediente = ExpedienteModel(
            idTipoExpediente=idTipoExpediente,
            nroLegajo=nroLegajo,
            nroExpediente=nuevo_nroExpediente,
            anioExpediente=anioActual,
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
            # Enviar correo una vez actualizado
            try:
                background_tasks.add_task(
                    enviar_expediente_creado,
                    "nidia@9dejulio.gov.ar",
                    nuevo_expediente.nroLegajo,
                    nuevo_expediente.anioMesaEntrada,
                    nuevo_expediente.nroPartida
                )

            except Exception as e:
                print(f"⚠️ Error al enviar el correo: {e}")

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Expediente agregado exitosamente y se ha enviado el mail."}
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
   
    # -------------------------
    # PROPIETARIOS
    # -------------------------
    valoresPropietarios = []

    for valor in expediente_data.get("propietarios", []):

        parsed = parse_propietario_string(
            valor,
            request.session["user_id"]
        )

        if parsed:
            valoresPropietarios.append(parsed)

    if not valoresPropietarios:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Debe ingresar al menos un propietario"}
        )

    # -------------------------
    # PROFESIONALES
    # -------------------------
    valoresProfesionales = []

    for valor in expediente_data.get("profesionales", []):

        parsed = parse_profesional_string(valor)

        if parsed:
            valoresProfesionales.append(parsed)

    if not valoresProfesionales:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Debe ingresar al menos un profesional"}
            )   

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

    # Enviar correo una vez actualizado
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


