
from celery.app import shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.mail import send_mail

from insurance.celery import app
from newsletters.models import NewsLetter, ScheduleMail


@shared_task(name='Send_Mail')
def send_async_mail(subject:str, emails:list, text_msg:str, html_msg:str):
    send_mail(
        subject = subject,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list=emails,
        message=text_msg,
        fail_silently=True,
        html_message=html_msg
    )
    print("Email is :")
    return True



@shared_task(name = "send_schedule_mails")
def send_schedule_mails():
    mail = ScheduleMail.objects.all().first()
    send_mail(
        subject = mail.subject,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[_.email for _ in NewsLetter.objects.all()],
        message=mail.content,
        fail_silently=True,
        html_message=mail.html_msg

    )
    print("Running send chedule mail")


app.conf.CELERYBEAT_SCHEDULE = {

    'add-every-monday_morning': {
        'task': 'send_schedule_mails',
        'schedule': crontab(minute="*/1"),
        'args': (),
    },
}