from django import forms
from category.models import Category
from django.utils.translation import gettext_lazy as _

        
class CategoryForm(forms.ModelForm):
    content = forms.CharField(label='پیام', widget=forms.Textarea(attrs={'class': 'ckeditor'}))
   
    class Meta:
        model = Category
        exclude = ("slug","published_at")

