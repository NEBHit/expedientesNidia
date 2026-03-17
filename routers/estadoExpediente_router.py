from fastapi import APIRouter, Depends, Form, Body, Request
from typing import List
from sqlmodel import Session
from models.estadoExpediente_model import EstadoExpedienteModel
from services.estadoExpediente_service import EstadoExpedienteService
from fastapi.responses import RedirectResponse
from config.conexion import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/estadosExpedientes", response_model=List[EstadoExpedienteModel])
async def get_estadoExpedientes(request: Request, session: Session = Depends(get_session)):

    service = EstadoExpedienteService(session)  # ✅ instanciás la clase
    estados = service.listar_estados()  # ✅ usás el método de instancia
    return templates.TemplateResponse("listar_estadosExpedientes.html", { 
        "request": request,
        "estadosExpedientes": estados
    })

@router.get("/agregar_estadoExpediente")
async def agregar(request: Request):
    return templates.TemplateResponse(
        "modalEstadoExpediente_add.html",
        {"request": request}
    )
                                      
@router.post("/agregar_estadoExpediente", response_model=EstadoExpedienteModel)
async def agregar_estadoExpediente_post(
    request: Request,
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_estadoExpediente = EstadoExpedienteModel(
        nombre=nombre,
        descripcion=descripcion,
        idUsuarioCrear=request.session["user_id"]
    )
     
    service = EstadoExpedienteService(session)
    service.crear_estado(nuevo_estadoExpediente)
    return RedirectResponse("/estadosExpedientes", status_code=303)
   

@router.put("/estadoExpediente/{idEstadoExpediente}", response_model=EstadoExpedienteModel)
async def update_estadoExpediente(
    idEstadoExpediente: int,
    estadoExpediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    estadoExpediente = session.get(EstadoExpedienteModel, idEstadoExpediente)
    if not estadoExpediente:
        return {"error": "Estado del Expediente no encontrado"}
    
    update_estado = EstadoExpedienteModel(
        idEstadoExpediente = idEstadoExpediente,
        nombre = estadoExpediente_data["nombre"],
        descripcion = estadoExpediente_data.get("descripcion", "")
    )
    
    service = EstadoExpedienteService(session)
    service.actualizar_estado(update_estado)
    return update_estado


@router.delete("/estadoExpediente/{idEstadoExpediente}")
async def delete_estadoExpediente(
    idEstadoExpediente: int,
    session: Session = Depends(get_session)
):
    service = EstadoExpedienteService(session)
    exito = service.eliminar_estado(idEstadoExpediente)
    if not exito:
        return {"error": "Estado no encontrado"}
    return {"message": "Estado Expediente eliminado exitosamente"}

