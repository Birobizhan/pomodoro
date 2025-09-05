from dataclasses import dataclass
from worker.celery import send_email_task
from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    @staticmethod
    async def send_welcome_email(to: str) -> int:
        """Метод для отправки уведомления на почту"""
        task_id = send_email_task.delay(f'Welcome email', f'Welcome to pomodoro-timer service!', to)
        return task_id
