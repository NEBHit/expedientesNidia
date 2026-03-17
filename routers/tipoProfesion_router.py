from fastapi import APIRouter, Depends, Body, Form,Request,status
from typing import List
from sqlmodel import Session
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates

from models.tipoProfesion_model import TipoProfesionModel
from services.tipoProfesion_service import TipoProfesionService

from config.conexion import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tiposProfesiones", response_model=List[TipoProfesionModel])
async def get_tiposProfesiones(request: Request, session: Session = Depends(get_session)):
    service = TipoProfesionService(session)  # ✅ instanciás la clase
    tiposProfesiones = service.listar_tipoProfesiones()  # ✅ usás el método de instancia

    return templates.TemplateResponse("listar_tiposProfesiones.html", { 
        "request": request,
        "tiposProfesiones": tiposProfesiones
    })

@router.get("/agregar_tipoProfesion", response_model=TipoProfesionModel)
async def agregar_tipoProfesion_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_tipoProfesion.html",{"request":request})
                                      
@router.post("/agregar_tipoProfesion", response_model=TipoProfesionModel)
async def agregar_tipoProfesion_post(
    request: Request,
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_tipoProfesion = TipoProfesionModel(
        nombre=nombre,
        descripcion=descripcion,
        idUsuarioCrear=request.session["user_id"])
    
    service = TipoProfesionService(session)  # ✅ instanciás la clase
    service.crear_tipoProfesion(nuevo_tipoProfesion)  # ✅ usás el método de instancia
  
    return RedirectResponse("/tiposProfesiones", status_code=303)

@router.put("/tipoProfesion/{idTipoProfesion}", response_model=TipoProfesionModel)
async def update_tipoProfesion(
    idTipoProfesion: int,
    tipoProfesion_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    tipoProfesion = TipoProfesionModel(
        idTipoProfesion = idTipoProfesion,
        nombre = tipoProfesion_data["nombre"],
        descripcion = tipoProfesion_data.get("descripcion", "")
    )    
    
    service = TipoProfesionService(session)  # ✅ instanciás la clase
    tipoProfesion=service.actualizar_tipoProfesion(tipoProfesion)  # ✅ usás el método de instancia
    
    if not tipoProfesion:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Tipo de Profesión no encontrado"}
        )
    
    return tipoProfesion


@router.delete("/tipoProfesion/{idTipoProfesion}")
async def delete_tipoProfesion(
    idTipoProfesion: int,
    session: Session = Depends(get_session)
):
    service = TipoProfesionService(session)
    exito = service.eliminar_tipoProfesion(idTipoProfesion)

    if exito == "no existe":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Tipo de Profesión no encontrado"}
        )
    elif exito == "relacionado":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "No se puede eliminar el Tipo de Profesión porque está asignado a algún profesional"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Tipo de Profesión eliminado exitosamente"}
        )
   