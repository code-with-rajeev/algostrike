from celery import shared_task
from myapp.models import Algo  # Adjust your ORM model
from backend.interfaces.cache_manager import CacheManager
#from backend.core.uttils import get_logger

#logger = get_logger('app')

"""
DESCRIPTION: handle core logic of Algo's requirements
"""

class RequirementManager:
    def __init__(self):
        self.cache = CacheManager()
        
    def filter_requirements(REQUIREMENTS):
        # StreamSubscriber format
        # for GLOBAL : "active_algos:algo:requirements:GLOBAL" : {f"{INS}":
        pass
        
    def route_requirements(REQUIREMENTS):
        routes = {}
        # {'NIFTY:1M': ['algo1', 'algo3'], 'ZOMATO:5M': ['algo1', 'algo3'], 'NIFTY:5M': ['algo2'], 'RELIANCE:15M': ['algo2']}
        for algo  in REQUIREMENTS:
            req = algo['req']
            for r in req:
                key = f"{r['instrument']}:{r['timeframe']}"
                if routes.get(key, None):
                    routes[key].append(algo['algo_name'])
                else:
                    routes[key] = [algo['algo_name']]

        #add in redis
        self.cache.set(f"active_algos:algo:requirements:route", routes, ttl=86400)  # 24-hour TTL
        return routes
