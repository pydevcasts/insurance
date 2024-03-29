from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.managers import PostPublishedManager
from painless.models.mixins import OrganizedMixin


class Slider(OrganizedMixin):
    summary = models.CharField(_('خلاصه'),max_length = 128)
    content = RichTextField(_('پیام'),blank=True,null=True)
    
    condition = PostPublishedManager()

    class Meta:
        verbose_name = _('اسلایدر')
        verbose_name_plural = _('اسلایدر')
     

    def __str__(self):
        return self.title

    
    