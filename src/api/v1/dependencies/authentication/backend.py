from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from api.v1.dependencies.strategy import get_database_strategy
from infrastructure.authentication.transport import bearer_transport

authentication_backend = AuthenticationBackend(
    name="access-token-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)