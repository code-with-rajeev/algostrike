"""
ABOUT: manage cache with redis server
"""

import redis
import json

class CacheManager:
    def __init__(self):
        # Initialize Redis client
        self.client = redis.Redis(host='localhost', port=6379, db=0)  # Update with EC2 Redis

    def handler(self):
        """
        gives full access to redis
        """
        return self.client
    def set(self, key, value, ttl=None):
        """
        Store a value in the cache with an optional expiry time.
        """
        self.client.set(key, json.dumps(value))
        if ttl:
            self.client.expire(key, ttl)
            
    def get(self, key):
        """
        Retrieve a value from the cache.
        """
        value = self.client.get(key)
        return json.loads(value) if value else None