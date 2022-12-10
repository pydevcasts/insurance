import uuid
from django.db import models
from painless.models.mixins import TimeStampedMixin
from category.models import Category
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from painless.models.validations import validate_phone_number



class Renewal(TimeStampedMixin):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(_("نام بیمه گذار"), max_length=64, blank = True, null = True)
    phone = models.CharField(_('تلفن'),max_length = 128, validators = [validate_phone_number])
    code = models.CharField(_('کد رهگیری'),max_length = 128, blank = True, null = True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name = 'cats')
   

    objects = models.Manager()
 

    class Meta:
        ordering = ['-published_at', 'name']
        verbose_name = _('تمدید')
        verbose_name_plural = _('تمدیدی')
        get_latest_by = ['-published_at']

    def __str__(self):
        return self.name

    
    