from pyexpat import model
from django.db import models
from django.conf import settings
from django.urls.base import reverse
from painless.models.mixins import OrganizedMixin
from painless.models.managers import PostPublishedManager
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Member(OrganizedMixin):
    title = None
    slug = None
    first_name = models.CharField(_("firt_name"), max_length=128, null = True, blank = True)
    last_name = models.CharField(_("last_name"), max_length=128, null = True, blank = True)
    phone = models.CharField(_("phone"), max_length=128, null = True, blank = True)
    banner = models.ImageField(upload_to = 'memnber/%Y/%m/%d', null = True, blank = True)
    instagram = models.URLField(_("instagram"), blank = True, null = True)
    whatsapp = models.URLField(_("whatsapp"), blank = True, null = True)
    linkedin = models.URLField(_("linkedin"), blank = True, null = True)
    content = RichTextField(_('content'),blank=True,null=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE, blank = True, null = True)
    
    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")
    def __str__(self) -> str:

        return f"name of member is:{self.first_name}-{self.last_name}"



class Team(OrganizedMixin):
    about = models.ForeignKey("About", on_delete=models.CASCADE, blank = True, null = True)
  
    class Meta:
        verbose_name = _('ُteam')
        verbose_name_plural = _('teams')
    
    def __str__(self):
        return self.title


class About(OrganizedMixin):
    subtitle = models.CharField(_('subtitle'), max_length= 128, blank = True, null = True)
    summary = models.CharField(_('summary'),max_length = 128)
    banner = models.ImageField(upload_to = 'about/%Y/%m/%d', null = True, blank = True)
    content = RichTextField(_('content'),blank=True,null=True)
    

    objects = models.Manager()
    condition = PostPublishedManager()

    class Meta:
        verbose_name = _('about us')
        verbose_name_plural = _('about us')
     

    def __str__(self):
        return self.title

    
    