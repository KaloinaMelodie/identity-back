from celery import Celery
from email_service import EmailService

celery_app = Celery("tasks", broker="redis://redis:6379/0")

@celery_app.task
def send_contact_email_task(email, name, content):
    EmailService.send_contact_email(email, name, content)
