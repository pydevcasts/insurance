


from django.db.models.signals import post_save
from django.dispatch import receiver

from renewal.models import Renewal
from renewal.tasks import my_renewal_task_insurance


@receiver(post_save, sender=Renewal)
def send_new_renewal_notification_email(sender, instance, created, **kwargs):

    if created:
        name = instance.name if instance.name else "بدون نام"
        code = instance.code if instance.code else "کد بیمه گذار وارد نشده"
        phone = instance.phone if instance.phone else 'تلفن ندارد'

        subject = 'نام: {0}, کد بیمه گذار: {1}, شماره تلفن : {2}'.format(name, code, phone)
        message = f'شما یه درخواست از بیمه گذار به نام {name} \n' 
        message +=  ' و ' +'\n'  +  f'کد بیمه گذار: {code} \n' \
                  ' و ' + '\n' + f' شماره تلفن: {phone}' + '\n'
        message += '--' * 10
    
        my_renewal_task_insurance.delay(
        subject= subject,
        emails = ("siyamak1981@gmail.com",),
        text_msg = "ممنون برای پیوستن به ما",
        html_msg = message
        )