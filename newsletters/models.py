from logging import exception
import uuid
import markdown2
import jwt
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from painless.models.mixins import  OrganizedMixin, TimeStampedMixin
from django.core.validators import validate_email
from django.contrib.sites.models import Site



class NewsLetter(OrganizedMixin):
    title, slug = None, None
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    email = models.EmailField(_("ایمیل"),max_length = 128, unique = True, validators = [validate_email])
    

    objects = models.Manager()

    class Meta:
        ordering = ['email']
        verbose_name = _('خبر نامه')
        verbose_name_plural = _('خبر نامه ها')


    def __str__(self):
        return self.email


class ScheduleMail(TimeStampedMixin):
    subject = models.CharField(_('موضوع'), max_length=255, null = True, blank = True)
    content = models.TextField(_('پیام'), max_length=3000)

    class Meta:
        ordering = ['-created']
        verbose_name = "برنامه ایمیل"
        verbose_name_plural = "برنامه ایمیل"
    
    def __str__(self):
        return self.subject


    @property
    def html_content(self):
        markdown = markdown2.Markdown()
        return markdown.convert(self.content)


def encrypt_email(email: str)->str:
    encode_jwt = jwt.encode({'email':email}, settings.SECRET_KEY)
    return encode_jwt


def decrypt_email(token: str)->str:
    data = jwt.decode(
        token, settings.SECRET_KEY, 
        algorithms = ['HS256'],
        options = {"varify_exp":False},
    )
    
    return data['email']



def generate_unsub_url(token:str, https:bool=False)->str:
    
    try:
        site = Site.objects.get(name = "0.0.0.0:8000")
    except Site.DoesNotExist:
        raise Exception("Site does not exists")

    full_domain = f"http{'s' if https else ''}://{site.domain}"
    return f"{full_domain}/mail/newsletter/unsubscribe/{token}"
