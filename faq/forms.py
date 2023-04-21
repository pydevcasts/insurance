from django import forms

from faq.models import FAQ


class FaqForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['name','subject','content','email', 'phone']

   
    def clean_name(self):
        data = self.cleaned_data.get('name')
        if len(data) < 5:
            raise forms.ValidationError("طول نام نباید کمتر از ۵ حرف باشد ")
        return data