"""
Manage incoming socket stream data of ticks and store them in redis.
FORMAT:
redis-list: "OHLC:{instrument}:{timeframe}":[...]

"""
"""
ABOUT: handles the entire process of managing OHLC.
MAPPING:
    fdtm: EXCHANGE FEEDER TIME
    ltt: LAST TRADED TIME
"""
from backend.interfaces.cache_manager import CacheManager
from datetime import datetime

token_mapping = {
    "26000":"NIFTY"
    }

class TickManager:
    def __init__(self, timeframe = '1M'):
        self.timeframe = timeframe
        self.ping = None
        
    def update_OHLC(self, stock_feed):
        timestamp = None
        tk = None
        ltp = None
        
        for data in stock_feed:
            
            # check if both ltp and token value recived
            if not('ltp' in data and 'tk' in data):
                continue
            
            # fetch current tick timestamp
            timestamp = data.get('ftdm', None) or data.get('ltt', None)
            if not timestamp:
                continue
            # Convert datetime into UNIX timestamp
            timestamp = int(datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S").timestamp())

            # key = f"ohlc:{intrument_token}:{timeframe}"
            key = f"ohlc:{data['tk']}:{self.timeframe}"
            last = r.lindex(key,0)
            ltp = data['ltp']
            # print(f"LTP : {ltp}")
            if last:
                last_dt = eval(last)
                last_dt = int(last['timestamp'])
                if last_dt//60 != timestamp//60:
                    new_candle={
                        "timestamp":ltt_dt,
                        "o":ltp,
                        "h":ltp,
                        "l":ltp,
                        "c":ltp
                        }
                    r.lpush(key,str(new_candle))
                    #r.ltrim(key,0,9)
        
                else:
                    # Update existing candle
                    last['h'] = max(last['h'],ltp)
                    last['l'] = min(last['l'],ltp)
                    last['c'] = ltp
                    r.lset(key,0,str(last))
            else:
                new_candle={
                    "timestamp":ltt_dt,
                    "o":ltp,
                    "h":ltp,
                    "l":ltp,
                    "c":ltp
                    }
                r.lpush(key,str(new_candle))