from django.db import models
from painless.models.mixins import OrganizedMixin
from painless.models.managers import PostPublishedManager
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _



class Slider(OrganizedMixin):
    summary = models.CharField(_('خلاصه'),max_length = 128)
    content = RichTextField(_('پیام'),blank=True,null=True)
    
    objects = models.Manager()
    condition = PostPublishedManager()

    class Meta:
        verbose_name = _('اسلایدر')
        verbose_name_plural = _('اسلایدر')
     

    def __str__(self):
        return self.title

    
    