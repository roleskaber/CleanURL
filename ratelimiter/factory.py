from fastapi import HTTPException, Request, status, Depends
from typing import Annotated

from ratelimiter.service import RateLimiter, get_rate_limiter


def rate_limiter_factory(
        endpoint: str,
        max_requests: int,
        window_seconds: int,
):
    async def dependency(
            request: Request,
            rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],

    ):
        ip_address = request.client.host

        limited = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds
        )
        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
    return dependency
