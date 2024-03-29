from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDate as jd

from painless.models.actions import ExportMixin, PostableMixin
from slider.models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['title', 'status', 'is_published', 'published']
    list_filter = ['status', 'published_at']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('title','summary',), 
                    ('status'),
                    ('content')
                ),
            }
        ),

    ]

    search_fields = ('title',)
    ordering = ('title',)

    def published(self, obj):
        return jd(obj.published_at)


    def is_published(self, obj):
        published = 1
        return obj.status == published
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []

    is_published.boolean = True


