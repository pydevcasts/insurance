from django.test import TestCase, override_settings

class MultiDomainTestCase(TestCase):
    @override_settings(ALLOWED_HOSTS=['0.0.0.0'])
    def test_other_domain(self):
        response = self.client.get('127.0.0.1')

 