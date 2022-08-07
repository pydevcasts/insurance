from django import forms
from faq.models import FAQ


        
class FaqForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['name','subject','content','email', 'phone']