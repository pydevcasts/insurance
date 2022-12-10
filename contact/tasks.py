from logging import Logger
from celery.app import shared_task
from insurance.settings import EMAIL_HOST_USER
from .mail import send_mail_to
from time import sleep



@shared_task(name='my_first_task')
def my_first_task(duration):
    # Logger.info(f"from={EMAIL_HOST_USER}, {receivers=}, {subject=}, {content=}")
    subject= 'Celery'
    content= 'یک پیام دریافت کرده اید'
    receivers= 'siyamak1981@gmail.com'
    is_task_completed= False
    error=''

    try:
        sleep(duration)
        is_task_completed= True

    except Exception as err:
        error= str(err)
        Logger.error(error)
        
    if is_task_completed:
        send_mail_to(subject,content,receivers)
    else:
        send_mail_to(subject,error,receivers)
    return('first_task_done')