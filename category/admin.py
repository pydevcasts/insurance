from django.contrib import admin
from . import models
from khayyam import JalaliDate as jd



class SubCategoryInline(admin.StackedInline):
    model = models.SubCategory
    fields = [
        ('title','status', 'banner'),
        'content',
    
    ]

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']
    inlines = [SubCategoryInline]
    list_filter = ['title',]
    fields = [
        ('title','status', ),
        ('banner'),
        ('content',)
    
    ]
    def created_at(self, obj):
        return jd(obj.created)
    
    def updated_at(self, obj):
        return jd(obj.updated)