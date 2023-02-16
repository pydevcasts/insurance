
from django.urls import reverse,resolve
from django.test import TestCase
from blog.models import Post
from tag.models import Tag
from category.models import  Category
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
import urllib
from dashboard.views import PostListView


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



class BlogPostTests(MyAccountTest):
    def setUp(self):
        super().setUp()
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        self.author = User.objects.get(email = "admin@gmail.com")
        published_at = timezone.now()
        self.post = Post.objects.create(title='Django', summary = "Django summary test blog post", author= self.author, category = category, content='Django board.', published_at = published_at)

    def tearDown(self):
        print("Done..")

    def test_redirection_post_list_view(self):
        response = self.client.get(reverse('dashboard:post-list'), follow=True)
        expected_url = reverse('login') + "?next=" + urllib.parse.quote(reverse('dashboard:home'), "")
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


    def test_is_stance_of_class(self):
        self.assertIsInstance(self.post, Post)


    def test_post_status_code(self):
        User.objects.create_superuser(password="super", email="super@gmail.com")
        self.client.login(email = "super@gmail.com", password = "super")
        self.response = self.client.get(reverse('dashboard:post-list'))
        self.assertEqual(self.response.status_code, 200)

    
    def test_post_count_query(self):
        qs = Post.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), 1)

    
    def test_title_in_queryset(self):
        qs = Post.objects.get(status = 1, published_at__lte = timezone.now())
        self.assertIn("Django", qs.title)


    def test_url_name_list_view_dashboard(self):
        self.view = resolve('/dashboard/list-post/')
        self.assertEqual(self.view.url_name, 'post-list')
    

    def test_class_name_list_view_dashboard(self):
        self.view = resolve("/dashboard/list-post/")
        self.assertEqual(self.view.func.view_class, PostListView)

    def test_common_set_up(self):
        User.objects.create_superuser(password="super", email="super@gmail.com")
        self.client.login(email = "super@gmail.com", password = "super")
        self.url = reverse('dashboard:post-list')
        self.response = self.client.get(self.url)


    def test_context_post_list_dashboard(self):
        self.test_common_set_up()
        self.assertTrue("posts" in self.response.context)
    

    def test_template_use_dashboard(self):
        self.test_common_set_up()
        self.assertTemplateUsed(self.response, 'dashboard/blog/list.html')
    

    def test_realationcat_and_post_dashboard(self):
        cat_one = Category.objects.get(title = "test category")
        qs_one = Post.objects.published().select_related('category').order_by('category_id').distinct('category')
        qs_tow = Post.objects.filter(category = cat_one)
        self.assertTrue(qs_one.exists())
        self.assertTrue(qs_tow.exists())
        self.assertNotEqual(qs_one, qs_tow)
    

    def test_manytomany_relation_tag_post_dashboard(self):
        tag = Tag.objects.all()
        self.assertFalse(tag.exists())
        tag_one = Tag.objects.create(title = "first tag", slug = "first-tag")
        self.post.tags.add(tag_one)
        self.assertTrue(self.post.tags.exists())
        self.assertEqual(self.post.tags.all().count(),1)
        qs = Post.objects.prefetch_related('tags')
        self.assertTrue(qs.exists())
    

