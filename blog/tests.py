
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

User = get_user_model()


class MyAccountTest(TestCase):
    def setUp(self):
        self.email = "admin@gmail.com"
        self.password = "admin"
        self.user = User.objects.create_user(email = self.email, password = self.password)
        self.url = reverse('user:user-create')
    
    def test_status_code(self):
        self.author = self.client.login(email = self.email, password = self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


