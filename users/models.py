from painless.models.mixins import TimeStampedMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(TimeStampedMixin):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE ,verbose_name = _('User'))
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d", verbose_name = _('آپلود فایل'), null=True, blank=True)
    birthday = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    gender = models.PositiveSmallIntegerField(_('جنسیت'),choices=GENDER_CHOICES, null=True, blank=True, default=1)
    phone = models.CharField(_(' تلفن ثابت'),max_length=12, null=True, blank=True)
    address = models.CharField(_(' آدرس'),max_length=255, null=True, blank=True)
    city = models.CharField(_('شهر'),max_length=50, null=True, blank=True)
    zip = models.CharField(_('کد پستی'),max_length=30, null=True, blank=True)
    instagram = models.URLField(_("اینستاگرام"), blank = True, null = True)
    whatsapp = models.URLField(_("واتس آپ"), blank = True, null = True)
    linkedin = models.URLField(_("لینکدین"), blank = True, null = True)
    about = models.TextField(_('درباره خود بنویسید'),null = True, blank = True)


    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('../static/assets/backend/img/team/profile-picture-1.jpg')

    def __str__(self):
        return f'({self.city})'

