import pytest
from httpx import AsyncClient, ASGITransport

from app import app
from app import container
from settings import settings

from tests.api.test_airport_api import fake


@pytest.fixture(scope="function", autouse=True)
async def initialize_db():
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())
    yield
    await sessionmanager.close()


@pytest.fixture(scope="function")
async def create_user():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        clean_phone = ''.join(filter(str.isdigit,
                                     fake.unique.phone_number()))[:15]
        payload = {
            'email': fake.unique.email(),
            'password': 'str_345',
            'full_name': fake.name(),
            'phone_number': clean_phone,
            'passport_number': str(fake.unique.random_number(digits=8)),
        }
        resp = await ac.post("/api/v1/auth/register", json=payload)
        assert resp.status_code == 201

        resp = await ac.post("/api/v1/auth/login", data={
            'username': payload['email'],
            'password': payload['password'],
        })
        assert resp.status_code == 200
        token = resp.json()['access_token']
    return {**payload, "token": token}


@pytest.fixture(scope="function")
async def create_superuser_and_token():
    email = fake.unique.email()
    password = 'super_str_345'
    await create_superuser(
        email=email,
        password=password,
        full_name=fake.name(),
        phone=''.join(filter(str.isdigit, fake.unique.phone_number()))[:15],
    )



    async with AsyncClient(transport = ASGITransport(app=app),
                           base_url="http://test") as ac:
        resp = await ac.post("/api/v1/auth/login", data={
            'username': email,
            'password': password,
        })
        assert resp.status_code == 200
        token = resp.json()['access_token']
    return {'email': email, 'password': password, 'token': token}



