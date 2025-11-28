from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database.models import ShortURL
from src.exceptions import SlugAlreadyExistsError


async def add_slug_to_db(
    slug: str,
    user_url: str,
    session,
):
    new_slug = ShortURL(
        slug=slug,
        user_url=user_url,
    )
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsError


async def get_url_by_slug(
    slug: str,
    session,
) -> str | None:
    query = select(ShortURL).filter_by(slug=slug)
    result = await session.execute(query)
    res: ShortURL | None = result.scalar_one_or_none()
    return res.user_url if res else None
