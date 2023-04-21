from django import forms
from django.utils.translation import gettext_lazy as _

from category.models import Category


class CategoryForm(forms.ModelForm):
    content = forms.CharField(label='پیام', widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    class Meta:
        model = Category
        exclude = ("slug","published_at")

