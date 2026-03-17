from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse 

import logging

from config.auth import AuthMiddleware
from routers.usuario_router import router as usuarioRouter
from routers.estadoExpediente_router import router as estadoExpedienteRouter
from routers.estadoInspeccion_router import router as estadoInspeccionRouter
from routers.inspector_router import router as inspectorRouter
from routers.tipoExpediente_router import router as tipoExpedienteRouter
from routers.tipoObra_router import router as tipoObraRouter
from routers.tipoProfesion_router import router as tipoProfesionRouter
from routers.profesional_router import router as profesionalRouter
from routers.expediente_router import router as expedienteRouter

# ----------------------
# IMPORTAR MODELOS (REGISTRA RELACIONES)
# ----------------------
import models  # registra todos los modelos antes de crear tablas

#Registro de logues 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI()

# AUTH 
app.add_middleware(AuthMiddleware)

# SESIONES 
app.add_middleware(
    SessionMiddleware,
    secret_key="CLAVE_SUPER_SECRETA_CAMBIAR"
)

# Montar la carpeta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse("/login")

templates = Jinja2Templates(directory="templates")

app.include_router(usuarioRouter, prefix="", tags=["usuario"])
app.include_router(estadoExpedienteRouter, prefix="", tags=["estadosExpedientes"])
app.include_router(estadoInspeccionRouter, prefix="", tags=["estadosInspecciones"])
app.include_router(inspectorRouter, prefix="", tags=["inspectores"])
app.include_router(tipoExpedienteRouter, prefix="", tags=["tiposExpedientes"])
app.include_router(tipoObraRouter, prefix="", tags=["tiposObras"])
app.include_router(tipoProfesionRouter, prefix="", tags=["tiposProfesiones"])
app.include_router(profesionalRouter, prefix="", tags=["profesionales"])
app.include_router(expedienteRouter, prefix="", tags=["expedientes"])


