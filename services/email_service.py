import logging

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.settings import settings
from jinja2 import Environment, FileSystemLoader

from models.expediente_model import ExpedienteModel

#Servicio para el envio de los distintos mails segun los estados seeccionados por el usuario
#Cada estado tiene un formato distinto y algunos tienen adjuntos

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
    MAIL_SSL_TLS=settings.MAIL_SSL,
    USE_CREDENTIALS=False
)

env = Environment(loader=FileSystemLoader("templates"))

async def enviar_expediente_creado(destinatario, nro_legajo, anio, partida):

    try:
        
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

async def enviar_mail_aInspeccionar(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")     

async def enviar_mail_aUrbanismo(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")     

async def enviar_mail_carpetaIncompleta(destinatario: str, expediente: ExpedienteModel):
    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        <br><br>
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")        

async def enviar_mail_derechoConstruccionAPagar(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")       

async def enviar_mail_expedienteConDeuda(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")     

async def enviar_mail_expedienteFinalizado(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        OFICINA DE OBRAS PARTICULARES
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")     

async def enviar_mail_expedienteACatastro(destinatario:str, expediente: ExpedienteModel):

    try:
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}"

        body = f"""
        <h3>
        MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO
        <p>
        OFICINA DE OBRAS PARTICULARES
        </p>
        </h3>
        
        <hr>

        <p>
        Buen día,<br><br>

        Nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {expediente.nroExpedienteMesaEntrada}/{expediente.anioMesaEntrada}</b> ha sido ingresada <b>incompleta</b>.
        </p>

        <p>Faltan algunos de los siguientes datos:</p>

        <ul>
            <li>Carpeta Amarilla Incompleta</li>
            <li>Nota de la Intendente Incompleta</li>
            <li>Falta Planilla de Estadísticas</li>
        </ul>

        <p>
        Se solicita que se acerque a la oficina para completar la información.<br>
        Mientras tanto, el expediente queda retenido en esta oficina.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        <hr>

        <p>
        Líneas Rotativas: 2317 - 610000<br>
        Interno: 133 - Oficina de Obras Particulares
        </p>
        """

        message = MessageSchema(
            subject=subject,
            recipients=[destinatario],
            body=body,
            subtype="html"
        )

        fm = FastMail(conf)

        await fm.send_message(message)

        logger.info("Correo enviado correctamente")

    except Exception as e:
        logger.error(f"Error enviando mail: {e}")     