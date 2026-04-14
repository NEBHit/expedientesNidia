from fastapi import APIRouter, Depends, Body, Form
from typing import List
from sqlmodel import Session
from models.inspector_model import InspectorModel
from services.inspector_service import InspectorService
from fastapi.responses import RedirectResponse
from fastapi import Request
from config.conexion import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/inspectores", response_model=List[InspectorModel])
async def get_inspectores(request: Request, session: Session = Depends(get_session)):
    service = InspectorService(session)  # ✅ instanciás la clase
    inspectores = service.listar_inspectores()  # ✅ usás el método de instancia

    return templates.TemplateResponse("listar_inspectores.html", { 
        "request": request,
        "inspectores": inspectores
    })

@router.get("/agregar_inspector", response_model=InspectorModel)
async def agregar_inspector_get(nombre: str = Form(...), apellido: str = Form(...), session: Session = Depends(get_session)):

    service = InspectorService(session)  # ✅ instanciás la clase
    inspectores = service.crear_inspector(nombre, apellido)  # ✅ usás el método de instancia

    return RedirectResponse("/inspectores", status_code=303)
                                      
@router.post("/agregar_inspector", response_model=InspectorModel)
async def agregar_inspector_post(
    request: Request,
    nombre : str = Form(...),
    apellido: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_inspector = InspectorModel(
        nombre=nombre,
        apellido=apellido,
        idUsuarioCrear=request.session["user_id"]
    )
    
    service = InspectorService(session)
    service.crear_inspector(nuevo_inspector)
    
    return RedirectResponse("/inspectores", status_code=303)

@router.put("/inspector/{idInspector}", response_model=InspectorModel)
async def update_inspector(
    idInspector: int,
    inspector_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    inspector = session.get(InspectorModel, idInspector)
    if not inspector:
        return {"error": "Inspector no encontrado"}
    
    inspector.nombre = inspector_data["nombre"]
    inspector.apellido = inspector_data.get("apellido", "")
    
    service = InspectorService(session)
    service.actualizar_inspector(inspector)
        
    return inspector

@router.delete("/inspector/{idInspector}")
async def delete_inspector(
    idInspector: int,
    session: Session = Depends(get_session)
):
    service = InspectorService(session)
    exito = service.eliminar_inspector(idInspector)
    if not exito:
        return {"error": "Inspector no encontrado"}
    return {"message": "Isnpector eliminado exitosamente"}



