from fastapi import Body, FastAPI, HTTPException, status
from database.db import engine
from database.models import Base
from contextlib import asynccontextmanager
from service import generate_short_url, get_url_by_slug
from fastapi.responses import RedirectResponse
from exceptions import NoUrlFoundException

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection: 
       await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_slug_url(
    long_url: str = Body(embed=True)
):
    slug = await generate_short_url(long_url)
    return {"slug": slug}


@app.get("/{slug}")
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug=slug)
    except NoUrlFoundException:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="...")
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)

