import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    subject = models.CharField(_("subject"),max_length = 128)
    email = models.EmailField(_('email'),max_length = 128)
    content = models.TextField(_("content"))
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created', 'subject']
        verbose_name = _('تماس')
        verbose_name_plural = _('تماسها')
        get_latest_by = ['-created']

    def __str__(self):
        return self.subject




class Location(models.Model):
    address = models.CharField(_('آدرس'),max_length=200, null = True)
    date = models.DateTimeField(auto_now_add = True)
    class Meta:
        verbose_name = _('نقشه')
        verbose_name_plural = _('نقشه')

    def __str__(self):
        return self.address