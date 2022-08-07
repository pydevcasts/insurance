
from operator import length_hint
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from painless.models.mixins import OrganizedMixin, TimeStampedMixin
from ckeditor.fields import RichTextField
from django.core.validators import validate_email
from painless.models.validations import validate_charachters,validate_phone_number



class FAQ(TimeStampedMixin):
  
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(_("نام"),max_length = 128, validators = [validate_charachters])
    email = models.EmailField(_("ایمیل"),max_length = 128, validators = [validate_email])
    subject = models.CharField(_("موضوع"),max_length = 128)
    phone = models.CharField(_('تلفن'),max_length = 128, validators = [validate_phone_number])
    content = models.TextField(_("پیام"))
  

    objects = models.Manager()

    class Meta:
        ordering = ['subject']
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQ')
        get_latest_by = ['-created']

    def __str__(self):
        return self.subject



class Question(OrganizedMixin):
    slug = None
    class Meta:
        ordering = ['-created']
        verbose_name = _('سوال')
        verbose_name_plural = _('سوالها')
      
    def __str__(self):
        return self.title[:10]



class Answer(OrganizedMixin):
    slug = None
    title = None
    answer = RichTextField(_('پیام'), blank=True,null=True)
    banner = models.ImageField(_('آپلود فایل'),upload_to = 'answer/%Y/%m/%d', null = True, blank = True)
    alt = models.CharField(_('توضیح عکس'),max_length = 50, blank = True, null = True, default = "insurance")
    question = models.OneToOneField('Question', on_delete=models.CASCADE, related_name='question')
    
    class Meta:
        ordering = ['-created']
        verbose_name = _('پاسخ')
        verbose_name_plural = _('پاسخ')
      
    def __str__(self):
        return self.answer[:10]

