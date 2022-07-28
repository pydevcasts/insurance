from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .actions import make_active
from .actions import make_deactive
from .models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'General Profile'
    fk_name = 'user'
    
    
    fieldsets = [
        ('I. Personal Information', {
            'fields': ['number', 'phone', 'address'],
            'classes': ['collapse']
        }),
        ('II. Personal Information', {
            'fields':[ 'gender', 'birthday', 'about'],
            'classes': ['collapse']
        }),
        ('III. Personal Information', {
            'fields': ['avatar', 'zip'],
            'classes': ['collapse']
        })
    ]   





@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
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


