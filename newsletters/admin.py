from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDate as jd

from newsletters.models import NewsLetter, ScheduleMail
from painless.models.actions import ExportMixin, PostableMixin


@admin.register(NewsLetter)
class NewsLetterdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['subscriber', 'published', 'status']
    list_filter = ['subscriber']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('subscriber','status'), 
                ),
            }
        ),

    ]

    search_fields = ('subscriber',)
    ordering = ('subscriber',)

    def published(self, obj):
        return jd(obj.published_at)

    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []


admin.site.register(ScheduleMail)