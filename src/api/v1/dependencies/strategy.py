import uuid

from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

import settings
from infrastructure.database.postgresql.models.access_token import AccessToken


def get_database_strategy(
    access_token_db: AccessTokenDatabase['AccessToken'] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db,
                            lifetime_seconds=settings._AccessToken.lifetime_seconds)
