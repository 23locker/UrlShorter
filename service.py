from database.crud import add_slug_to_db, get_url_by_slug
from exceptions import NoUserUrlFoundError
from shortener import generate_random_slug


async def generate_short_url(
    user_url: str,
) -> str:
    # generate slug -> add slug to db -> give to user
    slug = generate_random_slug()
    await add_slug_to_db(slug, user_url)
    return slug


async def get_user_url_by_slug(
    slug: str,
) -> str:
    user_url = await get_url_by_slug(slug)
    if not user_url:
        raise NoUserUrlFoundError()
    return user_url
