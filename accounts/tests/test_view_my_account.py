from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from django.urls import resolve, reverse

from users.views import ProfileView
from users.views import ProfileForm


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.email = 'admin@gmail.com'
        self.password = "admin"
        self.user = User.objects.create_user(email=self.email, password=self.password)
        self.url = reverse('user:create')


class MyAccountTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email=self.email, password=self.password)
        self.response = self.client.get(self.url)


    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_url_resolves_correct_view(self):
        view = resolve('/user/create/')
        self.assertEquals(view.func.view_class, ProfileView)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_form_validation_for_blank_items(self):
        form = ProfileForm(data={'first_name': ''})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, first_name, last_name, email
        '''
        self.assertContains(self.response, '<input', 13)
        self.assertContains(self.response, 'type="text"', 6)
        self.assertContains(self.response, 'type="email"', 1)



class LoginRequiredMyAccountTests(TestCase):
    def test_redirection(self):
        url = reverse('user:create')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

