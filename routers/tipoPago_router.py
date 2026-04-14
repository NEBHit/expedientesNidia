from fastapi import APIRouter, Depends, Body, Form, Request
from typing import List
from sqlmodel import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.tipoPago_model import TipoPagoModel
from services.tipoPago_service import TipoPagoService

from config.conexion import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tiposPagos", response_model=List[TipoPagoModel])
async def get_tiposPagos(request: Request, session: Session = Depends(get_session)):
        
    service = TipoPagoService(session)  # ✅ instanciás la clase
    tiposPagos = service.listar_TipoPagos()  # ✅ usás el método de instancia
   
    return templates.TemplateResponse("listar_tiposPagos.html", { 
        "request": request,
        "tiposPagos": tiposPagos
    })

@router.get("/agregar_TipoPago", response_model=TipoPagoModel)
async def agregar_TipoPago_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_TipoPago.html",{"request":request})

                                      
@router.post("/agregar_TipoPago", response_model=TipoPagoModel)
async def agregar_TipoPago_post(
    request: Request,
    nombre : str = Form(...),
    descripcion: str = Form(...),
    session: Session = Depends(get_session)
):
    nuevo_TipoPago = TipoPagoModel(
        nombre=nombre,
        descripcion=descripcion,
        idUsuarioCrear=request.session["user_id"])
    
    service = TipoPagoService(session)  # ✅ instanciás la clase
    service.crear_tipoExpediente(nuevo_TipoPago)  # ✅ usás el método de instancia
  
    return RedirectResponse("/tiposPagos", status_code=303)

@router.put("/TipoPago/{idTipoPago}", response_model=TipoPagoModel)
async def update_TipoPago(
    idTipoPago: int,
    TipoPago_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    TipoPago = session.get(TipoPagoModel, idTipoPago)
    if not TipoPago:
        return {"error": "Tipo de Pago no encontrado"}
    
    TipoPago.nombre = TipoPago_data["nombre"]
    TipoPago.descripcion = TipoPago_data.get("descripcion", "")
    
    service = TipoPagoService(session)  # ✅ instanciás la clase
    service.actualizar_TipoPago(TipoPago)  # ✅ usás el método de instancia
     
    return TipoPago

@router.delete("/TipoPago/{idTipoPago}")
async def delete_TipoPago(
    idTipoPago: int,
    session: Session = Depends(get_session)
):
    service = TipoPagoService(session)
    exito = service.eliminar_TipoPago(idTipoPago)
    if not exito:
        return {"error": "Tipo Pago no encontrado"}
    return {"message": "Tipo pago eliminado exitosamente"}


