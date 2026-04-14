from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, select, create_engine
import math

app = FastAPI()
templates = Jinja2Templates(directory="templates")

engine = create_engine("sqlite:///./test.db")

class Profesional(SQLModel, table=True):
    id: int | None = None
    nombre: str
    apellido: str
    cuil_cuit: str
    calle: str
    nroCalle: str
    piso: str
    dpto: str
    areaCelular: str
    nroCelular: str
    matricula: str
    razonSocial: str
    idTipoProfesion: str
    mail: str

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/profesionales", name="mostrar_profesionales")
def mostrar_profesionales(request: Request, page: int = 1, session: Session = Depends(get_session)):
    per_page = 10

    total = session.exec(select(Profesional)).count()
    total_pages = math.ceil(total / per_page)

    profesionales = session.exec(
        select(Profesional)
        .offset((page - 1) * per_page)
        .limit(per_page)
    ).all()

    columnas = [
        {"nombre": "Nombre"},
        {"nombre": "Apellido"},
        {"nombre": "CUIL"},
        {"nombre": "Calle"},
        {"nombre": "Nro Calle"},
    ]

    return templates.TemplateResponse("tabla.html", {
        "request": request,
        "titulo": "Listado de Profesionales",
        "nomBtnAdd": "Profesional",
        "nomtabla": "profesional",
        "columnas": columnas,
        "valores": profesionales,
        "page": page,
        "total_pages": total_pages,
        "url_base": "mostrar_profesionales"
    })