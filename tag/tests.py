from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .models import Tag

User = get_user_model()

class MyAccountTest(TestCase):
    def setUp(self):
        self.password = "admin"
        self.email = "admin@gmail.com"
        self.user = User.objects.create_user(email = self.email, password = self.password)
        self.url = reverse('user:user-create')


class TagModelTest(MyAccountTest):
    def setUp(self):
        super().setUp()
        tag_1 = Tag.objects.create(title = "secound tag", slug = "secound-tag",status = 1)
        tag_2 = Tag.objects.create(title = "third tag", slug = "third-tag",status = 0)
        self.client.login(email = self.email, password = self.password)
        self.url = reverse('user:user-create')
        self.response = self.client.get(self.url)


    def test_status_code_user(self):
        self.assertEqual(self.response.status_code, 200)
    

    def test_check_username(self):
        self.assertTrue(self.user.email, 'admin@gmail.com')


    def test_tag_list_url_name(self):
        self.view = resolve('/tag/list/')
        self.assertEqual(self.view.url_name, 'tag-list')


    def test_tag_template_dashboard_use(self):
        self.response = self.client.get(reverse('tag:tag-list'))
        self.assertFalse(self.user.has_perm('tag.view_tag'))
        self.assertTemplateUsed(self.response, 'dashboard/tag/list.html')
        

    def test_tag_create_url_name(self):
        self.view = resolve('/tag/create/')
        self.assertEqual(self.view.url_name, 'tag-create')

    
    def test_tag_delete_url_name(self):
        self.slug = 'secound-tag'
        self.view = resolve(f'/tag/{self.slug}/delete/')
        self.assertEqual(self.view.url_name, 'tag-delete')
    

    def test_tag_update_url(self):
        self.slug = 'secound-tag'
        self.view = resolve(f'/tag/{self.slug}/edit/')
        self.assertEqual(self.view.url_name, 'tag-update')


    def test_tag_status_code(self):
        self.url = reverse('tag:tag-list')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    

    def test_tag_status_code_create_page(self):
        self.url = reverse('tag:tag-create')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    

    def test_tag_templateuse_create_tag(self):
        self.url = reverse('tag:tag-create')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'dashboard/tag/create.html')


    def test_draft_post_count(self):
        qs = Tag.objects.filter(status = 0)
        self.assertEqual(qs.count(), 1)
    


