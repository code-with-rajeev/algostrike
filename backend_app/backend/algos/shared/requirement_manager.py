from backend.interfaces.cache_manager import CacheManager
import json
#from backend.core.uttils import get_logger

#logger = get_logger('app')

"""
DESCRIPTION: handle core logic of Algo's requirements
"""

class RequirementManager:
    def __init__(self):
        self.cache = CacheManager()
        
    def filter_requirements(self,REQUIREMENTS):
        # StreamSubscriber format: hset
        # for GLOBAL : "active_algos:algo:requirements:GLOBAL" : {f"{INS}":[timeframe,last_fetch]}
        pass
        
    def route_requirements(self,REQUIREMENTS):
        """ stores and manages the mapping of requirements to corresponding algorithms """
        filtered_routes = {}
        handler = self.cache.handler()
        key = f"active_algos:algo:requirements:route"
        # {'NIFTY:1M': ['algo1', 'algo3'], 'ZOMATO:5M': ['algo1', 'algo3'], 'NIFTY:5M': ['algo2'], 'RELIANCE:15M': ['algo2']}
        for algo  in REQUIREMENTS:
            static_requirements = algo['requirements']
            for r in static_requirements:
                symbol = f"{r['instrument']}:{r['timeframe']}"
                if filtered_routes.get(symbol, None):
                    filtered_routes[symbol].append(algo['algo_name'])
                else:
                    filtered_routes[symbol] = [algo['algo_name']]

        #add in redis
        for requirement,routes in filtered_routes.items():
            handler.hset(key, requirement,json.dumps(routes))
            handler.expire(key,86400)# TTL: 24 Hours
