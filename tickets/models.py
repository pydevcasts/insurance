# -*- coding: utf-8 -*-
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


def user_unicode(self):
    """
    return 'last_name, first_name' for User by default
    """
    return u'%s, %s' % (self.last_name, self.first_name)


User.__unicode__ = user_unicode


class Ticket(models.Model):

    title = models.CharField('Title', max_length=255)

    owner = models.ForeignKey(User,
                              related_name='owner',
                              blank=True,
                              null=True,
                              verbose_name='Owner', on_delete =
                              models.CASCADE)

    description = models.TextField('Description', blank=True, null=True)

    STATUS_CHOICES = (
        ('TODO', 'TODO'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('WAITING', 'WAITING'),
        ('DONE', 'DONE'),
    )
    status = models.CharField('Status',
                              choices=STATUS_CHOICES,
                              max_length=255,
                              blank=True,
                              null=True)

    waiting_for = models.ForeignKey(User,
                                    related_name='waiting_for',
                                    blank=True,
                                    null=True,
                                    verbose_name='Waiting For' ,on_delete =
                              models.CASCADE)

    # set in view when status changed to "DONE"
    closed_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(User,
                                    related_name='assigned_to',
                                    blank=True,
                                    null=True,
                                    verbose_name='Assigned to', on_delete =
                              models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', ]


    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("tickets:ticket_detail", kwargs={"pk": self.pk })
     


class FollowUp(models.Model):
    """
    A FollowUp is a comment to a ticket.
    """
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', on_delete =
                              models.CASCADE, related_name="tickets")
    date = models.DateTimeField('Date', default=timezone.now)
    title = models.CharField('Title', max_length=200,)
    text = models.TextField('Text', blank=True, null=True,)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='User', on_delete =
                              models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified', ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return self.title


def attachment_path(instance, filename):
    """
    Provide a file path that will help prevent files being overwritten, by
    putting attachments in a folder off attachments for ticket/followup_id/.
    """
    import os
    from django.conf import settings
    os.umask(0)
    path = 'tickets/%s' % instance.ticket.id
    print(path)
    att_path = os.path.join(settings.MEDIA_ROOT, path)
    if settings.DEFAULT_FILE_STORAGE == "django.core.files. \
                                         storage.FileSystemStorage":
        if not os.path.exists(att_path):
            os.makedirs(att_path,)
    return os.path.join(path, filename)


class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', on_delete =
                              models.CASCADE)

    file = models.FileField('File',
                            upload_to=attachment_path,
                            max_length=1000)

    filename = models.CharField('Filename', max_length=1000)

    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             verbose_name='User', on_delete = models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    def get_upload_to(self, field_attname):
        """ Get upload_to path specific to this item """
        if not self.id:
            return u''
        return u'../media/tickets/%s' % (
            self.ticket.id,
        )

    class Meta:
        ordering = ['filename', ]
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
