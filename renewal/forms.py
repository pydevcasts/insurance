from django import forms
from django.utils.translation import gettext_lazy as _

from renewal.models import Renewal


class RenewalForm(forms.ModelForm):

    class Meta:
        model = Renewal
        fields = ("name","code", "phone", "category",)


    
