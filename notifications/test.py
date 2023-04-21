from django.urls import resolve, reverse
from notifications.models import BroadcastNotification

from blog.views import post_category_list

from django.contrib.auth import get_user_model
from django.urls import resolve, reverse
from django.utils import timezone

from blog.tests import MyAccountTest

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from notifications.tasks import broadcast_notification
User = get_user_model()

# tests/intergration_tests/conftest.py
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
import pytest
from unittest import mock

class NotificationModelTest(MyAccountTest):
    def setUp(self):
        super().setUp()
        user = User.objects.create_superuser(password="super", email="super@gmail.com")
        self.client.login(email = "super@gmail.com", password = "super")
        self.url = reverse('blog:post_and_category')
        self.response = self.client.get(self.url)
        broad = BroadcastNotification.objects.create(message='Big',published_at = timezone.now(), sent=True)

    @classmethod
    def setUpTestData(cls):
        broad = BroadcastNotification.objects.create(message='Big',published_at = timezone.now(), sent=True)
        

    def setUp(self):
        url = reverse('blog:post_and_category')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_front_url_resolves_front_view(self):
        view = resolve('/')
        self.assertEquals(view.func, post_category_list)
    

    def test_post_count_query(self):
        qs = BroadcastNotification.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(), 1)
    

    def test_signal_registry(self):
        from django.db.models import signals
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=12,
            hour=8,
            day_of_week="*",
            day_of_month=1,
            month_of_year=2,
        )
        task = PeriodicTask.objects.create(
            crontab=schedule,
            name="broadcast-notification-" + str(self.id),
            task="notifications.tasks.broadcast_notification",
            args="1",
        )
        registered_functions = [r[1]() for r in signals.post_save.receivers]
        # self.assertIn(task, registered_functions)
        self.assertTrue(broadcast_notification.delay(1))

    @pytest.mark.django_db
    def test_signals_disabled(self):
        example = BroadcastNotification.objects.create(message="Hello World")
        self.assert_  == "Hello World"
    

    @pytest.fixture(autouse=True) # Automatically use in tests.
    def mute_signals(request):
        # Skip applying, if marked with `enabled_signals`
        if 'enable_signals' in request.keywords:
            return

        signals = [
            pre_save,
            post_save,
            pre_delete,
            post_delete,
            m2m_changed
        ]
        restore = {}
        for signal in signals:
            # Temporally remove the signal's receivers (a.k.a attached functions)
            restore[signal] = signal.receivers
            signal.receivers = []

        def restore_signals():
            # When the test tears down, restore the signals.
            for signal, receivers in restore.items():
                signal.receivers = receivers

        # Called after a test has finished.
        request.addfinalizer(restore_signals)

    


    # @pytest.mark.django_db
    # @pytest.mark.enable_signals  # Enable signals for this test.
    # def test_signals_enabled(self):
    #     example = BroadcastNotification.objects.create(message="Hello world")
    #     assert example.message != "Signal override"
    
    @pytest.mark.enable_signals
    def test_signals_enabled(self):
        example = BroadcastNotification.objects.create(message="Hello world2")
        self.assertEqual(example.message, "Signal override")