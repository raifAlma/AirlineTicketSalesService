from app import app
from tests.conftest import unique_aircraft_model
from httpx import ASGITransport, AsyncClient

async def test_create_aircraft_requires_superuser(create_user, unique_aircraft_model):
    token = create_user["token"]
    model = unique_aircraft_model
    async with AsyncClient(
        transport = ASGITransport(app = app), base_url="http://test"
    ) as ac:
        resp = await ac.post(
            '/api/v1/aircraft',
            json={'model': model, 'rows': 30,
                  'seats_per_row': 4, 'business_rows': 5
                  },
            headers={'Authorization': f'Bearer {token}'},
        )

    assert resp.status_code == 403
