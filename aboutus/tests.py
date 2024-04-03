from django.test import TestCase
from django.urls import reverse, resolve

from aboutus.views import AboutView
from . models import About


class AboutModelTest(TestCase):
    def setUp(self):
        self.about = About.objects.create(summary="this is a test summary", banner=None, content="this is content test ")
        self.url = reverse("about:about-insurance")
        self.response = self.client.get(self.url)
        self.view = resolve("/about/")
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_is_active(self):
        self.assertTrue(self.about.status)
    
    def test_page_template_list_view(self):
        self.assertTemplateUsed(self.response, 'frontend/about/index.html')
    
    def test_page_create_url_name(self):
        self.assertEquals(self.view.url_name, 'about-insurance')
    
    def test_page_create_about_class_name(self):
        self.assertEqual(self.view.func.view_class, AboutView)