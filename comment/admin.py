from django.contrib import admin

from . import models


@admin.register(models.Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'content_type', 'user','published',)
    search_fields = ('content',)
    list_editable = ['content_type']
    list_filter = ['user', 'published_at']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']

    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []


 