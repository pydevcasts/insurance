
from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import Comment


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