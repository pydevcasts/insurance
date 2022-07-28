from django.core.mail import send_mail
from insurance.settings import EMAIL_HOST_USER

def send_mail_to(subject, content, receivers):
    send_mail(subject,content,EMAIL_HOST_USER,[receivers], fail_silently= False)