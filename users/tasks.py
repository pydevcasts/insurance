import string

from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

User = get_user_model()

@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user( email=email, first_name = "username",last_name = "username", password=password)
    return '{} random users created with success!'.format(total)
