import uuid
from django.db import models
from django.conf import settings
from django.urls.base import reverse
from comment.models import Comment
from painless.models.mixins import OrganizedMixin
from painless.models.managers import PostPublishedManager
from tag.models import Tag
from category.models import Category
from painless.models.choices import PostStatus
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType



status = PostStatus(is_charfield = False)



class Post(OrganizedMixin):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '+', on_delete = models.CASCADE,verbose_name = _("نویسنده"))
    summary = models.CharField(_("خلاصه"), max_length = 128)
    banner = models.ImageField(_("تصویر"), upload_to = 'blog/%Y/%m/%d', null = True, blank = True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name = 'posts',verbose_name = _("ساب کتگوری"))
    views= models.IntegerField(_("بازدید"), default=0)
    tags = models.ManyToManyField(Tag, related_name = 'tags',  blank = True, verbose_name = _("برچسب"))
    content = RichTextField(_("پیام"), blank=True,null=True)
    comments = GenericRelation(Comment)

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
    

    




