import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from painless.models.mixins import  TimeStampedMixin
from django.core.validators import validate_email






class NewsLetters(TimeStampedMixin):
  
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(_("ایمیل"),max_length = 128, validators = [validate_email])
    

    objects = models.Manager()

    class Meta:
        ordering = ['email']
        verbose_name = _('خبر نامه')
        verbose_name_plural = _('خبر نامه ها')


    def __str__(self):
        return self.email

