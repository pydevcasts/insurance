from django import forms
from tag.models import Tag





class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude=("slug",)


