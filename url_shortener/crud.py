from url_shortener.database.db import new_session
from url_shortener.database.models import ShortURL
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from url_shortener.exceptions import SlugAlreadyExists


async def add_slug_to_db(slug: str, long_url: str):
    async with new_session() as session:
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
        )
        session.add(new_slug)
        try: 
            await session.commit()
        except IntegrityError:
            raise SlugAlreadyExists

        

async def get_url_from_db(slug: str) -> str | None:
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        result = await session.execute(query)
        res: ShortURL | None = result.scalar_one_or_none()
    return res.long_url if res.long_url else None

    