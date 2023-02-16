
from django.urls import reverse,resolve
from django.test import TestCase
from blog.models import Post
from tag.models import Tag
from category.models import  Category
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from blog.forms import PostForm


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


    def test_manytomany_relation_tag_post_dashboard(self):
        tag = Tag.objects.all()
        self.assertFalse(tag.exists())
        tag_one = Tag.objects.create(title = "first tag", slug = "first-tag")
        self.post.tags.add(tag_one)
        self.assertTrue(self.post.tags.exists())
        self.assertEqual(self.post.tags.all().count(),1)
        qs = Post.objects.prefetch_related('tags')
        self.assertTrue(qs.exists())
    


    def test_has_permission_check_dashboard(self):
        self.assertTrue(self.author.email, "admin@gmail.com")
        self.assertFalse(self.author.has_perm('post.create_post'))
        superuser = User.objects.create_superuser(
            password="super", email="super@gmail.com"
            )
        self.assertTrue(superuser.has_perm('post.add_post'))
     
       
   
    def test_status_code_post_create(self):
        User.objects.create_superuser(password="super", email="super@gmail.com")
        self.client.login(email = "super@gmail.com", password = "super")
        self.url = reverse('dashboard:post-create')
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)


    def test_csrf(self):
        self.test_status_code_post_create()
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    

    def test_form_inputs(self):
        self.test_status_code_post_create()
        self.assertContains(self.response, "<input", 6)
        self.assertContains(self.response, '<textarea', 1)

        
    
    def test_contains_form(self):
        self.test_status_code_post_create()
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)


    def test_create_view_link_back_to_post_list_page_dashboard(self):
        self.test_status_code_post_create()
        x = reverse('dashboard:post-list')
        self.assertContains(self.response, 'href="{}"'.format(x))

 