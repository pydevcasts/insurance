

from django import forms
from newsletters.models import NewsLetter


class NewsLettersForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ("subscriber",)

