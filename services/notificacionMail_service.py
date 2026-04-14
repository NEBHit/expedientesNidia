import logging
import asyncio

from fastapi import BackgroundTasks
from email_validator import validate_email, EmailNotValidError

from models.expediente_model import ExpedienteModel

from services.email_service import (
    enviar_mail_carpetaIncompleta,
    enviar_mail_expedienteACatastro,
    enviar_mail_expedienteConDeuda,
    enviar_mail_aInspeccionar,
    enviar_mail_aUrbanismo,
    enviar_mail_derechoConstruccionAPagar,
    enviar_mail_expedienteFinalizado,
)

logger = logging.getLogger(__name__)

# -------------------------
# VALIDACIÓN EMAIL
# -------------------------
def es_email_valido(email: str) -> bool:
    try:
        validate_email(email, check_deliverability=True)
        return True
    except EmailNotValidError as e:
        logger.warning(f"Email inválido: {email} - {e}")
        return False


# -------------------------
# DESTINATARIOS
# -------------------------
#def obtener_destinatarios(expediente: ExpedienteModel) -> List[str]:
    #expediente.emailPropietario,
    #expediente.emailProfesional

#    return ["nidia@9dejulio.gov.ar"]

def obtener_destinatarios(idEstadoExpediente: int, mailProp: str, mailProf:str):
    funcion = MAPA_DESTINATARIOS.get(idEstadoExpediente)

    if not funcion:
        return {"to": None, "cc": None}

    data = funcion(mailProp,mailProf)

    # limpiar nulos
    to = data.get("to")
    cc = data.get("cc") # Si el dia de mañana hay wque enviarlo a mas de un destinatario con CC reemplazar por esto: [email for email in data.get("cc", []) if email]

    return {
        "to": to,
        "cc": cc
    }

def destinatario_propietario_con_profesional(mailProp: str, mailProf:str):
    return {
        "to": mailProp,
        "cc": mailProf
    }

def destinatario_profesional_con_propietario(mailProp: str, mailProf:str):
    return {
        "to": mailProf,
        "cc": mailProp
    }

# -------------------------
# MAPA DE DESTINATARIOS
# -------------------------
#Este mapa se arma relacionando el estado del expediente
MAPA_DESTINATARIOS = {
    1: destinatario_profesional_con_propietario,
    2: destinatario_profesional_con_propietario,
    3: destinatario_propietario_con_profesional,
    4: destinatario_profesional_con_propietario,
    5: destinatario_profesional_con_propietario,
    6: destinatario_propietario_con_profesional,
    8: destinatario_propietario_con_profesional
}

# -------------------------
# MAPA DE MAILS
# -------------------------
MAPA_MAILS = {
    1: enviar_mail_carpetaIncompleta,
    2: enviar_mail_expedienteACatastro,
    3: enviar_mail_expedienteConDeuda,
    4: enviar_mail_aInspeccionar,
    5: enviar_mail_aUrbanismo,
    6: enviar_mail_derechoConstruccionAPagar,
    8: enviar_mail_expedienteFinalizado,
}

# -------------------------
# WRAPPER ASYNC
# -------------------------
def ejecutar_async(func, *args):
    asyncio.run(func(*args))



# -------------------------
# FUNCIÓN PRINCIPAL
# -------------------------
def enviarMailSegunEstado(idEstadoExpediente: int, expediente: ExpedienteModel, background_tasks: BackgroundTasks, emailPropietario: str, celularPropietario: str, emailProfesional: str):
    try:
        idEstadoExpediente = int(idEstadoExpediente)

        funcion_mail = MAPA_MAILS.get(idEstadoExpediente)

        if not funcion_mail:
            return {
                "ok": False,
                "mensaje": "El Estado del Expediente no válido. Verifique la información"
            }

        # SOLO DATOS NECESARIOS
        data_mail = {
            "nroExpedienteMesaEntrada": expediente.nroExpedienteMesaEntrada,
            "anioMesaEntrada": expediente.anioMesaEntrada,
            "celularPropietario": celularPropietario,
            "nroPartida": expediente.nroPartida,
        }

        destinatarios = obtener_destinatarios(idEstadoExpediente, emailPropietario, emailProfesional)

        to = destinatarios["to"]
        cc = destinatarios["cc"]

        # VALIDACIÓN TO
        if not to or not es_email_valido(to):
            return {
                "ok": False,
                "mensaje": "Email principal inválido. Verifique la direccion PRINCIPAL de email del Propietario o Profesional."
            }

        # VALIDACIÓN CC 
        if cc and not es_email_valido(cc):
            logger.warning(f"CC inválido: {cc}")
            cc = None

        logger.info(f"Enviando mail TO: {to} CC: {cc}")

        # ENVÍO MAIL
        background_tasks.add_task(
            ejecutar_async,
            funcion_mail,
            to,
            data_mail,
            cc
        )

        return {
            "ok": True,
            "mensaje": "El email fue enviado correctamente."
        }

    except Exception as e:
        logger.error(f"Error al enviar email: {str(e)}")

        return {
            "ok": False,
            "mensaje": f"Error al enviar email: {str(e)}"
        }
        
       