

from django import forms
from newsletters.models import NewsLetter


class NewsLettersForm(forms.ModelForm):
    # subscriber = forms.EmailField(
    #         widget=forms.TextInput(attrs={'placeholder': 'ایملتان را وارد کنید ...'}))

    class Meta:
        model = NewsLetter
        fields = ("subscriber",)

