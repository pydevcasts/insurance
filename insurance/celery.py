import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance.settings')
django.setup()
app = Celery('insurance')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kabul')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


 