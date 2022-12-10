


from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(name='my_renewal_task_insurance')
def my_renewal_task_insurance(subject:str, emails:list, text_msg:str, html_msg:str):
    send_mail(
        subject = subject,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list=emails,
        message=text_msg,
        fail_silently=True,
        html_message=html_msg
    )
    return True

