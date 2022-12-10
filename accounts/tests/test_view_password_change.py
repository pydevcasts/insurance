from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase
from django.urls import resolve, reverse
import urllib.parse
from django.contrib.auth import get_user_model
User = get_user_model()



class PasswordChangeTests(TestCase):
    def setUp(self):
        email = 'admin@gmail.com'
        password = 'admin'
        User.objects.create_user(email=email, password=password)
        url = reverse('dashboard:password_change')
        self.client.login(email=email, password=password)
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, old_password, new_password1, new_password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="password"', 3)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('dashboard:password_change')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    '''
    Base test case for form processing
    accepts a `data` dict to POST to the view.
    '''
    def setUp(self, data={}):
        self.user = User.objects.create_user(email='admin@gmail.com', password='old_password')
        self.url = reverse('dashboard:password_change')
        self.client.login(email='admin@gmail.com', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        '''
        refresh the user instance from database to get the new password
        hash updated by the change password view.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have an `user` to its context, after a successful sign up.
        '''
        response = self.client.get(reverse('dashboard:home'))
        user = response.context.get('user')
        self.assertTrue(user.)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        '''
        refresh the user instance from the database to make
        sure we have the latest data.
        '''
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))
