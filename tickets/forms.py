from django import forms
from . models import Ticket, FollowUp, Attachment
from django.forms import inlineformset_factory




class TicketCreateForm(forms.ModelForm):
    description = forms.CharField(label='پیام', widget=forms.Textarea(attrs={'class': 'ckeditor','style':'direction:rtl;'}))
    class Meta:
        model = Ticket
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'user', 'description',
                  'status', )


class FollowupForm(forms.ModelForm):
    description = forms.CharField(label='پیام', widget=forms.Textarea(attrs={'class': 'ckeditor'}))
    class Meta:
        model = FollowUp
        fields = ('title', 'description',)
       


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('file','filename',)
        widgets = {
                'filename': forms.TextInput(
                    attrs={
                        'class': 'form-control'
                        }
                    ),
            }


AttachmentFormSet = inlineformset_factory(
    Ticket, Attachment, form=AttachmentForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)

