from fastapi import Request, HTTPException
from app.core.redis import redis_client

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        client_ip = request.client.host if request.client else "127.0.0.1"
            
        path = request.url.path
        key = f"rate_limit:{client_ip}:{path}"
        
        current = await redis_client.get(key)
        if current and int(current) >= self.times:
            raise HTTPException(status_code=429, detail="Too Many Requests")
            
        pipe = redis_client.pipeline()
        pipe.incr(key, 1)
        pipe.expire(key, self.seconds)
        await pipe.execute()
