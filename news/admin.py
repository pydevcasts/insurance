from django.contrib import admin
from django.utils.html import format_html
from khayyam import JalaliDate as jd

from painless.models.actions import ExportMixin, PostableMixin

from . import models


@admin.register(models.New)
class NewAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    def thumbnail(self, object):
        if object.banner:
            return format_html('<img src="{}" width="40" style="border-radius:50%;">'.format(object.banner.url))

    thumbnail.short_description = 'Category Picture'
    list_display = ['thumbnail','title', 'slug', 'is_published', 'published','views', 'category', 'get_tags']
    filter_horizontal = ['tags',]
    list_editable = ['category',]
    list_filter = ['status', 'published_at', 'category__title']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('title',), 
                    ('author', 'status', ),
                    ('category','views')
                ),
            }
        ),

        ('Advanced_options', { 
            'fields': (
                    'tags',
                    'banner',
                    'summary',
                    'content',
                    'published_at',
                ),
            'classes': ('collapse',)
            },

        ),
    ]

    def published(self, obj):
        return jd(obj.published_at)

    def get_tags(self, obj):
        return ", ".join([t.title for t in obj.tags.all()])
        

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


