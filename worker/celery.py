import json
import smtplib
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import redis
from app.settings import Settings
from app.timer.repository import TimerRepository
from app.infrastructure.database.accessor import get_db_session
from celery import Celery
from celery.contrib.abortable import AbortableTask

settings = Settings()


celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = 'redis://cache:6379'

redis_client = redis.Redis(host='cache', port=6379)


@celery.task(bind=True, name='run_pomodoro_timer')
def run_pomodoro_timer_task(self, timer_id: str):
    while True:
        state_json = redis_client.get(timer_id)
        if not state_json:
            break

        state = json.loads(state_json)

        if not state.get("is_running", False):
            time.sleep(1)
            continue

        current_duration = state["work_duration"] if state["session_type"] == "work" else state["break_duration"]
        elapsed = time.time() - state["start_time"]
        remaining = current_duration - elapsed
        state["time_left"] = max(0, int(remaining))

        if remaining <= 0:
            if state["session_type"] == "work":
                state["pomodoro_count"] -= 1
                if state["pomodoro_count"] <= 0:
                    redis_client.delete(timer_id)
                    id_task = str(self.request.id)
                    celery.control.revoke(id_task, terminate=True)

                    break
                else:
                    state["session_type"] = "break"
                    state["time_left"] = state["break_duration"]
            else:
                state["session_type"] = "work"
                state["time_left"] = state["work_duration"]

            state["start_time"] = time.time()

        redis_client.set(timer_id, json.dumps(state))
        time.sleep(1)


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
