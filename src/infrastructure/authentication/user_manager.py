import logging
import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

import settings
from infrastructure.database.postgresql.models import User


log = logging.getlogger(__name__)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret
    async def on_after_register(self, user: User, request: Request | None = None):
        log.warning(f"User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        log.warning(f"User %r has forgot their password. Reset token: %r", user.id, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        log.warning(f"Verification requested for user %r. Verification token: %r", user.id, token)


