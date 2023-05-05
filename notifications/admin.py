from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from painless.models.actions import ExportMixin, PostableMixin

from . import models


@admin.register(models.BroadcastNotification)
class BroadcastNotificationAdmin(ModelAdminJalaliMixin,admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['message','sent', 'published',]
    list_filter = ['published_at']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
    fieldsets = [
        ('main', { 
            'fields': ( 
                    'message',
                    'published_at',
                    'sent'
                ),
            }
        ),
    ]

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []



    def is_published(self, obj):
        published = 1
        return obj.sent == published