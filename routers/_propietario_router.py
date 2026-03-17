from fastapi import APIRouter, Depends, Body, Form
from typing import List, Optional
from sqlmodel import Session, select
from models.propietario_model import PropietarioModel
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Request
from config.conexion import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/propietarios", response_model=List[PropietarioModel])
async def get_propietarios(request: Request, session: Session = Depends(get_session)):
    propietarios = session.exec(select(PropietarioModel).order_by(PropietarioModel.apellido)).all()
   
   
    return templates.TemplateResponse("listar_propietarios.html", { 
        "request": request,
        "inspectores": propietarios
    })
  

@router.get("/agregar_propietario", response_model=PropietarioModel)
async def agregar_propietario_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_propietario.html",{"request":request})
                                      
@router.post("/agregar_propietario", response_model=PropietarioModel)
async def agregar_propietario_post(
    
    request: Request,
    cuil_cuit : str = Form(...),
    nombre : str = Form(...),
    apellido: str = Form(...),
    calle : str = Form(default=None),
    nroCalle : Optional[str] = Form(None),
    nroDpto : str = Form(default=None),
    piso : str = Form(default=None),
    areaCelular : Optional[str] = Form(None),
    nroCelular : Optional[str] = Form(None),
    email : str = Form(default=None),
        
    session: Session = Depends(get_session)
):
    
    # Validar CUIL duplicado
    propietario_existente = session.exec(
        select(PropietarioModel).where(PropietarioModel.cuil_cuit == cuil_cuit)
    ).first()
    
    if propietario_existente:
        return HTMLResponse(content="""
            <script>
              alert("Verifique el Cuil/Cuit. Ya existe un profesional registrado con ese CUIL.");
              history.back();  // vuelve al formulario sin cerrar el modal
            </script>
        """, status_code=200)

    nro_calle_int = int(nroCalle) if nroCalle else None
    area_celular_int = int(areaCelular) if areaCelular else None
    nro_celular_int = int(nroCelular) if nroCelular else None

    nuevo_propietario = PropietarioModel(
        cuil_cuit = cuil_cuit,
        nombre  = nombre,
        apellido = apellido,
        calle  = calle,
        nroCalle  = nro_calle_int,
        nroDpto  = nroDpto,
        piso  = piso,
        areaCelular  = area_celular_int,
        nroCelular  = nro_celular_int,
        email  = email,
        )
    
    session.add(nuevo_propietario)
    session.commit()
    session.refresh(nuevo_propietario)
    return RedirectResponse("/propietarios", status_code=303)

@router.put("/propietario/{idPropietario}", response_model=PropietarioModel)
async def update_propietario(
    idPropietario: int,
    propietario_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    propietario = session.get(PropietarioModel, idPropietario)
    if not propietario:
        return {"error": "Propietario no encontrado"}

    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    propietario.cuil_cuit = propietario_data["cuil_cuit"]
    propietario.nombre = propietario_data["nombre"]
    propietario.apellido = propietario_data["apellido"]
    propietario.calle = propietario_data.get("calle")
    propietario.nroCalle = clean_int(propietario_data.get("nroCalle"))
    propietario.nroDpto = propietario_data.get("nroDpto")
    propietario.piso = propietario_data.get("piso")
    propietario.areaCelular = clean_int(propietario_data.get("areaCelular"))
    propietario.nroCelular = clean_int(propietario_data.get("nroCelular"))
    propietario.email = propietario_data.get("email")
    
    session.add(propietario)
    session.commit()
    session.refresh(propietario)
    
    return propietario

@router.delete("/propietario/{idPropietario}")
async def delete_propietario(
    idPropietario: int,
    session: Session = Depends(get_session)
):
    propietario = session.get(PropietarioModel, idPropietario)
    if not propietario:
        return {"error": "Propietario no encontrado"}
    
    session.delete(propietario)
    session.commit()
    
    return {"message": "Propietario eliminado exitosamente"}
