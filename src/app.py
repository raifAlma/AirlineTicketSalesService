import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.exceptions import UserAlreadyExists

from actions.create_superuser import create_superuser
from api.api_v1 import router as api_v1_router
from container import Container
from settings import settings


load_dotenv()
container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_database_url())
    print(f"Connecting to database with URL: {settings.database.get_database_url()}")
    container.wire(modules=["infrastructure.database.postgresql.session"])

    superuser_email = os.getenv("SUPERUSER_EMAIL")
    print(f"DEBUG: superuser_email={superuser_email}")  # временно добавьте
    superuser_password = os.getenv("SUPERUSER_PASSWORD")

    if superuser_email and superuser_password:
        try:
            await create_superuser(
                email=superuser_email,
                password=superuser_password,
                full_name=os.getenv("SUPERUSER_FULL_NAME", "Admin"),
                phone=os.getenv("SUPERUSER_PHONE", "00000000000"),
            )
        except UserAlreadyExists:
            print(f"Superuser {superuser_email} already exists, skipping creation")

    try:
        yield
    finally:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)
