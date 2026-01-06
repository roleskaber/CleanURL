from functools import lru_cache
from time import time
import random
from redis.asyncio import Redis


@lru_cache
def get_redis() -> Redis:
    return Redis(host='localhost', port=6379)


@lru_cache
def get_rate_limiter() -> RateLimiter:
    return RateLimiter(get_redis())


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(
            self,
            ip_address: str,
            endpoint: str,
            max_requests: int,
            window_seconds: int
    ) -> bool:
        key = f"ratelimiter:{endpoint}:{ip_address}"
        current_ms = time() * 1000
        window_start_ms = current_ms - window_seconds * 1000
        current_request = f"{time() * 1000}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, window_start_ms)
            await pipe.zcard(key)
            await pipe.zadd(key, {current_request: current_ms})
            await pipe.expire(key, window_seconds)
            res = await pipe.execute()
        _, cardinality, _, _ = res
        print(cardinality)
        if max_requests > cardinality:
            return False
        return True
