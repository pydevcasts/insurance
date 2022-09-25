import os
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import New
from django.utils.text import slugify


@receiver(models.signals.post_delete, sender=New)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.banner:
        if os.path.isfile(instance.banner.path):
            os.remove(instance.banner.path)


@receiver(models.signals.pre_save, sender=New)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = New.objects.get(pk=instance.pk).banner
    except New.DoesNotExist:
        return False
    if not old_file:
        return
    new_file = instance.banner
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)





@receiver(pre_save,sender=New)
def create_post(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_uniqe_slug(instance)


def create_uniqe_slug(instance,newslug=None):
    if newslug is not None:
        slug=newslug
    else:
        slug=slugify(instance.title,allow_unicode=True)

    instanClass=instance.__class__
    qs=instanClass.objects.filter(slug=slug)

    if qs.exists():
        newslug=f"{slug}-{qs.first().id}"
        return create_uniqe_slug(instance,newslug)

    return slug
   