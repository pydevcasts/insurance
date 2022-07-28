from django import forms
from tag.models import Tag
from django.core.validators import MinValueValidator, MaxValueValidator




class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude=("slug",)


class GenerateRandomTagForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(20),
            MaxValueValidator(500)
        ]
    )
