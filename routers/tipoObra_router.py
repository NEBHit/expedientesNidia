from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List
from sqlmodel import Session
from fastapi.responses import RedirectResponse

from models.tipoObra_model import TipoObraModel
from services.tipoObra_service import TipoObraService

from config.conexion import get_session

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tiposObras", response_model=List[TipoObraModel])
async def get_tiposObras(request: Request, session: Session = Depends(get_session)):
        
    service = TipoObraService(session)  # ✅ instanciás la clase
    tiposObras = service.listar_tipoObras()  # ✅ usás el método de instancia
   
    return templates.TemplateResponse("listar_tiposObras.html", { 
        "request": request,
        "tiposObras": tiposObras
    })

@router.get("/agregar_tipoObra", response_model=TipoObraModel)
async def agregar_tipoObra_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoObra.html",{"request":request})

                                      
@router.post("/agregar_tipoObra", response_model=TipoObraModel)
async def agregar_tipoObra_post(
    request: Request,
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoObra = TipoObraModel(
        nombre=nombre,
        descripcion=descripcion,
        idUsuarioCrear=request.session["user_id"])
    
    service = TipoObraService(session)  # ✅ instanciás la clase
    service.crear_tipoExpediente(nuevo_tipoObra)  # ✅ usás el método de instancia
  
    return RedirectResponse("/tiposObras", status_code=303)

@router.put("/tipoObra/{idTipoObra}", response_model=TipoObraModel)
async def update_tipoObra(
    idTipoObra: int,
    tipoObra_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoObra = session.get(TipoObraModel, idTipoObra)
    if not tipoObra:
        return {"error": "Tipo de Obra no encontrado"}
    
    tipoObra.nombre = tipoObra_data["nombre"]
    tipoObra.descripcion = tipoObra_data.get("descripcion", "")
    
    service = TipoObraService(session)  # ✅ instanciás la clase
    service.actualizar_tipoObra(tipoObra)  # ✅ usás el método de instancia
     
    return tipoObra

@router.delete("/tipoObra/{idTipoObra}")
async def delete_tipoObra(
    idTipoObra: int,
    session: Session = Depends(get_session)
):
    service = TipoObraService(session)
    exito = service.eliminar_tipoObra(idTipoObra)
    if not exito:
        return {"error": "Tipo Obra no encontrado"}
    return {"message": "Tipo Obra eliminado exitosamente"}


