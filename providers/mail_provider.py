from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dependencies.config import Settings


async def send_challenge_answer_results(
  email: str,
  answer_content: str,
  settings: Settings
):
  body = {
    "answer_content": answer_content
  }
  
  message = MessageSchema(
    subject="Tus respuestas al reto Beevify",
    recipients=[email],
    template_body=body,
    subtype=MessageType.html,
    headers={"Priority": "High"}
  )

  mail_config = _get_connection_config(settings)
  fm = FastMail(mail_config)
  print("Sending email to ", email)
  await fm.send_message(message, template_name="email_results_template.html")


def _get_connection_config(settings: Settings):
  return ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_FROM_NAME= "Docu-Menta Info",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(__file__).parent.parent / "templates" / "email",
  )