from __future__ import absolute_import, unicode_literals
import os
import sys 
from celery import Celery
from django.conf import settings

# Project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path where settings.py exists.
sys.path.append(PROJECT_DIR)

# Import Django settings to Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE','settings')

app = Celery('backend_app')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings

# Path where Celery will look for tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')