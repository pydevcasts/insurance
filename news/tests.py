from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from category.models import Category
from news.views import NewListView

User = get_user_model()
from .models import New


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.password = "admin"
        self.user = User.objects.create_user(email = "admin@gmail.com", password = self.password)
        self.url = reverse('user:user-create')


class NewTests(MyAccountTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(email = "admin@gmail.com", password = self.password)
        self.response = self.client.get(self.url)
    #     

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)



    # def test_new_page_tempplate_dashboard(self):
    #     self.response = self.client.get(reverse("dashboard:new-list"))
    #     # print(self.response)
        # self.assertTemplateUsed(self.response, 'dashboard/news/list.html')



    def test_new_list_resolve(self):
        self.view = resolve('/new/list-news')
        # self.assertEqual(self.view.__class__.__name__,NewListView)
        self.assertEqual(self.view.url_name,'pages')
  

    

class FrontPageNew(TestCase):
    def setUp(self):
        self.url = reverse('new:list_news')
        self.response = self.client.get(self.url)
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        author = User.objects.create_user(first_name='siyamak',last_name = "abasnezhad" , email='jamal@doe.com', password='123')
        self.published_at = timezone.now()
        self.new = New.objects.create(title='Django', slug = "new-django", summary = "Django summary test blog post", author = author,
            banner="https://static.vecteezy.com/system/resources/previews/002/375/042/non_2x/abstract-background-wave-radial-ellipse-free-vector.jpg",\
            content='Django board.', published_at = self.published_at, category = category)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    

    # def test_url_page_resolve_frontend_view_class(self):
    #     self.view = resolve('/new/')
    #     self.assertEquals(self.view, NewListView)

    # def test_template_front_view(self):
        # self.response = self.client.get(self.url)
        # self.assertTemplateUsed(self.response, 'frontend/news/index.html')


    # def test_get_absulote_url_view(self):
    #     new = New.obgects.get(id = 1)
    #     self.assertEqual(new.get_absolute_url(), f'new/{self.published_at}/new-django/')

    def test_title_max_length(self):
        new = New.objects.get(uid = '053652f5-00dd-4f79-890e-19caec16e81b')
        max_length = new._meta.get_field("title").max_length
        self.assertEqual(max_length, 128)

    # def test_summary_max_length(self):
    #     new = New.objects.get(id = 1)
    #     max_length = new._meta.get_field('summary').max_length
    #     self.assertEqual(max_length, 128)