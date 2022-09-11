from django import forms
from blog.models import Comment, Post
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    content = forms.CharField(label=_('content'),widget=CKEditorWidget())
    class Meta:
        model = Post
        exclude=("slug",)


    def clean_title(self):
        data = self.cleaned_data.get('title')
        if len(data) < 5:
            raise forms.ValidationError("length of title is less than Five!")
        return data

    def clean_summary(self):
        data = self.cleaned_data.get('summary')
        if len(data) < 20:
            raise forms.ValidationError("the length of summary is less than 20 letter!")
        return data


    def clean_published(self):
        data = self.cleaned_data.get('published_at')
        if not data == "DD/MM/YYYY":
            raise forms.ValidationError("format is not true")
        return data
    


class CommentForm(forms.ModelForm):
        # content_type = forms.CharField(widget=forms.HiddenInput,required=False)
        # object_id = forms.IntegerField(widget=forms.HiddenInput,required=False)
        # content = forms.CharField(widget=forms.Textarea(attrs={
        #     'class': 'form-control',
        #     'id': 'body',
        #     'rows': 5,
        #     'cols': 40
        # }))

        class Meta:
            model = Comment
            fields = ['content']
           