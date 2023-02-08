from django.test import TestCase
from . models import Category
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from .views import CategoryListView, CreateCategoryView
from blog.models import Post
from django.utils.text import slugify
from django.utils import timezone

class MyAccountTest(TestCase):
    def setUp(self):
        self.email = "admin@gmail.com"
        self.password = "admin"
        self.user = User.objects.create_user(email = self.email, password = self.password)
        self.url = reverse('user:user-create')
    
    def test_status_code(self):
        self.client.login(email = self.email, password = self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class CategoryModelTest(MyAccountTest):
    def setUp(self):
        super().setUp()
        self.cat = Category.objects.create(title = "secound cat", slug = "secound-cat", status = 1)
        self.cat_1 = Category.objects.create(title = "third cat", slug = "third-cat", status = 1)
        self.client.login(email = self.email, password = self.password)
        self.response = self.client.get(reverse('category:cat-list'))
        self.post = Post.objects.create(title = "third post", author = self.user, status = 1, category = self.cat)

    def test_category_is_active(self):
        self.assertTrue(self.cat.status)


    def test_category_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    

    
    def test_check_email(self):
        self.assertEqual(self.user.email, "admin@gmail.com")
    

    def test_category_list_url_for_checkclass(self):
        self.view = resolve('/category/list/')
        self.assertEqual(self.view.func.view_class,CategoryListView )
    

    def test_category_list_url_name(self):
        self.view = resolve('/category/list/')
        self.assertEqual(self.view.url_name, 'cat-list')
        self.response = self.client.get(reverse('category:cat-list'))
        self.assertTrue("categories" in self.response.context)


    def test_category_create_url_name(self):
        self.view = resolve('/category/create/')
        self.assertEqual(self.view.url_name, 'cat-create')
    

    def test_page_template_list_view(self):
        self.url = reverse('category:cat-list')
        self.response = self.client.get(self.url)
        self.assertTemplateUsed(self.response, 'dashboard/category/list.html')
      

    
    def test_page_templatecreate_view(self):
        self.url = reverse('category:cat-create')
        self.response = self.client.get(self.url)
        self.assertFalse(self.user.has_perm('category.create_category'))
        self.assertTemplateUsed(self.response, 'dashboard/category/create.html')

    
    def test_page_creat_cat_url_name(self):
        self.view = resolve('/category/create/')
        self.assertEqual(self.view.url_name, 'cat-create')
    

    def test_page_create_cat_class_name(self):
        self.view = resolve('/category/create/')
        self.assertEqual(self.view.func.view_class, CreateCategoryView)

    
    def test_realated_post_and_category(self):
        qs = self.cat.posts.all()
        self.assertEqual(qs.count(), 1)


    
    def test_slug_field_category(self):
        self.title = self.cat.title
        self.slug = slugify(self.title)
        self.assertEqual(self.slug, self.cat.slug)

    
    def test_title_field_content(self):
        qs = Category.objects.get(slug = 'secound-cat')
        self.assertTrue(qs.title, "secound cat")
    
    def test_queryset_exists(self):
        qs = Category.objects.all()
        self.assertEqual(qs.count(), 2)
    

    def test_check_trime_stamp(self):
        qs = Category.objects.filter(published_at__lte = timezone.now())
        self.assertTrue(qs.exists())

    
    def test_get_absolute_url(self):
        Category.objects.filter(published_at__lte = timezone.now())
        self.slug = "secound-cat"
        self.view = resolve(f'/insurance/{self.slug}/')
        self.assertEqual(self.view.url_name,'detail_by_category_slug')
        self.assertEqual(self.view.func.__name__,'post_category_list')
    

    def test_cat_by_blog_detail_view(self):
        cat = Category.objects.all().first()
        url = cat.get_absolute_url()
        self.assertIsNotNone(url)
    