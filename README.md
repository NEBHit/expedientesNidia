# expedientes_obras

Sistema web para la **Gestión de expedientes de obras particulares**, orientado a uso municipal.

La aplicación permite administrar expedientes, profesionales, propietarios y datos relacionados, utilizando una arquitectura web moderna basada en **FastAPI**.


---

## Generar requeriments
pip freeze > requeriments.txt

## Restaurar
pip install -r requeriments.txt

## Subir cambios a git
git add *
git commit -m 'UploadXX'
git push

---

## Tecnologías utilizadas

- **FastAPI** – Backend web
- **Jinja2** – Templates HTML
- **SQLAlchemy / SQLModel** – ORM y modelos
- **Uvicorn** – Servidor ASGI
- **MySQL / MariaDB** – Base de datos
- **Bootstrap** – Estilos del frontend
- **SessionMiddleware** – Manejo de sesiones (cookies firmadas)

---

##  Requisitos previos

- Python **3.11 o superior** (recomendado)
- Git
- Base de datos **MySQL / MariaDB**

---

##  Instalación del proyecto

###  Clonar el repositorio

    ```bash
    git clone https://github.com/sistemas9dj/expedientes_obras.git
    cd expedientes_obras


