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

encabezadoMail = encabezadoMail = """
<h3>
MUNICIPALIDAD DE 9 DE JULIO - SEC. DE VIVIENDA Y URBANISMO <br>
OFICINA DE OBRAS PARTICULARES <br>
EXPEDIENTE DE OBRA
</h3>
<hr>
"""

footerMail = """
<hr>
<p>
Líneas Rotativas: 2317 - 610000<br>
Interno: 133 - Oficina de Obras Particulares
</p>
"""
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

        logger.info("Email enviado correctamente")

    except Exception as e:

        logger.error(f"Error enviando email: {e}")


async def enviar_mail_aInspeccionar(destinatario: str, data: dict, cc: str = None):
    
    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
        celularPropietario = data["celularPropietario"]
        
        subject = f"AVISO A INSPECCION EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {nro}/{anio}</b> ha pasado a <b> INSPECCION </b>.<br>
        Para la coordinación de la misma, de ser necesario, nos pondremos en contacto al telefono: {celularPropietario} brindado por usted en la nota al intendente.
        </p>
        
        <br>

        <p>Saludos cordiales.</p>

        {footerMail}
        """
        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")

    except Exception as e:
        logger.error(f"Error enviando email: {e}")

 
async def enviar_mail_aUrbanismo(destinatario: str, data: dict, cc: str = None):

    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
    
        subject = f"AVISO DE PASE A URBANISMO DE EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {nro}/{anio}</b> ha sido INSPECCIONADA y pasó a la Oficina de Urbanismo para su <b> Revisión.</b><br>
        </p>
        
        <br>

        <p>Saludos cordiales.</p>

        {footerMail}
        """
       
        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")


    except Exception as e:
        logger.error(f"Error enviando email: {e}")     

async def enviar_mail_carpetaIncompleta(destinatario: str, data: dict, cc: str = None):
    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
    
        subject = f"AVISO DE CARPETA INCOMPLETA EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {nro}/{anio}</b> ha sido ingresada <b>INCOMPLETA</b>.
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

        {footerMail}
        """

        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")


    except Exception as e:
        logger.error(f"Error enviando email: {e}")        

async def enviar_mail_derechoConstruccionAPagar(destinatario: str, data: dict, cc: str = None):
#Este mail envia un archivo adjunto formato pdf 
    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
     
        subject = f"NOTIFICACION DE DERECHO DE CONSTRUCCION EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para enviarle en ADJUNTO archivo pdf con la LIQUIDACIÓN DE LOS DERECHOS DE CONSTRUCCION (Ordenanza Fiscal e Impositiva 2026) perteneciente al <b> Expediente Mesa de Entrada: {nro}/{anio}</b>, para que pueda efectura el pago de los mismos. 
        Información con fecha de vencimiento.>br>
        <b>Por favor confirmar recepción</b>.
        </p>

        <p>Se solicita que una vez efectuado el pago de los mismos se acerque a esta Oficina con una copia del pago para incorporarla al Expediente</p>

        <br>

        <p>Saludos cordiales.</p>

        {footerMail}
        """

        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")

    except Exception as e:
        logger.error(f"Error enviando email: {e}")       

async def enviar_mail_expedienteConDeuda(destinatario: str, data: dict, cc: str = None):

    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
    
        subject = f"AVISO DE DEUDA EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para informarle que el <b> Expediente Mesa de Entrada: {nro}/{anio}</b> posee <b>deudas municipales</b>.
        </p>

        <p>Solicitamos se acerque a la <b> OFICINA DE INGRESOS PUBLICOS </b> a regularizar el estado de la deuda. Esto implica:</p>
    
        <ul>
            <li>Pedir la Solicitud del Informe de Deuda</li>
            <li>Cancelar dicha deuda (Presentación de pagos)</li>
        </ul>

        <p>
        Una vez realizado lo anterior en la Oficina de Ingresos Públicos esta oficna (Obras Particulares) le expedirá el CERTIFICADO LIBRE DE DEUDA. Una vez expedido el certificado se podra proseguir con el trámite iniciado.
        
        <br>
        Queda usted debidamente notificado.
        </p>

        <br>

        <p>Saludos cordiales.</p>

        {footerMail}

        """

        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")

    except Exception as e:
        logger.error(f"Error enviando email: {e}")     

async def enviar_mail_expedienteFinalizado(destinatario: str, data: dict, cc: str = None):

    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
    
        subject = f"AVISO DE FINALIZACIÓN DE TRÁMITE EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto desde la Oficina de Obras Particulares para informarle que el trámite correspondiente al <b> Expediente Mesa de Entrada: {nro}/{anio}</b> ha <b>FINALIZADO</b>.
        </p>
        <p><b>Se solicita que se acerque a esta oficina para Retirar los Planos.</b><br></p>

        <br>

        <p>Saludos cordiales.</p>

        {footerMail}
        """

        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")

    except Exception as e:
        logger.error(f"Error enviando email: {e}")     

async def enviar_mail_expedienteACatastro(destinatario: str, data: dict, cc: str = None):

    try:
        nro = data["nroExpedienteMesaEntrada"]
        anio = data["anioMesaEntrada"]
        partida = data["noPartida"]
     
        subject = f"AVISO DE PASE A CATASTRO EXPTEDIENTE Mesa de Entradas N° {nro}/{anio}"

        body = f"""
        {encabezadoMail}

        <p>
        Buen día,<br><br>

        nos ponemos en contacto para informarle que la Carpeta de Obra del <b> Expediente Mesa de Entrada: {nro}/{anio}</b> ha sido enviada a la <b>Oficna de Catastro</b> para la revisión de los datos catastrales, Nº de Partida {partida} y titularidad de la propiedad.
        </p>
        <br>
        <p>De corresponder desde la oficina de Catastro se comunicarán para corregir y/o agregar información faltante. Caso contrario el expedeinte continua con su recorrido</p>

        <br>

        <p>Saludos cordiales.</p>

        {footerMail}
        """

        message = MessageSchema(
                    subject=subject,
                    recipients=[destinatario],
                    cc=[cc] if cc else [],
                    body=body,
                    subtype="html"
                )

        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email enviado a {destinatario} CC: {cc}")


    except Exception as e:
        logger.error(f"Error enviando email: {e}")     