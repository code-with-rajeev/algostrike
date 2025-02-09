from .celery import app as celery_app

# Helps Django to bind with Celery
__all__ = ('celery_app',)