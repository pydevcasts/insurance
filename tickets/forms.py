from django import forms
from . models import Ticket, FollowUp, Attachment


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description')


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'owner', 'description',
                  'status', 'waiting_for', 'assigned_to')



class FollowupForm(forms.ModelForm):

    class Meta:
        model = FollowUp
        fields = ('ticket', 'title', 'text', 'user')


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('file','ticket', 'filename')
