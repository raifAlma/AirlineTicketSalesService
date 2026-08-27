from httpx import ASGITransport, AsyncClient

from app import app
from tests.conftest import unique_airport_code


async def test_create_airport_requires_superuser(create_user, unique_airport_code):
    token = create_user["token"]
    code = unique_airport_code
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post(
            "/api/v1/airport",
            json={"code": code, "name": "Heathrow", "city": "London", "country": "USA"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert resp.status_code == 403


async def test_superuser_can_create_airport(created_airport):
    assert created_airport["id"] is not None


async def test_create_airport_with_city_101_symbol_raises_error(
    create_superuser_and_token, unique_airport_code
):
    token = create_superuser_and_token["token"]
    code = unique_airport_code
    long_city = "A" * 101
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post(
            "/api/v1/airport",
            json={
                "code": code,
                "name": "Heathrow",
                "city": long_city,
                "country": "USA",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 422


async def test_search_airport_by_code(created_airport):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        code = created_airport["code"]
        payload = {"q": code}
        resp = await ac.get("/api/v1/airport/search", params=payload)
        assert resp.status_code == 200


async def test_user_can_delete_airport(create_user, created_airport):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        token = create_user["token"]
        id = created_airport["id"]
        resp = await ac.delete(
            f"/api/v1/airport/{id}",
            headers={"Authorization": f"Bearer {token}"},
            params={"id": id},
        )
        assert resp.status_code == 403


async def test_superuser_can_delete_airport(
    create_superuser_and_token, created_airport
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        token = create_superuser_and_token["token"]
        id = created_airport["id"]
        resp = await ac.delete(
            f"/api/v1/airport/{id}", headers={"Authorization": f"Bearer {token}"}
        )
        assert resp.status_code == 204


async def test_create_airport_with_duplicate_code(
    create_superuser_and_token, created_airport
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        token = create_superuser_and_token["token"]
        code = created_airport["code"]
        resp = await ac.post(
            "/api/v1/airport",
            json={"code": code, "name": "Heathrow", "city": "London", "country": "USA"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 400, "Должен быть конфликт при дубликате кода"

        body = resp.json()
        # Проверяем, что в ответе есть понятное сообщение об ошибке
        assert "already" in str(body).lower() or "exists" in str(body).lower()
