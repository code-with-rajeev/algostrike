from celery import shared_task
from myapp.models import Algo  # Adjust your ORM model
from backend.interfaces.cache_manager import CacheManager
#from backend.core.utils import get_logger
from datetime import date

#logger = get_logger('scheduler')

@shared_task
def algo_scheduler():
    """
    PREMARKET TASK: activate all inactive algos and store in redis
    """
    pass


@shared_task
def filter_all_algos():
    """
    At any instance, Returns current status of Algos
    """
    cache = CacheManager()
    today = date.today().isoformat()  # e.g., "YYYY-MM-DD"
    try:
        # Fetch all inactive Algos from Django ORM
        # re-activate all inactive Algos
        inactive_algos = Algo.objects.filter(is_active__iexact='inactive')
        active_algos = Algo.objects.filter(is_active__iexact='active') # algo having active positions
        disabled_algos = Algo.objects.filter(is_active__iexact='disabled') # algo is under maintainance
        # is_active == "disabled", means algo under maintainance.
        active_algos = {}
        inactive_algos = {}
        disabled_algos = {}

        for algo in inactive_algos:
            algo_id = algo.algo_id  # e.g., "algo1"
            algo_name = algo.name
            inactive_algos[algo_id].append(algo_name)

        for algo in active_algos:
            algo_id = algo.algo_id  # e.g., "algo1"
            algo_name = algo.name
            active_algos[algo_id].append(algo_name)

        for algo in disabled_algos:
            algo_id = algo.algo_id  # e.g., "algo1"
            algo_name = algo.name
            disabled_algos[algo_id].append(algo_name)
            # Store in Redis: {algo1: [user1, user2], algo2: [user3]}
            #cache.set(f"active_algos:algo:{algo_name}", {"status":"active"})
            #logger.info(f"Scheduled algos for {today}: {active_algos.keys()}")
        return {"inactive_algos":inactive_algos,"active_algos":active_algos,"disabled_algos":disabled_algos}
    except Exception as e:
        #logger.error(f"Failed to schedule algos: {str(e)}")
        return {}
