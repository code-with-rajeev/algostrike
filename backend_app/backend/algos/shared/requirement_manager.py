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
        # StreamSubscriber format: hashset
        # redis-key : "active_algos:algo:requirements:GLOBAL"
        # key-value : {
        #    f"{instrument_name}": {
        #         "timeframe":[...],
        #         "instrument_token":token,
        #         "exchange_segment":segment
        #         }
        #    }
        filtered = {
            'SUB':{},
            'SNAP':{},
            'API':{},
            }
        key = f"active_algos:algo:requirements:"
        handler = self.cache.handler()
        # redis-key : "active_algos:algo:requirements:SUB"
        # key-value : {
        #    "NIFTY": {
        #         "timeframe":['1M','5M'],
        #         "instrument_token":26000,
        #         "exchange_segment":"nse_cm"
        #         }
        #    }        for algo  in REQUIREMENTS:

        for algo  in REQUIREMENTS:
            static_requirements = algo['requirements']
            for r in static_requirements:
                mode = r['frequency']
                if filtered[mode].get(r['instrument'],None):
                    filtered[mode][r['instrument']]['timeframe'].append(r['timeframe'])
                else:
                    filtered[mode][r['instrument']] = {'timeframe':[r['timeframe']], 'instrument_token':r['instrument_token'], 'exchange_segment':r['exchange_segment']}
        #add in redis
        for mode,filtered_requirements in filtered.items():
            for instrument,value in filtered_requirements.items():
                handler.hset(key+mode, instrument,json.dumps(value))
                handler.expire(key,86400)# 24-hour TTL
        
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