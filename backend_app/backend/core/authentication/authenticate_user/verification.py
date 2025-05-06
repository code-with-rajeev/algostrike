"""
Verify user
"""
from backend.interfaces.cache_manager import CacheManager

def generate_otp(username, email):
    # Return JSON Response
    import random
    handler = CacheManager().handler() # full access
    key = f'user:authentication:{email}:otp'
    
    if handler.exists(key):
        # check for timeout left
        attempts = int(handler.hget(key, "attempts").decode('utf-8'))
        ttl = handler.ttl(key)
        if (attempts < 3):
            return {"status":False, "message":f"OTP has already been sent.", "type": "OTP sent", "attempts":attempts}
        else:
            return {"status":False, "message":f"Too many attempts. Try again in {ttl} seconds.", "type":"max attempts", "ttl":ttl}


    # Random 6-digits otp
    otp = str(random.randint(100000,999999))

    mapping = {
        "otp":otp,
        "attempts":0
        }
    
    handler.hset(key, mapping = mapping) # store in redis
    handler.expire(key, 300)# 5-min expiry (300 seconds)

    try:
        # Import module for sending email
        from backend.core.notifications import authentication_otp_mail as auth
        auth(username, email,otp)
        #print("Your OTP is",otp)
        return {"status":True, "message":"OTP has been sent"}
    except Exception as a:
        #print(f'Error while sending mail {a}')
        return {"status":False, "message":"Email service is temporarily unavailable"}

def verify_otp(email,otp):
    handler = CacheManager().handler() # full access
    key = f'user:authentication:{email}:otp'
    user_otp = handler.hget(key, "otp")
    user_attempts = handler.hget(key, "attempts")

    if user_otp:
        # Convert decode bytes
        user_otp = user_otp.decode('utf-8')
        user_attempts = int(user_attempts.decode('utf-8'))
        # ttl: time-till-expiry
        ttl = handler.ttl(key)

        if user_attempts > 2:
            # Max attempts reached.
            return {"status":False, "message":f"Too many attempts. Try again in {ttl} seconds.", "type":"max attempts", "ttl":ttl}
        if user_otp == otp:
            # Verified
            handler.delete(key)
            return {"status":True, "message":"OTP has been verified"}
        else:
            # hincrby: used to increment a numeric field in a Redis hash by specific amount, atomic.
            handler.hincrby(key, "attempts", 1)
            user_attempts += 1
            if (user_attempts > 2): return {"status":False, "message":f"Too many attempts. Try again in {ttl} seconds.", "type":"max attempts", "ttl":ttl}
            return {"status":False, "message":f"Invalid OTP! {3-user_attempts} attempts left."}
    else:
        handler.delete(key)
        return {"status":False, "message":"The OTP has expired. Please try again.", "type":"expired"}