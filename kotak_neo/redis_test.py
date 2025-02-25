import redis
import json
from datetime import datetime
# Connect to Redis
r = redis.Redis(host="localhost", port=6379,db=0)

# Deletes all the keys in the current database [ db = 0 ]
# r.flushdb()
#r.set('key','value')
def update(ins , tf , ltp, ltt):
    key = f"ohlc:{ins}:{tf}"
    
    ltt_dt = int(datetime.strptime(ltt, "%d/%m/%Y %H:%M:%S").timestamp())
    last = r.lindex(key,0)
    
    if last:
        last = eval(last)
        last_dt = int(last['timestamp'])
        if last_dt//60 != ltt_dt//60:
            print('New Candle')
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
            #print("updating.. current candle")
            last['h'] = max(last['h'],ltp)
            last['l'] = min(last['l'],ltp)
            last['c'] = ltp
            r.lset(key,0,str(last))
        
        
    
    # Check for new candle
    else:        
        new_candle={
            "timestamp":ltt_dt,
            "o":ltp,
            "h":ltp,
            "l":ltp,
            "c":ltp
            }
        r.lpush(key,str(new_candle))
        #print("New Candle")
    #print(r.lrange('ohlc:NIFTY:1M',0,-1))
