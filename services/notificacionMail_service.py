import logging

from typing import List, Union
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
#Funcion que valida si despues de @ corresponde a un tipo de mail valido
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
#Funcion que retorna el destinatario o los destinatarios. Hay que implementarla cuando pasen el formato
def obtener_destinatarios(expediente: ExpedienteModel) -> List[str]:
    return ["nidia@9dejulio.gov.ar"]

# ------------------------------------------
# FUNCIONES AL QUE DEBE LLAMAR SEGUN ESTADO
# ------------------------------------------
MAPA_MAILS = {
    1: enviar_mail_carpetaIncompleta,
    2: enviar_mail_expedienteACatastro,
    3: enviar_mail_expedienteConDeuda,
    4: enviar_mail_aInspeccionar,
    5: enviar_mail_aUrbanismo,
    6: enviar_mail_derechoConstruccionAPagar,
    7: enviar_mail_expedienteFinalizado,
}

# ------------------------------
# FUNCIÓN PRINCIPAL DE ENVIO
# ------------------------------
def enviarMailSegunEstado(idEstadoExpediente: Union[int, str], expediente: ExpedienteModel,background_tasks: BackgroundTasks):
    try:
        idEstadoExpediente = int(idEstadoExpediente)

        funcion_mail = MAPA_MAILS.get(idEstadoExpediente)

        if not funcion_mail:
            return {
                "ok": False,
                "mensaje": f"Estado no válido"  #esto no deberia pasar xq el estado se selecciona desde una tabla parametrizada, pero....puede ser que se elimine alguno manualmente y salte error
            }

        destinatarios = obtener_destinatarios(expediente)
        
        enviados = 0
     
        for email in destinatarios:
            if not es_email_valido(email):
                continue

            background_tasks.add_task(funcion_mail, email, expediente)
            enviados += 1


        if enviados == 0:
            return {
                "ok": False,
                "mensaje": "No se pudo enviar el mail (emails inválidos), verifique las direcciones de emails de los destinatarios."
            }

        return {
                    "ok": True,
                    "mensaje": "Mail fue enviado correctamente"
                }
    
    except Exception as e:
        return {
            "ok": False,
            "mensaje": f"Error al enviar mail: {str(e)}"
        }