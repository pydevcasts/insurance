
import urllib.parse
from django.urls import reverse,resolve
from django.test import TestCase, testcases
from blog.models import Post
from tag.models import Tag
from category.models import SubCategory, Category
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class BlogPostTests(TestCase):
    def setUp(self):
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        subcategory = SubCategory.objects.create(title='Django subcat', content='Django subcat.', category = category)
        author = User.objects.create_user(first_name='siyamak',last_name = "abasnezhad" , email='jamal@doe.com', password='123')
        published_at = timezone.now()
        self.post = Post.objects.create(title='Django', summary = "Django summary test blog post", author = author, banner="https://static.vecteezy.com/system/resources/previews/002/375/042/non_2x/abstract-background-wave-radial-ellipse-free-vector.jpg",subcategory = subcategory, content='Django board.', published_at = published_at)


    def test_redirection_post_list_view(self):
        response = self.client.get(reverse('blog:list'), follow=True)
        expected_url = reverse('login') + "?next=" + urllib.parse.quote(reverse('blog:list'), "")
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)


    
