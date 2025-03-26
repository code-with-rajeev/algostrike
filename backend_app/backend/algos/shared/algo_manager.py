import importlib
from celery import shared_task
from myapp.models import Algo  # Adjust your ORM model
from backend.interfaces.cache_manager import CacheManager
#from backend.core.uttils import get_logger

#logger = get_logger('app')

"""
DESCRIPTION: handle core logic of Algo's
"""

class AlgoManager:
    def __init__(self):
        self.cache = CacheManager()
        self.base_path = "backend.algos" #Python module path to algo folders
        
    def get_algo_module(self, algo_name):
        """Dynamically import an algo’s config.py."""
        try:
            module = importlib.import_module(f"{self.base_path}.{algo_name}.config")
            return module
        except ImportError as e:
            """
            logger.error(f"Failed to load config for {algo_name}: {str(e)}")
            """
            return None
    
    def get_algo(self, status):
        """Return algos with required status"""
        if not status:
            """Raise an Error"""
            return None
        try:
            algos = Algo.objects.get(is_active=status)
            all_algos = []
            for algo in algos:
                all_algos.append({"name":algo.name, "id":algo.id})
            return all_algos
        except Algo.DoesNotExist:
            """
            logger.warning(f"Cannot disable, algo {algo_name} not found")
            """
            return []


    def get_requirements(self, algo_name):
        """Read requirements from algo’s config.py."""
        module = self.get_algo_module(algo_name)
        if module and hasattr(module, 'STATIC_REQUIREMENTS'):
            return module.STATIC_REQUIREMENTS  # e.g., ["NIFTY", "5min"]
        return []  # Default empty list

    def setup_requirements(self,REQUIREMENTS):
        """Remove duplicates and store in redis"""
        req_manager = RequirementManager()
        
    def get_subscribed_users(self, algo_name):
        """Fetch all users subscribed to this algo."""
        try:
            algo = Algo.objects.get(name=algo_name)
            subscriptions = Subscription.objects.filter(algo=algo, is_active=True)
            return [sub.user_id for sub in subscriptions]
        except Algo.DoesNotExist:
            """
            logger.warning(f"Algo {algo_name} not found in DB")
            """
            return []
        except Exception as e:
            """
            logger.error(f"Error fetching users for {algo_name}: {str(e)}")
            """
            return []

    def disable(self, algo_name):
        """Mark algo as disabled in DB."""
        try:
            algo = Algo.objects.get(name=algo_name)
            algo.is_active = "disabled"
            # Remove all connections
            algo.save()
            """
            logger.info(f"Disabled algo: {algo_name}")
            """
        except Algo.DoesNotExist:
            """
            logger.warning(f"Cannot disable, algo {algo_name} not found")
            """
            pass

    def set_active(self, algo_name):
        """Mark algo as active in DB and Redis."""
        try:
            algo = Algo.objects.get(name=algo_name)
            algo.is_active = True
            algo.save()
            key = f"active_algo:algo:{algo_name}"
            #data = {"status": "active", "requirements": self.get_requirements(algo_name)}
            #self.cache.set(key, data, ttl=86400)  # 24-hour TTL
            """
            logger.info(f"Set algo {algo_name} as active in Redis")
            """
        except Algo.DoesNotExist:
            """
            logger.warning(f"Cannot activate, algo {algo_name} not found")
            """
            pass