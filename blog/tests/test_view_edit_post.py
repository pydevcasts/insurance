from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from django.utils import timezone

from blog.models import Post
from blog.tests import MyAccountTest
from category.models import Category
from dashboard.views import PostUpdateView

User = get_user_model()



class PostUpdateViewTestCase(MyAccountTest):
    def setUp(self):
        super().setUp()
        user = User.objects.create_superuser(password="super", email="super@gmail.com")
        self.client.login(email = "super@gmail.com", password = "super")
        category = Category.objects.create(title = "test category", content = 'this is test content category')
        published_at = timezone.now()
        self.post = Post.objects.create(title='Django', summary = "Django summary test blog post", author= user, category = category, content='Django board.', published_at = published_at)
        self.post.tags.create(title = "test tag", status = 1)
        self.url = reverse('dashboard:post-update', kwargs={
            'pk': self.post.pk,
        })
        self.response = self.client.get(self.url)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_view_class(self):
        view = resolve('/dashboard/d89f155e-1059-4fe7-a275-a2a318277774/edit-post/')
        self.assertEquals(view.func.view_class, PostUpdateView)


    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, '<textarea', 1)


    def test_update_view_contains_link_to_post_list_page(self):
        x = reverse('dashboard:post-list')
        response = self.client.get(self.url)
        self.assertContains(response, 'href="{}"'.format(x))


    def test_new_post_valid_data(self):

        data = {
            "title": "test update",
            'summary': 'Test title',
            'content': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(self.url, data)
        self.assertTrue(Post.objects.exists())
        self.assertTrue(Category.objects.exists())
        self.assertEqual(response.status_code, 200)

    
    def test_new_post_invalid_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)


    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.title, 'Django')



