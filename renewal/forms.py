from django import forms
from renewal.models import Renewal
from django.utils.translation import gettext_lazy as _

class RenewalForm(forms.ModelForm):

    class Meta:
        model = Renewal
        fields = ("name","code", "phone", "category",)


    
