from django.contrib import admin
from painless.models.actions import ExportMixin
from . import models
from khayyam import JalaliDate as jd

class AttachmentInline(admin.StackedInline):
    model = models.Attachment
    fields = [
        ('file','filename',),
    ]


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin, ExportMixin):
    list_display = (
                    'title',
                    'description',
                    'user',
                    'status', 
                    'created_at',
                    'updated_at',)
    inlines = [AttachmentInline]
    list_editable = ['status']
    list_filter = ['status']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
 

    def created_at(self, obj):
        return jd(obj.created)
    
    def updated_at(self, obj):
        return jd(obj.updated)


    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []





@admin.register(models.FollowUp)
class FollowUpAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ['title', 'ticket','created_at','user', 'published']
    list_filter = ['ticket']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
    fields = [
        ('title'),
         ('ticket'),
        ('description',)
    ]
  

    def created_at(self, obj):
        return jd(obj.created)
    
    def updated_at(self, obj):
        return jd(obj.updated)


    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []

        

@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ['ticket', 'file', 'filename',  'created']
    list_filter = ['ticket']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']

    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []


