from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from report_exchange import settings


@shared_task()
def send_feedback_email_task(a):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django


@shared_task()
def send_email(message, subject, email):
    response = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
    return response


@shared_task()
def schedule_send_email(message, subject, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
