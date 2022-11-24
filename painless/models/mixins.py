from django.db import models
from painless.models.choices import PostStatus
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDate as jd

status = PostStatus(is_charfield=False)


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("تاریخ ایجاد"),auto_now_add=True)
    updated = models.DateTimeField(_("تاریخ ویرایش"),auto_now=True)
    published_at = models.DateTimeField(_("تاریخ انتشار"),default=timezone.now)
    
    class Meta:
        abstract = True
    
    @property
    def published(self):
        return jd(self.published_at)



class OrganizedMixin(TimeStampedMixin):
    title = models.CharField(_("متن"),
        max_length=128, unique_for_month='published_at', help_text='متن منحصر به فرد باید باشد')
    slug = models.CharField(_("اسلاگ"),max_length=128, unique_for_month='published_at',)
    status = models.PositiveSmallIntegerField(_("وضعیت"),
        choices=status.get_status(), default=status.PUBLISHED)

    class Meta:
        abstract = True
    
    def is_published(self):
        return self.status 
    is_published.boolean = True
