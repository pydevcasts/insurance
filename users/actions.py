from django.utils.translation import gettext_lazy as _


def make_active(modeladmin, request, queryset):
    queryset.update(is_active = True)


def make_deactive(modeladmin, request, queryset):
    queryset.update(is_active = False)


make_active.short_description = _('کاربر فعال شده')
make_deactive.short_description = _('کاربر غیر فعال شده')