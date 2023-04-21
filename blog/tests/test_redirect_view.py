from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post
from category.models import Category

User = get_user_model()
import urllib


class BlogPostTests(TestCase):
    def test_redirection_post_list_view(self):
        response = self.client.get(reverse('dashboard:post-list'), follow=True)
        expected_url = reverse('login') + "?next=" + urllib.parse.quote(reverse('dashboard:home'), "")
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


    
    def test_redirect_post_create_view_dashboard(self):
        response = self.client.get(reverse('dashboard:post-create'), follow=True)
        expected_url = reverse('login') + "?next=" + urllib.parse.quote(reverse('dashboard:home'), "")
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)