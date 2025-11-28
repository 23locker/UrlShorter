from sqlalchemy import select

from database.models import ShortURL

from .db import new_session


async def add_slug_to_db(
    slug: str,
    user_url: str,
):
    async with new_session() as session:
        new_slug = ShortURL(
            slug=slug,
            user_url=user_url,
        )
        session.add(new_slug)
        await session.commit()


async def get_url_by_slug(slug: str) -> str | None:
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        result = await session.execute(query)
        res: ShortURL | None = result.scalar_one_or_none()
        return res.user_url if res.user_url else None
