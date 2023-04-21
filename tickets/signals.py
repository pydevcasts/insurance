import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Attachment, Ticket


@receiver(post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)




