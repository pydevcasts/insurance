from django.test import TestCase
from django.urls import resolve, reverse
from blog.views import PostListView
from blog.models import Post
from tag.models import Tag
from category.models import SubCategory, Category
from django.utils import timezone
import urllib.parse
from blog.forms import PostForm
from django.contrib.auth import get_user_model
User = get_user_model()


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.password = 'admin'
        self.user = User.objects.create_user(email='admin@gmail.com', password=self.password)
        self.url = reverse('user:create')


class DashboardPostCreateTest(MyAccountTestCase):
    def setUp(self):
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        subcategory = SubCategory.objects.create(title='Django subcat', content='Django subcat.', category = category)
        author = User.objects.create_user(first_name='siyamak',last_name = "abasnezhad" , email='jamal@doe.com', password='123')
        author.save()
        published_at = timezone.now()
        self.post = Post.objects.create(title='Django', summary = "Django summary test blog post", author = author, banner="https://static.vecteezy.com/system/resources/previews/002/375/042/non_2x/abstract-background-wave-radial-ellipse-free-vector.jpg",subcategory = subcategory, content='Django board.', published_at = published_at)
        self.post.tag.create(title = "test tag", status = 1)
        super().setUp()
        self.client.login(email='admin@gmail.com', password=self.password)
        self.response = self.client.get(self.url)
    
    def test_status_code_post_create(self):
        self.assertEquals(self.response.status_code, 200)


    def test_create_view_contains_link_to_post_list_page(self):
        url = reverse('blog:create')
        x = reverse('blog:list')
        response = self.client.get(url)
        self.assertContains(response, 'href="{}"'.format(x))

    def test_csrf(self):
        url = reverse('blog:create')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    
    def test_logged_user_get_details(self):
        response = self.client.get(reverse('blog:detail', kwargs={"slug":self.post.slug}), )    # for first object
        self.assertEqual(response.status_code, 200)
  

    def test_new_post_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('blog:create')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

