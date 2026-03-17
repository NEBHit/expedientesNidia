from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List
from sqlmodel import Session

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.tipoExpediente_model import TipoExpedienteModel
from services.tipoExpediente_service import TipoExpedienteService

from config.conexion import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tiposExpedientes", response_model=List[TipoExpedienteModel])
async def get_tiposExpedientes(request: Request, session: Session = Depends(get_session)):

    service = TipoExpedienteService(session)  # ✅ instanciás la clase
    tiposExpedientes = service.listar_tipoExpedientes()  # ✅ usás el método de instancia

    return templates.TemplateResponse("listar_tiposExpedientes.html", { 
        "request": request,
        "tiposExpedientes": tiposExpedientes
    })

@router.get("/agregar_tipoExpediente", response_model=TipoExpedienteModel)
async def agregar_tipoExpediente_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoExpediente.html",{"request":request})
                                      
@router.post("/agregar_tipoExpediente", response_model=TipoExpedienteModel)
async def agregar_tipoExpediente_post(
    request: Request,
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoExpediente = TipoExpedienteModel(
        nombre=nombre,
        descripcion=descripcion,
        idUsuarioCrear=request.session["user_id"])
    
    service = TipoExpedienteService(session)
    service.crear_tipoExpediente(nuevo_tipoExpediente)
    return RedirectResponse("/tiposExpedientes", status_code=303)

@router.put("/tipoExpediente/{idTipoExpediente}", response_model=TipoExpedienteModel)
async def update_tipoExpediente(
    idTipoExpediente: int,
    tipoExpediente_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoExpediente = session.get(TipoExpedienteModel, idTipoExpediente)
    if not tipoExpediente:
        return {"error": "Tipo del Expediente no encontrado"}
    
    tipoExpediente.nombre = tipoExpediente_data["nombre"]
    tipoExpediente.descripcion = tipoExpediente_data.get("descripcion", "")
    
    service = TipoExpedienteService(session)
    service.actualizar_tipoExpediente(tipoExpediente)
    
    return tipoExpediente

@router.delete("/tipoExpediente/{idTipoExpediente}")
async def delete_tipoExpediente(
    idTipoExpediente: int,
    session: Session = Depends(get_session)
):
    service = TipoExpedienteService(session)
    exito = service.eliminar_tipoExpediente(idTipoExpediente)
    if not exito:
        return {"error": "Estado no encontrado"}
    return {"message": "Estado Expediente eliminado exitosamente"}
