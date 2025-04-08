"""
Verify user
"""
from backend.interfaces.cache_manager import CacheManager

def generate_otp(username):
    import random
    cache = CacheManager()

    # Checks if user attempting again within 5-min
    if cache.exists(f'user:authentication:user_otp:{username}'):
        return False
    # Random 6-digits otp
    otp = str(random.randint(100000,999999))
    user_otp = cache.set(f'user:authentication:user_otp:{username}',otp, ttl = 300 ) # 5-min expiry (300 seconds)
    return True

def verify_otp(username,otp):
    cache = CacheManager()
    user_otp = cache.get(f'user:authentication:user_otp:{username}')
    if user_otp == otp:
        return True
    else:
        return False