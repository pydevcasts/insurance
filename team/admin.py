from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDate as jd

from painless.models.actions import ExportMixin, PostableMixin
from team.models import Member, Team


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = _('Member')
    fk_name = 'team'
    
    
    fieldsets = [
        ('I. Personal Information', {
            'fields': ['first_name', 'last_name', 'phone'],
            'classes': ['collapse']
        }),
        ('II. Personal Information', {
            'fields':[ 'banner', 'content', 'status', 'role'],
            'classes': ['collapse']
        }),
         ('II. Personal Information', {
            'fields':[ 'instagram', 'whatsapp', 'linkedin'],
            'classes': ['collapse']
        }),
      
    ]   




  

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['title', 'is_published', 'published']
    list_filter = ['status', 'published_at']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('title','summary'), 
                    ('status', ),
                     ('content')
                ),
            }
        ),

    ]
    search_fields = ('title',)

    inlines = (
        MemberInline,
    )
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

