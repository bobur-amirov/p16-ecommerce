from __future__ import absolute_import, unicode_literals
import os
import time

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')

app = Celery('Ecommerce')
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    time.sleep(10)
    print(f"Request: {self.request!r}")