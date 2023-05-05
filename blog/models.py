import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from category.models import Category
from comment.models import Comment
from insurance.settings import CACHE_TTL
from painless.models.managers import PostPublishedManager
from painless.models.mixins import OrganizedMixin
from tag.models import Tag
from django_redis import get_redis_connection
from accounts.models import IPAddress



class Post(OrganizedMixin):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '+', on_delete = models.CASCADE,verbose_name = _("نویسنده"))
    summary = models.CharField(_("خلاصه"), max_length = 128)
    banner = models.ImageField(_("تصویر"), upload_to = 'blog/%Y/%m/%d', null = True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name = 'posts',verbose_name = _("دسته بندی"))
    tags = models.ManyToManyField(Tag, related_name = 'tags',  blank = True, verbose_name = _("برچسب"))
    content = RichTextField(_("پیام"), blank=True,null=True)
    comments = GenericRelation(Comment)
    viewers = models.PositiveIntegerField(default=0)
    objects = PostPublishedManager()

    class Meta:
        ordering = ['-published_at', 'title']
        verbose_name = _('پست')
        verbose_name_plural = _('پستها')
        get_latest_by = ['-published_at']
    

    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse("blog:detail", args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day, 
                             self.slug])
    
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
        
    
    def get_view_count(self):
        # Get Redis connection
        r = get_redis_connection()

        # Check if post view count is in cache
        key = f"post:{self.uid}:views"
        if r.exists(key):
            # If yes, return view count from cache
            viewers = int(r.get(key))
            print(viewers,'cache view ............')
        else:
            # If not, get view count from database
            viewers = self.viewers
            print(viewers, 'db view...........')

            # Set view count in cache
            r.setex(key, CACHE_TTL, viewers)
            print(r, 'chache db................')

        return viewers

    def increase_view_count(self):
        # Get Redis connection
        r = get_redis_connection()

        # Increase view count in cache
        key = f"post:{self.uid}:views"
        r.incr(key)
        
        # Increase view count in database
        self.viewers += 1
        self.save()