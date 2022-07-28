from django.test import TestCase
from django.urls import resolve, reverse
from blog.views import PostListView
import urllib.parse
from django.contrib.auth import get_user_model
User = get_user_model()


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.password = 'admin'
        self.user = User.objects.create_user(email='admin@gmail.com', password=self.password)
        self.url = reverse('user:create')


class DashboardPostListTest(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email='admin@gmail.com', password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_post_list_url_resolves_post_view(self):
        view = resolve('/blog/list/')
        self.assertEquals(view.func.view_class, PostListView)
    
    def test_post_page_template(self):
        url = reverse('blog:list')
        self.response = self.client.get(url)
        self.assertTemplateUsed(self.response, 'backend/blog/list.html')
    

