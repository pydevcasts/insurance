# -*- coding: utf-8 -*-

from django.shortcuts import reverse,render
from django.db import models
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from painless.models.mixins import TimeStampedMixin
User = get_user_model()
from django.conf import settings
from ckeditor.fields import RichTextField



def user_unicode(self):
    """
    return 'last_name, first_name' for User by default
    """
    return u'%s, %s' % (self.last_name, self.first_name)


User.__unicode__ = user_unicode


class Ticket(TimeStampedMixin):

    STATUS_CHOICES = (
        ('TODO', 'مشاهده نشده'),
        ('IN PROGRESS', 'در حال انجام'),
        ('WAITING', 'در حال انتظار'),
        ('DONE', 'انجام شده'),
    )
    title = models.CharField(_("متن"), max_length=255)
    user = models.ForeignKey(User,
                              related_name='user',
                              blank=True,
                              null=True,
                              on_delete =
                              models.CASCADE, verbose_name = _("کاربر"))
    description = RichTextField(_('پیام'),blank=True,null=True)
    
    status = models.CharField(_("وضعیت"),
                              choices=STATUS_CHOICES,
                              max_length=255,
                              blank=True,
                              null=True)
   

    class Meta:
        ordering = ['-created']
        verbose_name = _("تیکت")
        verbose_name_plural = _("تیکت ها")


    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("tickets:ticket_detail", kwargs={"pk": self.pk })
     
  


class FollowUp(TimeStampedMixin):
    """
    A FollowUp is a comment to a ticket.
    """
    ticket      = models.ForeignKey(Ticket, on_delete = models.CASCADE, related_name="tickets", verbose_name = _("تیکت"))
    title       = models.CharField(_("متن"), max_length=200)
    description = RichTextField(_('پیام'),blank=True,null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,  on_delete = models.CASCADE, verbose_name = _("کاربر"))


    class Meta:
        ordering = ['-created', ]
        verbose_name = 'پاسخ'
        verbose_name_plural = 'پاسخ ها'
    
    def __str__(self):
        return self.title




class Attachment(TimeStampedMixin):
    ticket   = models.ForeignKey(Ticket, on_delete =models.CASCADE, related_name = "attachments", verbose_name = _("تیکت"))
    file     = models.FileField(_("فایل"), upload_to="tickets", max_length=1000)
    filename = models.CharField(_("نام فایل"), max_length=1000)
   


    def get_upload_to(self, field_attname):
        """ Get upload_to path specific to this item """
        if not self.id:
            return u''
        return u'../media/tickets/%s' % (
            self.ticket.id,
        )

    class Meta:
        ordering            = ['filename', ]
        verbose_name        = 'فایل ضمیمه'
        verbose_name_plural = 'فایل های ضمیمه'
