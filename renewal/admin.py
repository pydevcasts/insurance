from django.contrib import admin
from . import models
from painless.models.actions import PostableMixin,ExportMixin
from khayyam import JalaliDate as jd




@admin.register(models.Renewal)
class RenewalAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['name', 'category','phone','code', 'published', ]
    list_editable = ['category']

    list_filter = ['published_at', 'category']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('name',), 
                    ('phone', 'code', ),
                    'category',
                ),
            }
        ),

    ]

    def published(self, obj):
        return jd(obj.published_at)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []





