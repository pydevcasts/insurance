from django.contrib import admin
from newsletters.models import NewsLetters
from painless.models.actions import PostableMixin,ExportMixin
from khayyam import JalaliDate as jd
from django.utils.translation import gettext_lazy as _




@admin.register(NewsLetters)
class FAQAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['email', 'published']
    list_filter = ['email']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('email',), 
                ),
            }
        ),

    ]

    search_fields = ('email',)
    ordering = ('email',)

    def published(self, obj):
        return jd(obj.published_at)

    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []


