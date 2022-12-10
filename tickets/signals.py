import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from . models import Attachment



@receiver(post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)




