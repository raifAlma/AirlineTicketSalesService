import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient

from actions.create_superuser import create_superuser
from app import app, container
from settings import settings


fake = Faker()


@pytest.fixture(scope="function", autouse=True)
async def initialize_db():
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())
    container.wire(modules=["infrastructure.database.postgresql.session"])
    yield
    await sessionmanager.close()
    container.unwire()


@pytest.fixture(scope="function")
async def create_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        clean_phone = "".join(filter(str.isdigit, fake.unique.phone_number()))[:15]
        payload = {
            "email": fake.unique.email(),
            "password": "str_345",
            "full_name": fake.name(),
            "phone": clean_phone,
            "is_verified": True,
        }
        resp = await ac.post("/api/v1/auth/register", json=payload)
        assert resp.status_code == 201

        resp = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": payload["email"],
                "password": payload["password"],
            },
        )
        print("Login status:", resp.status_code)
        print("Login body:", resp.text)
        assert resp.status_code == 200
        token = resp.json()["access_token"]
    return {**payload, "token": token}


@pytest.fixture(scope="function")
async def create_superuser_and_token():
    email = fake.unique.email()
    password = "super_str_345"
    await create_superuser(
        email=email,
        password=password,
        full_name=fake.name(),
        phone="".join(filter(str.isdigit, fake.unique.phone_number()))[:15],
    )

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post(
            "/api/v1/auth/login",
            data={
                "username": email,
                "password": password,
            },
        )
        assert resp.status_code == 200
        token = resp.json()["access_token"]
    return {"email": email, "password": password, "token": token}


@pytest.fixture
def unique_airport_code():
    return fake.unique.lexify("???").upper()


@pytest.fixture
async def created_airport(create_superuser_and_token, unique_airport_code):
    token = create_superuser_and_token["token"]
    code = unique_airport_code
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        resp = await ac.post(
            "/api/v1/airport",
            json={"code": code, "name": "Heathrow", "city": "London", "country": "USA"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        data = resp.json()
        print(data)
        return {"id": data["id"], "code": code}
