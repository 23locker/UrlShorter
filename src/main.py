from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import get_url_by_slug
from src.database.db import engine, new_session
from src.database.models import Base
from src.exceptions import NoUserUrlFoundError, SlugAlreadyExistsError
from src.service import generate_short_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


@app.post("/short_url")
async def generate_slug_url(
    session: Annotated[AsyncSession, Depends(get_session)],
    user_url: Annotated[str, Body(embed=True)],
):
    try:
        new_slug = await generate_short_url(user_url, session)
    except SlugAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось сгенерировать slug",
        )
    return {"data": new_slug}


@app.get("/{slug}")
async def redirect_to_url(
    session: Annotated[AsyncSession, Depends(get_session)],
    slug: str,
):
    try:
        user_url = await get_url_by_slug(slug, session)
    except NoUserUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не существует"
        )
    return RedirectResponse(url=user_url, status_code=status.HTTP_302_FOUND)
