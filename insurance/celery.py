import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance.settings')

app = Celery('insurance')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



# https://coderedirect.com/questions/571813/django-celery-send-register-email-do-not-work
# https://www.merixstudio.com/blog/boost-your-django-project-celery/