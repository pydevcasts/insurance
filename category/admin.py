from django.contrib import admin
from . import models
from khayyam import JalaliDate as jd



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent','created_at', 'updated_at']
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