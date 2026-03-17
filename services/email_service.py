import logging

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.settings import settings
from jinja2 import Environment, FileSystemLoader


# ---------------------------------
# LOGGER
# ---------------------------------
logger = logging.getLogger(__name__)


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=settings.MAIL_TLS,
    MAIL_SSL_TLS=settings.MAIL_SSL
)

env = Environment(loader=FileSystemLoader("templates"))


async def enviar_expediente_creado(destinatario, nro_legajo, anio, partida):

    try:
        #logger.info(f"Intentando enviar mail a {destinatario}")

        message = MessageSchema(
            subject="Nuevo expediente creado",
            recipients=[destinatario],
            body=f"""
                <h3>Nuevo expediente creado</h3>

                <p><b>Legajo:</b> {nro_legajo}</p>
                <p><b>Año:</b> {anio}</p>
                <p><b>Partida:</b> {partida}</p>
            """,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:

        logger.error(f"Error enviando mail: {e}")