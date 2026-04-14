from fastapi import APIRouter, Depends, Body, Form, Request
from sqlmodel import Session

from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

from datetime import datetime

import random
import string

from models.usuario_model import UsuarioModel
from services.usuario_service import UsuarioService

from config.conexion import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=302)


@router.get("/login")
async def login_form(request: Request):
    captcha = generar_captcha()
    request.session["captcha"] = captcha

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "captcha": captcha,
            "hide_layout": True
        }
    )

@router.get("/indexPpal")
async def indexPpal(request: Request):
    return templates.TemplateResponse(
        "indexPpal.html",
        {
            "request": request,
            "hide_layout": False
        }
    )

@router.post("/login")
async def login(
    request: Request,
    usuario: str = Form(...),
    clave: str = Form(...),
    captcha: str = Form(...),
    session: Session = Depends(get_session)
):
    #validar captcha (si o si debe estar en el router y no afuera porque lee la session)
    captcha_session = request.session.get("captcha")

    if not captcha_session or captcha.upper() != captcha_session:
        captcha_new = generar_captcha()
        request.session["captcha"] = captcha_new

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_login": "Captcha incorrecto",
                "usuario": usuario, 
                "captcha": captcha_new,
                "hide_layout": True
            }
        )
    
    service = UsuarioService(session)
    auth_result = service.authenticate(usuario, clave)

    if auth_result is None:
        captcha_new = generar_captcha()
        request.session["captcha"] = captcha_new

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_login": "El usuario no existe",
                "usuario": usuario,
                "captcha": captcha_new,
                "hide_layout": True
            }
        )

    if auth_result == "NO ACTIVO":
        captcha_new = generar_captcha()
        request.session["captcha"] = captcha_new

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_login": "Usuario no habilitado para usar la Aplicación",
                "usuario": usuario,
                "captcha": captcha_new,
                "hide_layout": True
            }
        )

    if auth_result is False:
        captcha_new = generar_captcha()
        request.session["captcha"] = captcha_new

        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error_login": "Contraseña incorrecta",
                "usuario": usuario,
                "captcha": captcha_new,
                "hide_layout": True
            }
        )

    # LOGIN OK
    # Limpiar captcha usado
    request.session.pop("captcha", None)
    request.session["user"] = auth_result.usuario
    request.session["user_id"] = auth_result.idUsuario

    auth_result.fechaUltimoLogin = datetime.now()   
    auth_result =service.actualizar_fechaUltimoLogin(auth_result)

    return RedirectResponse("/indexPpal", status_code=302)

def generar_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
@router.get("/captcha-refresh")
async def captcha_refresh(request: Request):
    captcha = generar_captcha()
    request.session["captcha"] = captcha
    return JSONResponse({"captcha": captcha})

@router.put("/cambiar-clave", response_model=UsuarioModel)
async def update_clave(
    request: Request,
    usuario_data: dict = Body(...),
    session: Session = Depends(get_session)
):
    
    #validar captcha
    captcha_session = request.session.get("captcha")
    captcha_cambio = usuario_data["captcha_cambio"]

    if not captcha_session or captcha_cambio.upper() != captcha_session:
        captcha_new = generar_captcha()
        request.session["captcha"] = captcha_new

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Captcha incorrecto en cambio de contraseña"}
        )
    
    #validar clave nueva y repeticion
    clave_nueva = usuario_data["clave_nueva"]
       
    usuario = UsuarioModel(
        usuario = usuario_data["usuarioMod"],
        clave = usuario_data["clave_actual"]
    )    
    
    service = UsuarioService(session)  # ✅ instanciás la clase
    usuario = service.authenticate(usuario.usuario, usuario.clave)
    
    if usuario is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Usuario no registrado"}
        )

    if usuario is False:
            
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "La contraseña actual es incorrecta"}
        )
          
    usuario.clave = service.hash_password(clave_nueva)

    usuario=service.actualizar_clave(usuario)  # ✅ usás el método de instancia
    
    if not usuario:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Usuario no registrado"}
        )
    
    return usuario


