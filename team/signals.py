import os

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from team.models import Member


@receiver(models.signals.post_delete, sender=Member)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.banner:
        if os.path.isfile(instance.banner.path):
            os.remove(instance.banner.path)


@receiver(models.signals.pre_save, sender=Member)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = Member.objects.get(pk=instance.pk).banner
    except Member.DoesNotExist:
        return False
    if not old_file:
        return
    new_file = instance.banner
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)