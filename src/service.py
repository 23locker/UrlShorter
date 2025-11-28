import re

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import add_slug_to_db, get_url_by_slug
from src.exceptions import NotValidUserUrl, NoUserUrlFoundError, SlugAlreadyExistsError
from src.shortener import generate_random_slug

pattern = r"^https:\/\/([A-Za-z0-9-]+\.)+[A-Za-z]{2,}([\/?#][^\s]*)?$"


async def generate_short_url(
    user_url: str,
    session: AsyncSession,
) -> str:
    # generate slug -> add slug to db -> give to user
    if not re.match(pattern, user_url):
        raise NotValidUserUrl()

    async def _generate_slug() -> str:
        slug = generate_random_slug()
        await add_slug_to_db(slug, user_url, session)
        return slug

    for attempt in range(5):
        try:
            slug = await _generate_slug()
            return slug
        except SlugAlreadyExistsError:
            if attempt == 4:
                raise SlugAlreadyExistsError()


async def get_user_url_by_slug(
    slug: str,
) -> str:
    user_url = await get_url_by_slug(slug, session)
    if not user_url:
        raise NoUserUrlFoundError()
    return user_url
