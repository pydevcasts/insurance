from django.db import models
from painless.models.mixins import OrganizedMixin
from django.urls import reverse



class Category(OrganizedMixin):
    banner=models.ImageField(
        upload_to='category/%Y/%m/%d', blank=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('frontend:detail_by_subcategory_slug', kwargs={"slug": self.slug})



class SubCategory(OrganizedMixin):
    category=models.ForeignKey('Category',on_delete=models.CASCADE, related_name="subcats")
    banner=models.ImageField(
        upload_to='subcategory/%Y/%m/%d', blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('frontend:detail_by_subcategory_slug', kwargs={"slug": self.slug})