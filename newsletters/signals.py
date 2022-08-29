
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.template.loader import render_to_string
from newsletters.models import NewsLetter, ScheduleMail
from newsletters.tasks import send_async_mail
from newsletters.models import (
    generate_unsub_url,
    encrypt_email
)



@receiver(post_save, sender = NewsLetter)
def send_configuration_mail(sender, instance, **kwargs):
    message = render_to_string(
        'frontend/partials/_subscribe_email.txt',
        {
            "subscriber":instance.subscriber,
        }
    )
    send_async_mail.delay(
        subject= f"ممنون برای اشتراک گذاری",
        emails = [instance.subscriber],
        text_msg = "ممنون برای پیوستن به ما",
        html_msg = message
    )




@receiver(post_delete, sender = NewsLetter)
def send_unsubscribe_mail(sender, instance, **kwargs):
    unsub_url = generate_unsub_url(encrypt_email(instance.subscriber))
    NewsLetter.objects.filter(subscriber = instance.subscriber).delete()
    message = render_to_string(
        'frontend/partials/_unsubscribe.html',
         {
            "subscriber":instance.subscriber,
            "unsubscrib_url":unsub_url
         }
    )
    send_async_mail.delay(
        subject= f"ما دلمان برایت تنگ خواهد شد",
        emails = [instance.subscriber],
        text_msg = "ما رو فراموش نکن",
        html_msg = message
    )




@receiver(post_save, sender = ScheduleMail)
def send_configuration_mail(sender, instance,  **kwargs):
    newsletters = NewsLetter.objects.filter(status = 1)
    for newsletter in newsletters:
        unsub_url = generate_unsub_url(encrypt_email(newsletter.subscriber))
        message = render_to_string(
            'frontend/partials/_schedule_email.html',
            {
                "subscriber":newsletter.subscriber,
                "subject":instance.subject,
                "content":instance.content,
                "unsubscrib_url":unsub_url
            }
        )
    
        send_async_mail.delay(
            subject= f"اطلاعیه از دپارتمان بیمه هوشمند",
            emails = [newsletter.subscriber],
            text_msg = "از اعتماد شما سپاسگذاریم",
            html_msg = message
        )
  
