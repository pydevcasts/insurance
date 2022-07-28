from painless.models.mixins import TimeStampedMixin
from django.db import models
from django.utils.translation import gettext as _
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
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True, default=1)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    about = models.TextField(null = True, blank = True, verbose_name = _('about'))


    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('../static/assets/backend/img/team/profile-picture-1.jpg')

    def __str__(self):
        return f'({self.city})'

