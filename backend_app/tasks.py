from celery import shared_task

@shared_task
def schedule_algo():
    from backend.tasks.premarket.algo_scheduler import algo_scheduler
    algo_scheduler()

@shared_task
def schedule_stream_worker():
    from backend.algos.shared.stream_manager import start_stream_worker
    start_stream_worker()
    # connect to StreamSubscriber
    # Activate all connection SUB/SNAP/API
