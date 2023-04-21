from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.managers import PostPublishedManager
from painless.models.mixins import OrganizedMixin
from painless.models.validations import (validate_file_extension,
                                         validate_file_size)


class About(OrganizedMixin):
    summary = models.CharField(_('خلاصه'),max_length = 128)
    banner = models.ImageField(upload_to = 'about/%Y/%m/%d', null = True, blank = True, validators=[validate_file_extension, validate_file_size])
    content = RichTextField(_('پیام'),blank=True,null=True)
    
    objects = models.Manager()
    condition = PostPublishedManager()

    class Meta:
        verbose_name = _('درباره ما ')
        verbose_name_plural = _('درباره ما')
     

    def __str__(self):
        return self.title

    
    