from celery.app import shared_task
from tag.models import Tag
import string
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def create_random_tag(total):
    for i in range(total):
        title = f'{get_random_string(5, string.ascii_letters)}-{get_random_string(5, string.ascii_uppercase)}'
        Tag.objects.create(title = title)
    return '{} random tag created with success!'.format(total)



