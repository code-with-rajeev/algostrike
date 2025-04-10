"""
Manage incoming socket stream data of ticks and store them in redis.
FORMAT:
redis-list: "OHLC:{instrument}:{timeframe}":[...]

"""