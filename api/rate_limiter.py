import os
import redis
from fastapi import HTTPException, Request
import logging

logger = logging.getLogger(__name__)
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

def verify_rate_limit(request: Request):
    """
    Distributed Rate Limiter using Redis.
    Protects multi-core Gunicorn workers from localized DDoS and SLA degradation.
    Limit: 50 requests per minute per IP.
    """
    client_ip = request.client.host
    cache_key = f"rate_limit:{client_ip}"
    
    try:
        current_requests = redis_client.get(cache_key)
        
        if current_requests and int(current_requests) >= 50:
            logger.warning(f"[Rate Limiter] SLA Protection triggered for IP: {client_ip}")
            raise HTTPException(status_code=429, detail="Too Many Requests: SLA Protection Active. Please slow down.")
            
        # Increment request count and set a 60-second rolling expiry window
        pipe = redis_client.pipeline()
        pipe.incr(cache_key, 1)
        pipe.expire(cache_key, 60)
        pipe.execute()
        
    except redis.RedisError as e:
        logger.error(f"Redis rate limiter bypassed due to connection error: {e}")
        # Fail open: Allow the request through if Redis crashes so the API doesn't completely die
        pass
