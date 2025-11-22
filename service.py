from shortener import generate_slug
from crud import add_slug_to_db, get_url_from_db
from exceptions import NoUrlFoundException, ShortenerBaseException, SlugAlreadyExists


async def generate_short_url(
    long_url: str
) -> str:
    slug = generate_slug()
    for _ in range(5):
        try:
            await add_slug_to_db(slug, long_url)
            return slug
        except SlugAlreadyExists:
            continue

async def get_url_by_slug(
    slug: str
):
    url = await get_url_from_db(slug)
    if not url:
        raise NoUrlFoundException
    return url
    