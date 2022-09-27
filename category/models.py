from django.db import models
from painless.models.mixins import OrganizedMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField



class Category(OrganizedMixin):
    icon = models.CharField(_("ایکن"), max_length=128, blank = True, null = True)
    banner=models.ImageField(_('تصویر'),
        upload_to='category/%Y/%m/%d', blank=True)
    content = RichTextField(_('پیام'),blank=True,null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندیها'
    
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # print("slug is:",self.subcats.subcategory.slug)
        return reverse('frontend:detail_by_subcategory_slug', kwargs={"slug": self.slug})



class SubCategory(OrganizedMixin):
    category=models.ForeignKey('Category',on_delete=models.CASCADE, related_name="subcats")
    banner=models.ImageField(_('تصویر'),
        upload_to='subcategory/%Y/%m/%d', blank=True)
    content = RichTextField(_('پیام'),blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('frontend:detail_by_subcategory_slug', kwargs={"slug": self.slug})