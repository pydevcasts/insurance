import uuid
from django.db import models
from django.conf import settings
from django.urls.base import reverse
from painless.models.mixins import OrganizedMixin
from painless.models.managers import PostPublishedManager
from tag.models import Tag
from category.models import SubCategory
from painless.models.choices import PostStatus
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

status = PostStatus(is_charfield = False)

class Post(OrganizedMixin):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'posts', on_delete = models.CASCADE)
    summary = models.CharField(max_length = 128)
    banner = models.ImageField(upload_to = 'blog/%Y/%m/%d', null = True, blank = True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, related_name = 'posts')
    tag = models.ManyToManyField(Tag, related_name = 'post',  blank = True)
    content = RichTextField(blank=True,null=True)

    objects = models.Manager()
    condition = PostPublishedManager()

    class Meta:
        ordering = ['-published_at', 'title']
        verbose_name = _('پست')
        verbose_name_plural = _('پستها')
        get_latest_by = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    