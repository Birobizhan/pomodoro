from dataclasses import dataclass
from worker.celery import send_email_task
from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    @staticmethod
    async def send_welcome_email(to: str):
        task_id = send_email_task.delay(f'welcome email', f'welcome to pomodoro', to)
        return task_id
