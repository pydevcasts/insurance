
import uuid
from django.db import models
from django.conf import settings
from django.urls.base import reverse
from blog.models import Comment
from painless.models.managers import NewManager
from painless.models.mixins import OrganizedMixin
from tag.models import Tag
from category.models import Category
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType



class New(OrganizedMixin):
    uid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'users', on_delete = models.CASCADE, verbose_name=_("نویسنده"))
    summary = models.CharField(_("خلاصه"), max_length = 128)
    banner = models.ImageField(_("آپلود"), upload_to = 'news/%Y/%m/%d', null = True, blank = True)
    category = models.ForeignKey(Category, related_name = 'news',verbose_name=_("دسته بندی"), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name = 'tags_new',  blank = True,verbose_name=_("برچسب"))
    views= models.IntegerField(_("بازدید"), default=0)
    content = RichTextField(_("پیام"), blank=True,null=True)
    comments = GenericRelation(Comment)

    objects = NewManager()

    class Meta:
        ordering = ['-published_at', 'title']
        verbose_name = _('خبر')
        verbose_name_plural = _('خبرها')
        get_latest_by = ['-published_at']


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('new:detail_news',
                       args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day, 
                             self.slug])


    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type