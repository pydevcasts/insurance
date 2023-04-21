from django import forms
from django.test import TestCase

from blog.templatetags.form_tags import field_type, input_class
from dashboard.views import PostForm


class ExampleForm(forms.Form):
    title = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        fields = ('title', 'password')
    

class TestFieldTypeTest(TestCase):
    def test_field_widget_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['title']))
        self.assertEquals('PasswordInput', field_type(form['password']))
    
   
class TestInputClassTests(TestCase):
    def test_unbound_field_intial_state(self):
        form = ExampleForm()
        self.assertEqual("form-control", input_class(form['title']))
    

    def test_valid_bound_field(self):
        form = ExampleForm({'title':'john', 'password':'123456'})
        self.assertEquals('form-control is-valid', input_class(form['title']))
        self.assertEquals('form-control', input_class(form['password']))
    
    def test_invalid_bound_field(self):
        form = ExampleForm({'title':'', 'password':'123'})
        self.assertEquals('form-control is-invalid', input_class(form['title']))


    def test_invalid_bound_filed_update_post(self):
        form = PostForm({
            "title":"",
            'summary': 'Test title',
            'content': 'Lorem ipsum dolor sit amet'
        
        })
        self.assertEqual('form-control is-invalid', input_class(form['title']))
