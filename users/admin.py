import admin_thumbnails
from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .actions import make_active, make_deactive
from .models import Profile, User


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


@admin_thumbnails.thumbnail('avatar')
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'General Profile'
    fk_name = 'user'
    
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
    fieldsets = [
        ('I. تلفن -آدرس', {
            'fields': ['phone', 'address'],
            'classes': ['collapse']
        }),
        ('II. کد ملی-تاریخ تولد-درباره', {
            'fields':[ 'code', 'birthday'],
            'classes': ['collapse']
        }),
        ('III. عکس -کد پستی', {
            'fields': ['avatar', 'zip'],
            'classes': ['collapse']
        }),
        ('IV. شبکه اجتماعی', {
            'fields': ['linkedin', 'instagram', 'whatsapp'],
            'classes': ['collapse']
        }),
         ('V. درباره خودتان ', {
            'fields': ['about'],
            'classes': ['collapse']
        })
    ]   





@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('mobile', 'first_name', 'last_name', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'mobile', 'last_name')

    inlines = (
        ProfileInline,
    )
    
    actions = [make_active, make_deactive]
    ordering = ('email',)


