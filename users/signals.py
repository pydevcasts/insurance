
import os
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()




@receiver(models.signals.post_delete, sender=Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    if not old_file:
        return
    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):    
    if created:
        Profile.objects.create(user=instance)
    

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html