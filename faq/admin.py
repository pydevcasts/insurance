from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from khayyam import JalaliDate as jd

from faq.models import FAQ, Answer, Question
from painless.models.actions import ExportMixin, PostableMixin


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    list_display = ['name','email', 'published']
    list_filter = ['name', 'email']
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
  
    fieldsets = [
        ('main', { 
            'fields': ( 
                    ('name','email',), 
                    ('subject', 'phone'),
                    ('content')
                ),
            }
        ),

    ]

    search_fields = ('name',)
    ordering = ('name',)

    def published(self, obj):
        return jd(obj.published_at)

    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_delete_permission(request)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('published_at',)
        return []


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))



class AnswerInline(admin.StackedInline):
    
    model = Answer
    can_delete = False
    verbose_name_plural = 'General Answer'
    actions = ['make_published', 'make_draft', 'export_as_json', 'export_as_csv']
    fieldsets = [
         ('main', { 
            'fields': ( 
                    ('answer',), 
                    ('banner', 'status', ),
                    ('alt')
                ),
            }
        ),
    ]   
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin, PostableMixin, ExportMixin):
    fieldsets = (
        (None, {'fields': ( 
                    ('title',), 
                    ('status', ),
                ),
            }),
        
    )
   
    list_display = ['title', 'status', 'is_published', 'published']
    search_fields = ('title',)
   
    inlines = [AnswerInline]
    ordering = ('-created',)


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
