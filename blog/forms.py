from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(label='پیام', widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    class Meta:
        model = Post
        exclude=("slug","published_at")


    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 5:
            raise forms.ValidationError("طول متن نباید کمتر از ۵ حرف باشد")
        return data

    def clean_summary(self):
        data = self.cleaned_data.get('summary')
        if len(data) < 10:
            raise forms.ValidationError("طول متن نباید کمتر از ۱۰ حرف باشد")
        return data





           