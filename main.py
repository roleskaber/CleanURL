from fastapi import Body, FastAPI, HTTPException, status, Depends
from url_shortener.database.db import engine
from url_shortener.database.models import Base
from contextlib import asynccontextmanager


from ratelimiter.service import get_redis
from ratelimiter.factory import rate_limiter_factory

from url_shortener.service import generate_short_url, get_url_by_slug
from fastapi.responses import RedirectResponse
from url_shortener.exceptions import NoUrlFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    redis = get_redis()
    await redis.ping()
    yield
    await redis.aclose()


app = FastAPI(lifespan=lifespan)


short_url_limiter = rate_limiter_factory("short_url", 3, 5)
slug_url_limiter = rate_limiter_factory("slug_url", 20, 3)


@app.post("/short_url", dependencies=[Depends(short_url_limiter)])
async def generate_slug_url(
        long_url: str = Body(embed=True)
):
    slug = await generate_short_url(long_url)
    return {"slug": slug}


@app.get("/{slug}", dependencies=[Depends(slug_url_limiter)])
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug=slug)
    except NoUrlFoundException:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="...")
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
