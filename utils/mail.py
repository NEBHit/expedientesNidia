import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_mail(destinatario: str, asunto: str, mensaje: str):
    remitente = "nidia@9deJulio.gov.ar"
    password = "gdfgdfgdfg"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(mensaje, "plain"))

    try:
        with smtplib.SMTP("smtp.9dejulio.gov.ar", 587) as server:
            server.starttls()
            server.login(remitente, password)
            server.send_message(msg)
        print(f"✅ Correo enviado a {destinatario}")
    except Exception as e:
        print(f"⚠️ Error al enviar correo: {e}")