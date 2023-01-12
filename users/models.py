from painless.models.mixins import TimeStampedMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.contrib.auth import get_user_model
from painless.models.validations import validate_postal_code,validate_national_code
User = get_user_model()




class Profile(TimeStampedMixin):
  
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE ,verbose_name = _('User'))
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d", verbose_name = _('آپلود فایل'), null=True, blank=True)
    birthday = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    code = models.CharField(_('کد ملی'),validators=[validate_national_code], blank=True, null = True, max_length= 20)
    phone = models.IntegerField(_(' تلفن ثابت'), null=True, blank=True)
    address = models.CharField(_(' آدرس'),max_length=255, null=True, blank=True)
    zip = models.CharField(_('کد پستی'),max_length=30, null=True, blank=True,validators=[validate_postal_code])
    instagram = models.URLField(_("اینستاگرام"), blank = True, null = True)
    whatsapp = models.URLField(_("واتس آپ"), blank = True, null = True)
    linkedin = models.URLField(_("لینکدین"), blank = True, null = True)
    about = models.TextField(_('درباره خود بنویسید'),null = True, blank = True)


    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل')

    def __str__(self):
        return "siyamak"

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('../static/assets/backend/img/team/profile-picture-1.jpg')

