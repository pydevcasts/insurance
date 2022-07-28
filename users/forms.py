import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from users.models import Profile

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=16)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if len(data) < 5:
            raise forms.ValidationError("length of firstname is less than Five!")
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        if len(data) < 5:
            raise forms.ValidationError("length of lastname is less than Five!")
        return data

    def clean_password(self):
        data = self.cleaned_data.get('password')
        if len(data) < 8:
            raise forms.ValidationError("length of title is less than eight!")
        return data

    def clean_birthday(self):
        data = self.cleaned_data.get('birthday')
        if data != None and data > datetime.date.today():
            raise forms.ValidationError(
                    """
                    \'to\' date cannot be later than today.
                    """)



def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg




class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(20),
            MaxValueValidator(500)
        ]
    )
    