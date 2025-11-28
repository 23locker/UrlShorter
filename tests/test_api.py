from httpx import AsyncClient


async def test_get_slug(ac: AsyncClient):
    create_resp = await ac.post("/short_url", json={"user_url": "https://example.com"})
    slug = create_resp.json()["data"]

    get_resp = await ac.get(f"/{slug}")

    assert get_resp.status_code == 307 or get_resp.status_code == 302
    # если редирект, можно проверить куда
    assert "location" in get_resp.headers


async def test_generate_slug(ac: AsyncClient):
    payload = {"user_url": "https://site.com"}

    response = await ac.post("/short_url", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    slug = data["data"]
    assert isinstance(slug, str)
