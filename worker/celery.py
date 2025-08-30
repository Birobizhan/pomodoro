import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import Settings
from celery import Celery

settings = Settings()

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = 'rpc://'


@celery.task(name='send_mail_task')
def send_email_task(subject: str, text: str, to: str) -> None:
    msg = _build_message(subject, text, to)
    _send_email(msg=msg)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg['from'] = settings.from_email
    msg['to'] = to
    msg['subject'] = subject
    msg.attach(MIMEText(text, 'plain'))
    return msg


def _send_email(msg: MIMEMultipart):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context)
    server.login(settings.from_email, settings.SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()