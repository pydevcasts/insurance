import json

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from khayyam import JalaliDate as jd


class BroadcastNotification(models.Model):
    message = models.TextField(_("پیام"))
    published_at = models.DateTimeField(_("تاریخ انتشار"),default=timezone.now)
    sent = models.BooleanField(_("وضعیت انتشار"),default=False)

    def __str__(self):
        return f"{self.message}"
        
    class Meta:
        ordering = ['-published_at']
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشنها"

    @property
    def published(self):
        return jd(self.published_at)   

@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=instance.published_at.minute,
            hour=instance.published_at.hour,
            day_of_week="*",
            day_of_month=instance.published_at.day,
            month_of_year=instance.published_at.month,
        )

        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="broadcast-notification-" + str(instance.id),
            task="notifications.tasks.broadcast_notification",
            args=json.dumps((instance.id,)),
        )

    # if not created:
