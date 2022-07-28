from django.test import TestCase
from django.urls import resolve, reverse
from frontend.views import post_subcategory_list


class FrontPageTests(TestCase):
    def setUp(self):
        url = reverse('frontend:post_and_subcategory')
        self.response = self.client.get(url)

    def test_front_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_front_url_resolves_front_view(self):
        view = resolve('/frontend/')
        self.assertEquals(view.func, post_subcategory_list)

   