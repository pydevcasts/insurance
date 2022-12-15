from django.db import models
from painless.models.mixins import OrganizedMixin
from painless.models.managers import PostPublishedManager
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

from painless.models.validations import validate_file_extension, validate_file_size


class Member(OrganizedMixin):
    title = None
    slug = None
    first_name = models.CharField(_("نام"), max_length=128, null = True, blank = True)
    last_name = models.CharField(_("نام خانوادگی"), max_length=128, null = True, blank = True)
    role = models.CharField(_("سمت"), max_length=128, null = True, blank = True)
    phone = models.CharField(_("تلفن"), max_length=128, null = True, blank = True)
    banner = models.ImageField(upload_to = 'memnber/%Y/%m/%d', null = True, blank = True, validators=[validate_file_extension, validate_file_size])
    instagram = models.URLField(_("اینستاگرام"), blank = True, null = True)
    whatsapp = models.URLField(_("واتس آپ"), blank = True, null = True)
    linkedin = models.URLField(_("لینکدین"), blank = True, null = True)
    content = RichTextField(_('پیام'),blank=True,null=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, blank = True, null = True, related_name="team")
    
    class Meta:
        verbose_name = _("عضو")
        verbose_name_plural = _("اعضاًٰٰ‌")
    def __str__(self) -> str:

        return f"نام عضو:{self.first_name}-{self.last_name}"



class Team(OrganizedMixin):
    slug = None
    summary = models.CharField(_('خلاصه'),max_length = 128)
    content = RichTextField(_('پیام'),blank=True,null=True)
  
    class Meta:
        verbose_name = _('تیم')
        verbose_name_plural = _('تیم ما')
    
    def __str__(self):
        return self.title