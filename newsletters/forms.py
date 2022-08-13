

from django import forms
from newsletters.models import NewsLetter


class NewsLettersForm(forms.ModelForm):
    email = forms.EmailField(label='ایمیل', 
            widget=forms.TextInput(attrs={'placeholder': 'ایملتان را وارد کنید ...'}))

    class Meta:
        model = NewsLetter
        fields = ("email",)

