from django.contrib import admin
from . import models
from khayyam import JalaliDate as jd



@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email', 'created_at']
    list_filter = ['created',]
    search_fields = ['subject']
    date_hierarchy = 'created'
    empty_value_display = '--empty--'
    
    def created_at(self, obj):
        return jd(obj.created)



@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address','date']
    list_filter = ['address',]
