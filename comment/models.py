from django.conf import settings
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.managers import CommentManager
from painless.models.mixins import TimeStampedMixin


class Comment(TimeStampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(_('پیام'), max_length=3000)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.CharField(null=True, blank=True, max_length=228)
    content_object = GenericForeignKey('content_type','object_id')
    comments = GenericRelation('self',related_query_name='reply')
 
  
    objects = CommentManager()

    def __str__(self):
        return "Comment for {}".format(self.content_type)
    

    class Meta:
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنتها')
        get_latest_by = ['-published_at']

