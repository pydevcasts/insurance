
from django import forms
from newsletters.models import NewsLetters


class NewsLettersForm(forms.ModelForm):
   
    class Meta:
        model = NewsLetters
        fields = ["email"]

    