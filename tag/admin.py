from django.contrib import admin
from . import models
from khayyam import JalaliDate as jd



@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']
    list_filter = ['created',]
    search_fields = ['title']
    date_hierarchy = 'created'
    empty_value_display = '--empty--'
    fields = [
        ('title','status', ),
       
    
    ]
    def created_at(self, obj):
        return jd(obj.created)
    
    def updated_at(self, obj):
        return jd(obj.updated)

