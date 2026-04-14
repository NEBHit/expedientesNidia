from fastapi import APIRouter, Depends, Body, Form
from typing import List, Optional
from sqlmodel import Session

from models.profesional_model import ProfesionalModel
from services.profesional_service import ProfesionalService
from services.tipoProfesion_service import TipoProfesionService

from fastapi.responses import RedirectResponse,JSONResponse
from fastapi import Request
from config.conexion import get_session
from fastapi.templating import Jinja2Templates
from fastapi import status


router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/profesionales", response_model=List[ProfesionalModel])
async def get_profesionales(request: Request, session: Session = Depends(get_session)):

    service = ProfesionalService(session)  # ✅ instanciás la clase
    profesionales = service.listar_profesionales()  # ✅ usás el método de instancia
    
    serviceTipo = TipoProfesionService(session)  # ✅ instanciás la clase
    tiposProfesiones = serviceTipo.listar_tipoProfesiones()  # ✅ usás el método de instancia
          
    return templates.TemplateResponse("listar_profesionales.html", { 
        "request": request,
        "profesionales": profesionales,
        "tiposProfesiones": tiposProfesiones
    })

@router.get("/agregar_profesional", response_model=ProfesionalModel)
async def agregar_profesional_get(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("agregar_profesional.html",{"request":request})
                                      
@router.post("/agregar_profesional", response_model=ProfesionalModel)
async def agregar_profesional_post(
    
    request: Request,
    cuil_cuit : str = Form(...),
    nombre : str = Form(...),
    apellido: str = Form(...),
    razonSocial : str = Form(default=None),
    calle : str = Form(default=None),
    nroCalle : Optional[str] = Form(None),
    nroDpto : str = Form(default=None),
    piso : str = Form(default=None),
    areaCelular : Optional[str] = Form(None),
    nroCelular : Optional[str] = Form(None),
    matricula : str = Form(default=None),
    email : str = Form(default=None),
    idTipoProfesion : int = Form(...),  # debe ser int
      
    session: Session = Depends(get_session)
):
    nro_calle_int = int(nroCalle) if nroCalle else None
    area_celular_int = int(areaCelular) if areaCelular else None
    nro_celular_int = int(nroCelular) if nroCelular else None

    nuevo_profesional = ProfesionalModel(
        cuil_cuit = cuil_cuit,
        nombre  = nombre,
        apellido = apellido,
        razonSocial  = razonSocial,
        calle  = calle,
        nroCalle  = nro_calle_int,
        nroDpto  = nroDpto,
        piso  = piso,
        areaCelular  = area_celular_int,
        nroCelular  = nro_celular_int,
        matricula  = matricula,
        email  = email,
        idTipoProfesion = idTipoProfesion,
        idUsuarioCrear=request.session["user_id"]   
        )
    
    service = ProfesionalService(session)  # ✅ instanciás la clase
    service.crear_profesional(nuevo_profesional)  # ✅ usás el método de instancia

    return RedirectResponse("/profesionales", status_code=303)

@router.put("/profesional/{idProfesional}", response_model=ProfesionalModel)
async def update_profesional(
    idProfesional: int,
    profesional_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    
   # print("id: " +  str(idProfesional))

    # Helper para convertir campos vacíos a None
    def clean_int(value):
        return int(value) if isinstance(value, int) or (isinstance(value, str) and value.strip().isdigit()) else None
    
    profesional = ProfesionalModel(
        idProfesional = idProfesional,
        cuil_cuit = profesional_data["cuil_cuit"],
        nombre = profesional_data["nombre"],
        apellido = profesional_data["apellido"],
        razonSocial = profesional_data.get("razonSocial"),
        calle = profesional_data.get("calle"),
        nroCalle = clean_int(profesional_data.get("nroCalle")),
        nroDpto = profesional_data.get("nroDpto"),
        piso = profesional_data.get("piso"),
        areaCelular = clean_int(profesional_data.get("areaCelular")),
        nroCelular = clean_int(profesional_data.get("nroCelular")),
        matricula = profesional_data.get("matricula"),
        email = profesional_data.get("email"),
        idTipoProfesion = clean_int(profesional_data.get("idTipoProfesion"))
    )

    service = ProfesionalService(session)  # ✅ instanciás la clase
    exito = service.actualizar_profesional(profesional)  # ✅ usás el método de instancia

    if exito == "noExiste":
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Profesional no encontrado"}
        )
    elif exito == "cuilRepetido":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": "El Cuil/Cuit ingresado ya fue asignado a un Profesional. Verifique la información."}
        )
    else:
        return exito
        

@router.delete("/profesional/{idProfesional}")
async def delete_profesional(
    idProfesional: int,
    session: Session = Depends(get_session)
):
    profesional = session.get(ProfesionalModel, idProfesional)
    if not profesional:
        return {"error": "Profesional no encontrado"}
    
    session.delete(profesional)
    session.commit()
    
    return {"message": "Profesional eliminado exitosamente"}


