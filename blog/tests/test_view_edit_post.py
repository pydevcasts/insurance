import urllib.parse
from django.test import TestCase
from django.urls import resolve, reverse
from blog.models import Post
from tag.models import Tag
from category.models import SubCategory, Category
from blog.views import PostUpdateView
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()



class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        author = User.objects.create_user(email='admin@gmail.com', password='admin')
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        subcategory = SubCategory.objects.create(title='Django subcat', content='Django subcat.', category = category)
        published_at = timezone.now()
        self.post = Post.objects.create(title='Django Edit', summary = "Django summary test blog post is Editedt Test", author = author, banner="https://static.vecteezy.com/system/resources/previews/002/375/042/non_2x/abstract-background-wave-radial-ellipse-free-vector.jpg",subcategory = subcategory, content='edited message', published_at = published_at)
        self.post.tag.create(title = "test tag", status = 1)
        self.client.login(email='admin@gmail.com', password="admin")
        self.url = reverse('blog:update', kwargs={
            'pk': self.post.pk,
        })
        self.response = self.client.get(self.url)



    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_view_class(self):
        view = resolve('/blog/d89f155e-1059-4fe7-a275-a2a318277774/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)


    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, '<textarea', 1)


    def test_update_view_contains_link_to_post_list_page(self):
        url = reverse('blog:update', kwargs={'pk':self.post.pk})
        x = reverse('blog:list')
        response = self.client.get(url)
        self.assertContains(response, 'href="{}"'.format(x))


    def test_new_post_valid_data(self):

        data = {
            "title":"test update",
            'summary': 'Test title',
            'content': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(Post.objects.exists())
        self.assertTrue(SubCategory.objects.exists())

    
    def test_new_post_invalid_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)


    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.content, 'edited message')



