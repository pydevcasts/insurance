from django import template
import datetime, time
import khayyam
register = template.Library()



@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = ' is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = ' is-valid'
    return 'form-control{}'.format(css_class)



@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__





@register.filter
def jalali_date(date):
    """Converts Date into JalaliDate"""
    timestamp = time.mktime(datetime.datetime.timetuple(date))
    jalali_date = khayyam.JalaliDate.fromtimestamp(timestamp)
    return str(jalali_date)

register.filter('jalali_date', jalali_date)