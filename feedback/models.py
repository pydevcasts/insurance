from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.managers import PostPublishedManager
from painless.models.mixins import OrganizedMixin
from painless.models.validations import (validate_file_extension,
                                         validate_file_size)


class CustomerFeedback(OrganizedMixin):
    title = None
    slug = None
    first_name = models.CharField(_("نام"), max_length = 128)
    last_name = models.CharField(_("نام خانوادگی"), max_length = 128)
    role = models.CharField(_("سمت"), max_length = 128)
    banner = models.ImageField(_("تصویر"), upload_to = 'feedback/%Y/%m/%d', null = True, blank = True, validators=[validate_file_extension, validate_file_size])
    content = RichTextField(_("پیام"), blank=True,null=True)

    objects = PostPublishedManager()

    class Meta:
        ordering = ['-published_at', 'first_name']
        verbose_name = _('فیدبک')
        verbose_name_plural = _('فیدبکها')
        get_latest_by = ['-published_at']
    
    
    def __str__(self):
        return self.first_name
        
    

