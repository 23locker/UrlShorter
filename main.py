from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from database.crud import get_url_by_slug
from database.db import engine
from database.models import Base
from exceptions import NoUserUrlFoundError
from service import generate_short_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/short_url")
async def generate_slug_url(
    user_url: str = Body(embed=True),
):
    new_slug = await generate_short_url(user_url)
    return {"data": new_slug}


@app.get("/{slug}")
async def redirect_to_url(slug: str):
    try:
        user_url = await get_url_by_slug(slug)
    except NoUserUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ссылка не существует"
        )
    return RedirectResponse(url=user_url, status_code=status.HTTP_302_FOUND)
