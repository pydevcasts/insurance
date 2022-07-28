from django.contrib import admin
from . models import  Attachment, Ticket,  FollowUp
from painless.models.actions import PostableMixin
from painless.models.actions import ExportMixin
from . import models


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
                    'assigned_to',
                    'status',
                    'created',
                    'updated',)
    inlines = [AttachmentInline]
    list_editable = ['status']
    list_filter = ['assigned_to']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
 


@admin.register(models.FollowUp)
class FollowUpAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ['title', 'user', 'ticket']
    list_filter = ['ticket']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
 

@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin, ExportMixin):
    list_display = ['ticket', 'file', 'filename', 'user', 'created']
    list_filter = ['ticket']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']

    
# @admin.register(models.Department)
# class DepartmentAdmin(admin.ModelAdmin, ExportMixin):
#     list_display = ['title']
#     list_filter = ['title']
#     actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']



