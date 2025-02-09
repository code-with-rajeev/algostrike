from celery import shared_task
import time

@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        pass
    return True
