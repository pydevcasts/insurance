from django.contrib import admin
from . import models
from khayyam import JalaliDate as jd
from django.utils.html import format_html



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.banner:
            return format_html('<img src="{}" width="40" style="border-radius:50%;">'.format(object.banner.url))
    thumbnail.short_description = 'Category Picture'
    list_display = ['thumbnail','title', 'slug', 'parent','created_at', 'updated_at']
    list_filter = ['title',]
    fields = [
        ('title','status', 'parent'),
        ('banner'),
        ('content','icon')
    
    ]
    def created_at(self, obj):
        return jd(obj.created)
    
    def updated_at(self, obj):
        return jd(obj.updated)