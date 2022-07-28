import re
import string
from django import forms

def validate_charachters(value):
    letters = set(string.punctuation)
    digits = set(string.digits)
    v = set(value)
    if not v.isdisjoint(letters) or not v.isdisjoint(digits):
        raise forms.ValidationError('نام تنها باید از کاراکتر تشکیل شده باشد.')


def validate_phone_number(value):
    pattern = r'^(09)[1-3][0-9]\d{7}$'
    if not re.match(pattern, value):
        raise forms.ValidationError('شماره صحیح وارد نشده است.')

def validate_national_code(value):
    if not len(value) == 10:
        raise forms.ValidationError('کد ملی معتبر نیست')
    positions = [i for i in range(1, 11)]
    code = value
    codes = [int(num) for num in code]
    # control number created by some operations on first 9 numbers of code
    control_number = codes[9]
    total = 0
    for i in range(10):
        row = codes[i] * positions[i]
        total += row
    
    extant = total % 11

    if not extant < 2 and not extant == control_number:
        raise forms.ValidationError('کد ملی معتبر نیست')
    elif extant >= 2:
        extant = 11 - extant
        if not extant == control_number:
            raise forms.ValidationError('کد ملی معتبر نیست')

def validate_postal_code(value):
    if not len(value) == 10:
        raise forms.ValidationError('کد پستی صحیح نیست')
    elif '2' in value or '0' in value:
        raise forms.ValidationError('کد پستی صحیح نیست')
    elif value[4] == 5:
        raise forms.ValidationError('کد پستی صحیح نیست')
    elif len(set(value)) == 1:
        raise forms.ValidationError('کد پستی صحیح نیست')
    else:
        pass
    

